from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel

from todo_list.models.task import TaskStatus


class TaskResponse(BaseModel):
    """Schema for task response"""
    id: int
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[datetime]
    created_at: datetime
    updated_at: Optional[datetime]
    closed_at: Optional[datetime]
    project_id: int
    project_name: str
    
    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Schema for task list response"""
    tasks: List[TaskResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "tasks": [
                    {
                        "id": 1,
                        "title": "Write documentation",
                        "description": "Complete API docs",
                        "status": "todo",
                        "deadline": "2024-12-31T17:00:00",
                        "created_at": "2024-01-10T09:15:00",
                        "updated_at": "2024-01-10T09:15:00",
                        "closed_at": None,
                        "project_id": 1,
                        "project_name": "Work Tasks"
                    }
                ],
                "total": 1
            }
        }
