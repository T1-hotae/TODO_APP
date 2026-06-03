from sqlmodel import Session, select
from app.api.models import Todo, TodoCreate, TodoUpdate
from typing import List

class TodoService:
    @staticmethod
    def create_todo(session: Session, todo_data: TodoCreate) -> Todo:
        db_todo = Todo.model_validate(todo_data)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def get_todos(session: Session) -> List[Todo]:
        statement = select(Todo).order_by(Todo.created_at.desc())
        return session.exec(statement).all()

    @staticmethod
    def update_todo(session: Session, todo_id: int, todo_data: TodoUpdate) -> Todo:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return None
        todo_dict = todo_data.model_dump(exclude_unset=True)
        for key, value in todo_dict.items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

    @staticmethod
    def delete_todo(session: Session, todo_id: int):
        db_todo = session.get(Todo, todo_id)
        if db_todo:
            session.delete(db_todo)
            session.commit()
        return db_todo