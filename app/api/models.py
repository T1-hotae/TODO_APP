from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class TodoBase(SQLModel):
    title: str = Field(index=True)
    content: Optional[str] = None
    priority: str = Field(default="Medium") # High, Medium, Low
    category: str = Field(default="General")
    due_date: Optional[datetime] = None
    is_completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[datetime] = None
    is_completed: Optional[bool] = None