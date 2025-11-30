import os
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

from todo_list.models.task import TaskStatus


class TaskCreate(BaseModel):
    """Schema for creating a new task"""
    title: str = Field(
        ...,
        min_length=1,
        max_length=int(os.getenv('MAX_TASK_TITLE_LENGTH', 200)),
        description="Task title"
    )
    description: Optional[str] = Field(
        None,
        max_length=int(os.getenv('MAX_TASK_DESCRIPTION_LENGTH', 2000)),
        description="Task description"
    )
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Write documentation",
                "description": "Complete API documentation",
                "deadline": "2024-12-31T17:00:00"
            }
        }


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=int(os.getenv('MAX_TASK_TITLE_LENGTH', 200)),
        description="Task title"
    )
    description: Optional[str] = Field(
        None,
        max_length=int(os.getenv('MAX_TASK_DESCRIPTION_LENGTH', 2000)),
        description="Task description"
    )
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Updated Task Title",
                "description": "Updated task description",
                "deadline": "2024-12-31T18:00:00"
            }
        }


class TaskStatusUpdate(BaseModel):
    """Schema for updating task status"""
    status: TaskStatus = Field(..., description="New task status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "doing"
            }
        }
