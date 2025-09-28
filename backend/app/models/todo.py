from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    scheduled_at = Column(DateTime)
    deadline_at = Column(DateTime)
    priority = Column(Enum("low", "medium", "high", "urgent", name="todo_priority_enum"))
    status = Column(Enum("pending", "completed", "cancelled", name="todo_status_enum"))
    order = Column(Integer)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="todos")
    tags = relationship("Tag", secondary="todo_tags", back_populates="todos")
