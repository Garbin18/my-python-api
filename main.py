from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 允许跨域请求（替换为你的 Vercel 前端域名）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体域名
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello from Python API!"}

@app.get("/api/data")
def get_data():
    return {"data": [1, 2, 3]}
