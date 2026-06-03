from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from app.api.database import get_session
from app.api.services.todo_service import TodoService
from app.llm.groq_client import answer_with_todos

router = APIRouter(prefix="/ask", tags=["ask"])


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str


@router.post("", response_model=AskResponse)
def ask(req: AskRequest, session: Session = Depends(get_session)):
    if not req.question or not req.question.strip():
        raise HTTPException(status_code=400, detail="질문을 입력해주세요.")

    todos = TodoService.get_todos(session)
    todo_dicts = [
        {
            "id": t.id,
            "title": t.title,
            "is_completed": t.is_completed,
            "due_date": str(t.due_date) if t.due_date else None,
            "created_at": str(t.created_at),
        }
        for t in todos
    ]

    answer = answer_with_todos(req.question.strip(), todo_dicts)
    return AskResponse(answer=answer)
