from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from ..main import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    notes = Column(String)
    scheduled_at = Column(DateTime)
    deadline_at = Column(DateTime)
    priority = Column(Enum("low", "mid", "high", "urgent", name="priority_enum"))
    status = Column(Enum("undone", "done", "cancelled", name="status_enum"))
    order = Column(Integer)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Project", back_populates="todos")
    tags = relationship("Tag", secondary="todo_tags", back_populates="todos")
