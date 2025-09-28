from sqlalchemy.orm import Session
from ..models.todo import Todo

def get_todo(db: Session, todo_id: int):
    return db.query(Todo).filter(Todo.id == todo_id).first()

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: Todo):
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo

def update_todo(db: Session, todo_id: int, todo: Todo):
    db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    db_todo.title = todo.title
    db_todo.status = todo.status
    db.commit()
    db.refresh(db_todo)
    return db_todo
