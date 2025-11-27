import os

from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from todo_list.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    _max_name_length = int(os.getenv('MAX_PROJECT_NAME_LENGTH', 100))
    _max_description_length = int(os.getenv('MAX_PROJECT_DESCRIPTION_LENGTH', 1000))
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(_max_name_length), unique=True, index=True, nullable=False)
    description = Column(String(_max_description_length))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"
