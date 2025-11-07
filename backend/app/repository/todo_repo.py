from sqlalchemy.orm import Session
from ..models.todo import Todo
from datetime import datetime

# NOTE: SQLAlchemy model attributes are dynamically instrumented; static type
# checkers may flag direct assignment. These are valid runtime operations.
# type: ignore
from ..schemas.todo import TodoCreate


def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(
        title=todo.title,
        description=todo.description,
        scheduled_at=todo.scheduled_at,
        deadline_at=todo.deadline_at,
        priority=todo.priority,
        status=todo.status,
        order=todo.order,
        project_id=todo.project_id,
        completed_at=(datetime.utcnow() if todo.status == "completed" else None),
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title  # type: ignore[attr-defined]
        db_todo.description = todo.description  # type: ignore[attr-defined]
        db_todo.scheduled_at = todo.scheduled_at  # type: ignore[attr-defined]
        db_todo.deadline_at = todo.deadline_at  # type: ignore[attr-defined]
        db_todo.priority = todo.priority  # type: ignore[attr-defined]
        prev_status = db_todo.status
        db_todo.status = todo.status  # type: ignore[attr-defined]
        db_todo.order = todo.order  # type: ignore[attr-defined]
        db_todo.project_id = todo.project_id  # type: ignore[attr-defined]
        # Auto timestamp completed_at when transitioning to completed; clear if leaving
        if prev_status != "completed" and todo.status == "completed" and not db_todo.completed_at:  # type: ignore[attr-defined]
            db_todo.completed_at = datetime.utcnow()  # type: ignore[attr-defined]
        elif todo.status != "completed":
            db_todo.completed_at = None  # type: ignore[attr-defined]
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
