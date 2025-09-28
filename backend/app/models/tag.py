from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..main import Base

todo_tags = Table('todo_tags', Base.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    todos = relationship("Todo", secondary=todo_tags, back_populates="tags")
