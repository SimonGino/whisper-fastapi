# Stage 1: Build the frontend
FROM node:20 as frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
# Skip type checking, only run the build
RUN npm run build -- --no-astro-check

# Stage 2: Build the backend
FROM python:3.11-slim as backend-builder
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Stage 3: Final image
FROM python:3.11-slim
WORKDIR /app

# Install ffmpeg
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy backend dependencies
COPY --from=backend-builder /usr/local/lib/python3.11 /usr/local/lib/python3.11
COPY --from=backend-builder /usr/local/bin/ /usr/local/bin/

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build output
COPY --from=frontend-builder /frontend/dist ./frontend/dist

# Install aiofiles for serving static files if necessary
RUN pip install aiofiles

# Copy start script
COPY start.sh .
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Set a default value for ENV_FILE
ENV ENV_FILE="/app/.env"

# Start the application
CMD ["./start.sh"]
