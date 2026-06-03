from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.api.database import get_session
from app.api.services.focus_service import FocusService
from typing import Optional

router = APIRouter(prefix="/pomodoro", tags=["pomodoro"])

@router.post("/complete")
def complete_session(task_id: Optional[int] = None, duration: int = 25, session: Session = Depends(get_session)):
    return FocusService.record_session(session, task_id, duration)