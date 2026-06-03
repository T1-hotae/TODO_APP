from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from app.api.database import init_db
from app.api.routes import todos
from app.ui.components.todo_list import create_todo_ui

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 데이터베이스 테이블 생성 초기화
    init_db()
    yield
    # Shutdown: 리소스 정리 (필요시)

app = FastAPI(
    title="ZenTodo REST API Server",
    description="ZenTodo의 백엔드를 전담하는 REST API 서버입니다.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(todos.router, prefix="/api")

# Phase 3: Gradio UI 마운트
with gr.Blocks(css="app/ui/styles/custom.css", title="ZenTodo") as demo:
    gr.Markdown("# 🧘 ZenTodo")
    create_todo_ui()

app = gr.mount_gradio_app(app, demo, path="/")

@app.get("/api/health", tags=["health"])
def health_check():
    """서버 헬스 체크 엔드포인트"""
    return {"status": "healthy", "service": "ZenTodo"}
