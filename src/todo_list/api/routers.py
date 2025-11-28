from fastapi import APIRouter

from .controllers.project_controller import router as project_router
from .controllers.task_controller import router as task_router


api_router = APIRouter()

api_router.include_router(project_router, prefix="/projects", tags=["projects"])
api_router.include_router(task_router, prefix="/tasks", tags=["tasks"])


__all__ = ['api_router']
