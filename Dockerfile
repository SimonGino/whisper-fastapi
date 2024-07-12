# 基于 Python 3.11 镜像构建
FROM python:3.11

# 设置工作目录
WORKDIR /app

# 复制项目代码到镜像中
COPY . /app

# 安装 ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# 安装项目依赖
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动命令，可以通过环境变量指定 .env 文件
CMD ["sh", "-c", "if [ -f $ENV_FILE ]; then cp $ENV_FILE .env; fi; uvicorn app.main:app --host 0.0.0.0 --port 8000"]

# 设定默认的环境变量
ENV ENV_FILE=".env"