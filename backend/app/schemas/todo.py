from pydantic import BaseModel, field_validator
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

    @field_validator("status")
    def normalize_status(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        mapping = {
            "undone": "pending",
            "todo": "pending",
            "in_progress": "pending",
            "done": "completed",
            "complete": "completed",
            "completed": "completed",
            "cancel": "cancelled",
            "canceled": "cancelled",
            "cancelled": "cancelled",
        }
        lowered = v.lower()
        return mapping.get(lowered, lowered)


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int

    class Config:
        from_attributes = True
