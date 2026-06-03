from typing import Optional
from datetime import datetime, date
from sqlmodel import SQLModel, Field

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_completed: bool = Field(default=False)
    due_date: Optional[date] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(SQLModel):
    title: str
    due_date: Optional[date] = None

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[date] = None
