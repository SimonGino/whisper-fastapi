import json
import logging
import os
from typing import List

import aiofiles
import openai
from fastapi import APIRouter, HTTPException
from fastapi import File, UploadFile
from fastapi.responses import StreamingResponse
from pydub import AudioSegment

from backend.app.core.settings import get_settings
from backend.app.models.transcription import TranscriptionSegment

router = APIRouter()

# 设置OpenAI API密钥
openai.api_key = get_settings().OPENAI_API_KEY
openai.base_url = get_settings().OPENAI_API_BASE_URL

# 创建临时文件夹
os.makedirs("temp", exist_ok=True)


async def save_audio_file(file: UploadFile, path: str):
    async with aiofiles.open(path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)


def split_audio(input_file: str, max_size_mb: int = 25):
    try:
        audio = AudioSegment.from_file(input_file)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error reading audio file: {str(e)}")

    part_length_ms = int((max_size_mb * 1024 * 1024) / (audio.frame_rate * audio.frame_width) * 1000)
    parts = [audio[i:i + part_length_ms] for i in range(0, len(audio), part_length_ms)]
    return parts


async def transcribe_audio(file_path: str) -> List[TranscriptionSegment]:
    try:
        with open(file_path, 'rb') as audio_file:
            response = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                language="zh"
            )

            # 确保响应是一个字典
            if isinstance(response, dict):
                response_dict = response
            else:
                response_dict = response.model_dump()

            segments = []
            if isinstance(response_dict, list):
                # 如果响应直接是一个列表
                for segment in response_dict:
                    segments.append(TranscriptionSegment(
                        start=segment.get('start', 0),
                        end=segment.get('end'),
                        text=segment.get('text', '')
                    ))
            elif 'segments' in response_dict:
                # 如果响应是一个包含 'segments' 键的字典
                for segment in response_dict['segments']:
                    segments.append(TranscriptionSegment(
                        start=segment.get('start', 0),
                        end=segment.get('end'),
                        text=segment.get('text', '')
                    ))
            else:
                # 如果响应既不是列表也不包含 'segments' 键，则创建一个单一的段落
                segments.append(TranscriptionSegment(
                    start=0,
                    end=None,
                    text=response_dict.get('text', '')
                ))

            return segments
    except Exception as e:
        logging.error(f"Error in transcribe_audio: {str(e)}")
        # 移除对 response_dict 的引用，因为在异常情况下它可能未定义
        raise HTTPException(status_code=500, detail=f"Error in transcription: {str(e)}")


def remove_extension(filename: str) -> str:
    name, extension = os.path.splitext(filename)
    return name


async def process_audio_parts(audio_parts: List[AudioSegment], filename: str):
    for i, part in enumerate(audio_parts):
        filename_without_extension = remove_extension(filename)
        part_file_path = f"temp/{filename_without_extension}_part_{i}.mp3"
        part.export(part_file_path, format="mp3")

        try:
            # 转录音频文件
            segments = await transcribe_audio(part_file_path)

            for segment in segments:
                yield segment.json() + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
        finally:
            # 删除临时文件
            os.remove(part_file_path)

@router.post("/convert")
async def upload_file(file: UploadFile = File(...)):
    input_file_path = f"temp/{file.filename}"

    # 保存上传的文件
    await save_audio_file(file, input_file_path)

    # 分割音频文件（如果超过25MB）
    audio_parts = split_audio(input_file_path)

    # 删除原始文件
    os.remove(input_file_path)

    return StreamingResponse(process_audio_parts(audio_parts, file.filename), media_type="application/json")
