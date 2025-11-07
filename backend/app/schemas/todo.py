from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class TodoPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TodoStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    deadline_at: Optional[datetime] = None
    priority: Optional[TodoPriority] = TodoPriority.low
    status: Optional[TodoStatus] = TodoStatus.pending
    order: Optional[int] = None
    project_id: Optional[int] = None
    completed_at: Optional[datetime] = None


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True


class TodoOrderUpdate(BaseModel):
    id: int
    order: int


class TodoOrdersUpdate(BaseModel):
    todo_orders: list[TodoOrderUpdate]
