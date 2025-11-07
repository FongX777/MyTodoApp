from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import repository
from ..database import SessionLocal
from ..schemas.todo import Todo, TodoCreate, TodoOrdersUpdate

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/todos", response_model=Todo, status_code=201)
def create_todo_endpoint(todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Create a new todo item.
    
    - **title**: Title of the todo (required)
    - **description**: Detailed description
    - **priority**: Priority level (low, medium, high)
    - **status**: Status (pending, completed)
    - **scheduled_at**: When the todo is scheduled
    - **deadline_at**: Deadline for the todo
    - **project_id**: Associated project ID
    - **order**: Display order within project
    """
    # Create a new todo item and return it with HTTP 201 Created
    return repository.todo_repo.create_todo(db=db, todo=todo)


@router.get("/todos", response_model=list[Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all todos with optional pagination.
    
    - **skip**: Number of todos to skip (default: 0)
    - **limit**: Maximum number of todos to return (default: 100)
    
    Returns a list of all todos ordered by creation time.
    """
    todos = repository.todo_repo.get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific todo by ID.
    
    - **todo_id**: The ID of the todo to retrieve
    
    Returns the todo if found, otherwise raises 404.
    """
    db_todo = repository.todo_repo.get_todo(db, todo_id=todo_id)
    return db_todo


@router.put("/todos/{todo_id}", response_model=Todo)
def update_todo_endpoint(todo_id: int, todo: TodoCreate, db: Session = Depends(get_db)):
    """
    Update an existing todo.
    
    - **todo_id**: The ID of the todo to update
    - **todo**: Updated todo data
    
    Returns the updated todo if found, otherwise raises 404.
    """
    return repository.todo_repo.update_todo(db=db, todo_id=todo_id, todo=todo)


@router.delete("/todos/{todo_id}")
def delete_todo_endpoint(todo_id: int, db: Session = Depends(get_db)):
    """
    Delete a todo by ID.
    
    - **todo_id**: The ID of the todo to delete
    
    Returns success message if deleted, otherwise raises 404.
    """
    repository.todo_repo.delete_todo(db=db, todo_id=todo_id)
    return {"message": "Todo deleted successfully"}


@router.put("/todos/reorder")
def update_todo_orders_endpoint(orders: TodoOrdersUpdate, db: Session = Depends(get_db)):
    """
    Update the order of multiple todos within a project.
    
    - **todo_orders**: List of todo IDs with their new order values
    
    Use this endpoint to reorder todos by drag-and-drop in the UI.
    Returns success message after updating orders.
    """
    todo_orders = [{"id": order.id, "order": order.order} for order in orders.todo_orders]
    return repository.todo_repo.update_todo_orders(db=db, todo_orders=todo_orders)
