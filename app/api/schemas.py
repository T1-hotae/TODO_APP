from typing import Optional
from pydantic import BaseModel, Field

class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1)

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    is_completed: Optional[bool] = None

class TodoResponse(BaseModel):
    id: int
    title: str
    is_completed: bool
    created_at: str

    class Config:
        from_attributes = True
