from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from app.api.database import init_db
from app.api.routes import todos, ask
from app.api.routes import chat as chat_route
from app.todo_list import create_todo_ui, PAGE_JS
from app.chat_ui import chat_demo


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="Todo REST API",
    description="간단한 Todo 앱 REST API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router, prefix="/api")
app.include_router(ask.router, prefix="/api")
app.include_router(chat_route.router, prefix="/api")


@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "healthy"}


with gr.Blocks(title="Todo App", js=PAGE_JS) as demo:
    create_todo_ui()

# /chat을 먼저 마운트해야 루트(/)가 /chat 요청을 가로채지 않음
app = gr.mount_gradio_app(app, chat_demo, path="/chat")
app = gr.mount_gradio_app(app, demo, path="/")
