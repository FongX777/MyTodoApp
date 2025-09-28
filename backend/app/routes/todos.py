from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import repository
from ..database import SessionLocal
from ..schemas.todo import Todo, TodoCreate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/todos", response_model=Todo)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)):
    return repository.todo_repo.create_todo(db=db, todo=todo)

@router.get("/todos", response_model=list[Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    todos = repository.todo_repo.get_todos(db, skip=skip, limit=limit)
    return todos

@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = repository.todo_repo.get_todo(db, todo_id=todo_id)
    return db_todo

@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo_endpoint(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    return repository.todo_repo.update_todo(db=db, todo_id=todo_id, todo=todo)
