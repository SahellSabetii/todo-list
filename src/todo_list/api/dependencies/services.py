from fastapi import Depends
from sqlalchemy.orm import Session

from todo_list.repositories.project_repository import ProjectRepository
from todo_list.repositories.task_repository import TaskRepository
from todo_list.services.project_service import ProjectService
from todo_list.services.task_service import TaskService

from .database import get_db


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """Dependency that provides ProjectService instance"""
    project_repo = ProjectRepository(db)
    return ProjectService(project_repo)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """Dependency that provides TaskService instance"""
    task_repo = TaskRepository(db)
    return TaskService(task_repo)
