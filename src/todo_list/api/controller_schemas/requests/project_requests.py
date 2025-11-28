import os
from typing import Optional

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(
        ...,
        min_length=1,
        max_length=int(os.getenv('MAX_PROJECT_NAME_LENGTH', 100)),
        description="Project name"
    )
    description: Optional[str] = Field(
        None,
        max_length=int(os.getenv('MAX_PROJECT_DESCRIPTION_LENGTH', 1000)),
        description="Project description"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Work Tasks",
                "description": "Professional tasks and deadlines"
            }
        }


class ProjectUpdate(BaseModel):
    """Schema for updating an existing project"""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=int(os.getenv('MAX_PROJECT_NAME_LENGTH', 100)),
        description="Project name"
    )
    description: Optional[str] = Field(
        None,
        max_length=int(os.getenv('MAX_PROJECT_DESCRIPTION_LENGTH', 1000)),
        description="Project description"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Project Name",
                "description": "Updated project description"
            }
        }
