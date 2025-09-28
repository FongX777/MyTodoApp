from sqlalchemy.orm import Session
from ..models.todo import Todo
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
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: TodoCreate):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        db_todo.scheduled_at = todo.scheduled_at
        db_todo.deadline_at = todo.deadline_at
        db_todo.priority = todo.priority
        db_todo.status = todo.status
        db_todo.order = todo.order
        db_todo.project_id = todo.project_id
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()
    return db_todo
