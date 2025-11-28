from typing import List, Optional
from datetime import datetime

from pydantic import BaseModel


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    task_count: int = 0
    
    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    """Schema for project list response"""
    projects: List[ProjectResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "projects": [
                    {
                        "id": 1,
                        "name": "Work Tasks",
                        "description": "Professional tasks",
                        "created_at": "2024-01-10T09:15:00",
                        "updated_at": "2024-01-10T09:15:00",
                        "task_count": 5
                    }
                ],
                "total": 1
            }
        }
