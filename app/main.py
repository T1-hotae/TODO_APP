from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import gradio as gr
from app.api.database import init_db
from app.api.routes import todos
from app.todo_list import create_todo_ui

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

with gr.Blocks(title="Todo App") as demo:
    create_todo_ui()

app = gr.mount_gradio_app(app, demo, path="/")

@app.get("/api/health", tags=["health"])
def health_check():
    return {"status": "healthy"}
