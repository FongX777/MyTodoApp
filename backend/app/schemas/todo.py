from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    deadline_at: Optional[datetime] = None
    priority: Optional[str] = "low"
    status: Optional[str] = "pending"
    order: Optional[int] = None
    project_id: Optional[int] = None


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True
