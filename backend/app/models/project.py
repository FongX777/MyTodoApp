from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from ..main import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    status = Column(Enum("undone", "done", "cancelled", name="project_status_enum"))

    todos = relationship("Todo", back_populates="project")
