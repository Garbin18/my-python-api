from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os
from deepseek_api import deepseek_stream_generator
from openai_api import openai_stream_generator


# my_python_api\Scripts\activate
# uvicorn main:app --reload

app = FastAPI()

# CORS 配置（根据你的前端地址调整）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议指定具体域名
    allow_methods=["*"],
    allow_headers=["*"],
)

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# DEEPSEEK_API_KEY = '...'

@app.post("/api/openai")
async def chat_completion(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])

        async def event_stream():
            async for chunk in openai_stream_generator(messages, OPENAI_API_KEY):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/deepseek")
async def chat_completion(request: Request):
    try:
        data = await request.json()
        messages = data.get("messages", [])

        async def event_stream():
            async for chunk in deepseek_stream_generator(messages, DEEPSEEK_API_KEY):
                yield f"data: {json.dumps({'content': chunk})}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data")
def get_data():
    return {"data": [1, 2, 3]}

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "ok"}