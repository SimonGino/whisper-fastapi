# whisper-fastapi

### generate [requirements.txt](requirements.txt)
```shell
pip install pipreqs
pipreqs .
```

### Docker examples
 
```shell
docker build -t whisper-fastapi .                            
docker run -d -p 8000:8000 -e ENV_FILE=dev.env whisper-fastapi
```

