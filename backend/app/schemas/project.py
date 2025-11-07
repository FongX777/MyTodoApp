from pydantic import BaseModel
from typing import Optional
from enum import Enum


class ProjectStatus(str, Enum):
    active = "active"
    completed = "completed"
    archived = "archived"


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    status: Optional[ProjectStatus] = ProjectStatus.active


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    class Config:
        from_attributes = True
