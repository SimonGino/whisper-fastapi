# whisper-fastapi
语音转文本
speech to text
### generate [requirements.txt](backend/requirements.txt)
```shell
pip install pipreqs
pipreqs .
```

### Docker examples
 
```shell
docker build -t whisper-fastapi .                            
docker run -v /absolute/path/to/your/.env:/app/.env -e ENV_FILE=/app/.env -p 8000:8000 whisper-fastapi
```

```shell
docker run -v $PWD/.env:/app/.env -e ENV_FILE=/app/.env -p 8000:8000 whisper-fastapi
```

