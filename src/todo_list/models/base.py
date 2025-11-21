from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
from enum import Enum


class TaskStatus(Enum):
    """Enum representing possible task statuses."""
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


@dataclass
class Project:
    """Project entity representing a collection of tasks."""
    project_id: int
    name: str
    description: str
    created_at: datetime = field(default_factory=datetime.now)
    tasks: List['Task'] = field(default_factory=list)
    
    def __str__(self) -> str:
        return f"Project(id={self.project_id}, name='{self.name}')"


@dataclass
class Task:
    """Task entity representing a single task item."""
    task_id: int
    project_id: int
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    deadline: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def change_status(self, new_status: TaskStatus) -> None:
        """Change the status of the task."""
        self.status = new_status
    
    def __str__(self) -> str:
        return f"Task(id={self.task_id}, title='{self.title}', status={self.status.value})"
