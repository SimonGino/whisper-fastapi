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
docker run -d -p 8000:8000 -e ENV_FILE=.env whisper-fastapi
```

