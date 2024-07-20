#!/bin/bash

# Check if the ENV_FILE exists
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: Environment file $ENV_FILE not found!"
    exit 1
fi

# Export all variables from ENV_FILE
export $(grep -v '^#' $ENV_FILE | xargs)

# 启动 FastAPI 应用（包括静态文件服务）
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

# 启动前端静态文件服务器
python -m http.server 80 --directory frontend/build &

# 等待所有后台进程
wait
