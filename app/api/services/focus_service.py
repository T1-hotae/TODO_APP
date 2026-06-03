from sqlmodel import Session
from app.api.models import PomodoroSession
from datetime import datetime
from typing import Optional

class FocusService:
    @staticmethod
    def record_session(session: Session, task_id: Optional[int] = None, duration: int = 25):
        db_session = PomodoroSession(task_id=task_id, duration=duration)
        session.add(db_session)
        session.commit()
        session.refresh(db_session)
        return db_session