# 실행 방법: uvicorn fastapi_chat:app --reload
# 필수 설치 패키지: pip install fastapi uvicorn gradio requests langchain langchain-groq pydantic
# API 키 설정: 실행 전 환경변수에 GROQ_API_KEY를 설정해야 합니다.

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import gradio as gr
import requests
from typing import List, Any

load_dotenv()

# LangChain & Groq 관련 모듈
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

app = FastAPI()

# Pydantic 모델: API 요청 데이터(Body) 구조 정의
class ChatRequest(BaseModel):
    message: str
    history: List[Any] = []

# 1. FastAPI API: 채팅 메시지를 받아 LLM 응답을 반환하는 엔드포인트
@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    try:
        # 환경변수에서 Groq API 키 확인
        if not os.environ.get("GROQ_API_KEY"):
            return {"reply": "서버 오류: GROQ_API_KEY 환경변수가 설정되지 않았습니다."}
        
        # Groq LLM 초기화
        llm = ChatGroq(model="openai/gpt-oss-20b")
        
        # LangChain에 전달할 메시지 기록(History) 구성
        # Gradio 버전에 따라 history 형식이 다름:
        # - 구버전: [[user_msg, bot_msg], ...]
        # - 신버전(5.x): [{"role": "user", "content": "..."}, ...]
        messages = []
        for item in request.history:
            if isinstance(item, dict):
                role = item.get("role")
                content = item.get("content", "")
                if role == "user":
                    messages.append(HumanMessage(content=content))
                elif role == "assistant":
                    messages.append(AIMessage(content=content))
            elif isinstance(item, list) and len(item) == 2:
                user_msg, bot_msg = item
                messages.append(HumanMessage(content=user_msg))
                messages.append(AIMessage(content=bot_msg))
        
        # 현재 사용자의 새 메시지 추가
        messages.append(HumanMessage(content=request.message))
        
        # LLM 호출 및 응답 텍스트 추출
        response = llm.invoke(messages)
        return {"reply": response.content}
        
    except Exception as e:
        return {"reply": f"API 서버 내부 오류: {str(e)}"}


# 2. Gradio에서 API를 호출하는 함수
def call_chat_api(message, history):
    try:
        # FastAPI 엔드포인트 호출 (POST 요청)
        res = requests.post(
            "http://127.0.0.1:8000/api/chat",
            json={"message": message, "history": history}
        )
        return res.json()["reply"]
    except Exception as e:
        return f"연결 오류: {str(e)}\n(터미널에서 서버가 8000번 포트로 실행 중인지 확인하세요.)"


# 3. Gradio UI 구성 (ChatInterface 사용)
demo = gr.ChatInterface(
    fn=call_chat_api,
    title="FastAPI + Groq(LangChain) 챗봇",
    description="FastAPI 백엔드, Gradio UI, LangChain(Groq LLM)을 활용한 채팅 앱입니다."
)


# 4. FastAPI에 Gradio 앱 마운트
app = gr.mount_gradio_app(app, demo, path="/")