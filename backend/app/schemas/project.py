from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from enum import Enum


class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.active

    @field_validator("status", mode="before")
    def map_incoming_status(cls, v):  # type: ignore[override]
        """Allow alternative incoming values 'undone'/'done' mapping to DB enum."""
        mapping = {
            "undone": ProjectStatus.active,
            "done": ProjectStatus.completed,
        }
        if isinstance(v, str):
            return mapping.get(v, v)
        return v


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
