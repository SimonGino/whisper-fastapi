#!/bin/bash

# 如果存在环境文件，则复制到后端目录
if [ -f $ENV_FILE ]; then
    cp $ENV_FILE backend/.env
fi

# 启动 FastAPI 应用（包括静态文件服务）
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# 启动前端静态文件服务器
python -m http.server 80 --directory frontend/build &

# 等待所有后台进程
wait
