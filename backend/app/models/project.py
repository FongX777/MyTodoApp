from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from ..database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    # Original production enum values retained in DB
    status = Column(Enum("active", "completed", "cancelled", name="project_status_enum"), default="active")

    todos = relationship("Todo", back_populates="project")
