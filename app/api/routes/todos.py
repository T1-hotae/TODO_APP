from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app.api.database import get_session
from app.api.models import Todo, TodoCreate, TodoUpdate
from app.api.services.todo_service import TodoService

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=Todo)
def create_todo(todo: TodoCreate, session: Session = Depends(get_session)):
    return TodoService.create_todo(session, todo)

@router.get("/", response_model=List[Todo])
def read_todos(session: Session = Depends(get_session)):
    return TodoService.get_todos(session)

@router.patch("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoUpdate, session: Session = Depends(get_session)):
    db_todo = TodoService.update_todo(session, todo_id, todo)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@router.delete("/{todo_id}")
def delete_todo(todo_id: int, session: Session = Depends(get_session)):
    db_todo = TodoService.delete_todo(session, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"ok": True}