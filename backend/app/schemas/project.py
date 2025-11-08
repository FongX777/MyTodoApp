from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
from enum import Enum


class ProjectStatus(str, Enum):
    undone = "undone"  # maps to DB 'active'
    done = "done"  # maps to DB 'completed'
    cancelled = "cancelled"  # passthrough for cancelled state


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.undone


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

    @field_validator("status", mode="before")
    def map_db_status(cls, v):  # type: ignore[override]
        """Translate DB enum values to API-facing enum values."""
        mapping = {
            "active": ProjectStatus.undone,
            "completed": ProjectStatus.done,
            "cancelled": ProjectStatus.cancelled,
        }
        if isinstance(v, str):
            return mapping.get(v, v)
        return v
