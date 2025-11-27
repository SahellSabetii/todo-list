import enum
import os

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from todo_list.db.base import Base


class TaskStatus(enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    _max_title_length = int(os.getenv('MAX_TASK_TITLE_LENGTH', 200))
    _max_description_length = int(os.getenv('MAX_TASK_DESCRIPTION_LENGTH', 2000))
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(_max_title_length), nullable=False)
    description = Column(String(_max_description_length))
    status = Column(String(20), default=TaskStatus.TODO.value)
    deadline = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    closed_at = Column(DateTime(timezone=True), nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    
    project = relationship("Project", back_populates="tasks")
    
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', status='{self.status}')>"
