from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    is_completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(SQLModel):
    title: str

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None