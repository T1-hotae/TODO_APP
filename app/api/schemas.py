from typing import Optional
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, description="할 일 제목")
    content: Optional[str] = Field(default=None, description="상세 내용")
    priority: Optional[str] = Field(default="Medium", description="우선순위 (High, Medium, Low)")
    category: Optional[str] = Field(default="General", description="카테고리 분류")
    due_date: Optional[str] = Field(default=None, description="마감일 (YYYY-MM-DD)")

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1)
    content: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    due_date: Optional[str] = None
    is_completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    content: Optional[str]
    priority: str
    category: str
    due_date: Optional[str]
    is_completed: bool
    created_at: str
    d_day: Optional[int] = None

    class Config:
        from_attributes = True
