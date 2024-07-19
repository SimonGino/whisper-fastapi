from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from backend.app.api.endpoints import audio2text_converter

app = FastAPI()


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(audio2text_converter.router, prefix="/audio", tags=["audio"])

# 挂载静态文件
app.mount("/", StaticFiles(directory="/app/frontend/dist", html=True), name="static")

@app.get("/test")
async def test():
    return {"message": "Test route working"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
