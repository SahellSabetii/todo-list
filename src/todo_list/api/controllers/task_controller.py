from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query

from todo_list.services.task_service import TaskService
from todo_list.services.project_service import ProjectService
from todo_list.api.controller_schemas.requests.task_requests import TaskCreate, TaskUpdate, TaskStatusUpdate
from todo_list.api.controller_schemas.responses.task_responses import TaskResponse, TaskListResponse
from todo_list.api.controller_schemas.responses.base_responses import StandardResponse, ErrorResponse
from todo_list.api.dependencies.services import get_task_service, get_project_service
from todo_list.exceptions import NotFoundException, ValidationException
from todo_list.models.task import TaskStatus


router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    responses={
        201: {"model": StandardResponse, "description": "Task created successfully"},
        400: {"model": ErrorResponse, "description": "Validation error"},
        404: {"model": ErrorResponse, "description": "Project not found"}
    }
)
async def create_task(
    task_data: TaskCreate,
    project_id: int = Query(..., description="Project ID to create task in"),
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Create a new task in the specified project.
    
    - **project_id**: Project ID (query parameter, required)
    - **title**: Task title
    - **description**: Optional task description
    - **deadline**: Optional task deadline (datetime)
    """
    try:
        project = project_service.get_project(project_id)
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        task = task_service.create_task(
            title=task_data.title,
            project_id=project_id,
            description=task_data.description,
            deadline=task_data.deadline
        )
        
        response_data = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            created_at=task.created_at,
            updated_at=task.updated_at,
            closed_at=task.closed_at,
            project_id=task.project_id,
            project_name=task.project.name
        )
        
        return StandardResponse(
            status="success",
            message="Task created successfully",
            data=response_data
        )
        
    except (NotFoundException, ValidationException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )

@router.get(
    "/",
    response_model=StandardResponse,
    summary="Get all tasks",
    responses={
        200: {"model": StandardResponse, "description": "Tasks retrieved successfully"}
    }
)
async def get_all_tasks(
    task_service: TaskService = Depends(get_task_service)
):
    """
    Retrieve all tasks across all projects.
    """
    tasks = task_service.get_all_tasks()
    
    task_responses = []
    for task in tasks:
        task_responses.append(
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                deadline=task.deadline,
                created_at=task.created_at,
                updated_at=task.updated_at,
                closed_at=task.closed_at,
                project_id=task.project_id,
                project_name=task.project.name
            )
        )
    
    response_data = TaskListResponse(
        tasks=task_responses,
        total=len(task_responses)
    )
    
    return StandardResponse(
        status="success",
        message="Tasks retrieved successfully",
        data=response_data
    )

@router.get(
    "/project/{project_id}",
    response_model=StandardResponse,
    summary="Get tasks by project",
    responses={
        200: {"model": StandardResponse, "description": "Tasks retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Project not found"}
    }
)
async def get_tasks_by_project(
    project_id: int,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Retrieve all tasks for a specific project.
    
    - **project_id**: Project ID (integer)
    """
    try:
        # Verify project exists
        project = project_service.get_project(project_id)
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        tasks = task_service.get_tasks_by_project(project_id)
        
        task_responses = []
        for task in tasks:
            task_responses.append(
                TaskResponse(
                    id=task.id,
                    title=task.title,
                    description=task.description,
                    status=task.status,
                    deadline=task.deadline,
                    created_at=task.created_at,
                    updated_at=task.updated_at,
                    closed_at=task.closed_at,
                    project_id=task.project_id,
                    project_name=task.project.name
                )
            )
        
        response_data = TaskListResponse(
            tasks=task_responses,
            total=len(task_responses)
        )
        
        return StandardResponse(
            status="success",
            message="Tasks retrieved successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )

@router.get(
    "/{task_id}",
    response_model=StandardResponse,
    summary="Get task by ID",
    responses={
        200: {"model": StandardResponse, "description": "Task retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def get_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Retrieve a specific task by its ID.
    
    - **task_id**: Task ID (integer)
    """
    try:
        task = task_service.get_task(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found")
        
        response_data = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            created_at=task.created_at,
            updated_at=task.updated_at,
            closed_at=task.closed_at,
            project_id=task.project_id,
            project_name=task.project.name
        )
        
        return StandardResponse(
            status="success",
            message="Task retrieved successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )

@router.put(
    "/{task_id}",
    response_model=StandardResponse,
    summary="Update task",
    responses={
        200: {"model": StandardResponse, "description": "Task updated successfully"},
        404: {"model": ErrorResponse, "description": "Task not found"},
        400: {"model": ErrorResponse, "description": "Validation error"}
    }
)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Update an existing task.
    
    - **task_id**: Task ID to update (integer)
    - **title**: New task title (optional)
    - **description**: New task description (optional)
    - **deadline**: New task deadline (optional)
    """
    try:
        update_data = {}
        if task_data.title is not None:
            update_data['title'] = task_data.title
        if task_data.description is not None:
            update_data['description'] = task_data.description
        if task_data.deadline is not None:
            update_data['deadline'] = task_data.deadline
        
        task = task_service.update_task(task_id, **update_data)
        
        response_data = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            created_at=task.created_at,
            updated_at=task.updated_at,
            closed_at=task.closed_at,
            project_id=task.project_id,
            project_name=task.project.name
        )
        
        return StandardResponse(
            status="success",
            message="Task updated successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )

@router.patch(
    "/{task_id}/status",
    response_model=StandardResponse,
    summary="Update task status",
    responses={
        200: {"model": StandardResponse, "description": "Task status updated successfully"},
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Update the status of a task.
    
    - **task_id**: Task ID to update (integer)
    - **status**: New task status (todo, doing, done)
    """
    try:
        task = task_service.update_task_status(task_id, status_data.status)
        
        response_data = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            created_at=task.created_at,
            updated_at=task.updated_at,
            closed_at=task.closed_at,
            project_id=task.project_id,
            project_name=task.project.name
        )
        
        return StandardResponse(
            status="success",
            message="Task status updated successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )

@router.post(
    "/{task_id}/close",
    response_model=StandardResponse,
    summary="Close task",
    responses={
        200: {"model": StandardResponse, "description": "Task closed successfully"},
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def close_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Close a task (mark as done).
    
    - **task_id**: Task ID to close (integer)
    """
    try:
        task = task_service.close_task(task_id)
        
        response_data = TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
            deadline=task.deadline,
            created_at=task.created_at,
            updated_at=task.updated_at,
            closed_at=task.closed_at,
            project_id=task.project_id,
            project_name=task.project.name
        )
        
        return StandardResponse(
            status="success",
            message="Task closed successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )

@router.get(
    "/overdue",
    response_model=StandardResponse,
    summary="Get overdue tasks",
    responses={
        200: {"model": StandardResponse, "description": "Overdue tasks retrieved successfully"}
    }
)
async def get_overdue_tasks(
    task_service: TaskService = Depends(get_task_service)
):
    """
    Retrieve all overdue tasks (tasks with past deadlines that are not done).
    """
    tasks = task_service.get_overdue_tasks()
    
    task_responses = []
    for task in tasks:
        task_responses.append(
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                status=task.status,
                deadline=task.deadline,
                created_at=task.created_at,
                updated_at=task.updated_at,
                closed_at=task.closed_at,
                project_id=task.project_id,
                project_name=task.project.name
            )
        )
    
    response_data = TaskListResponse(
        tasks=task_responses,
        total=len(task_responses)
    )
    
    return StandardResponse(
        status="success",
        message="Overdue tasks retrieved successfully",
        data=response_data
    )

@router.delete(
    "/{task_id}",
    response_model=StandardResponse,
    summary="Delete task",
    responses={
        200: {"model": StandardResponse, "description": "Task deleted successfully"},
        404: {"model": ErrorResponse, "description": "Task not found"}
    }
)
async def delete_task(
    task_id: int,
    task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a task by its ID.
    
    - **task_id**: Task ID to delete (integer)
    """
    try:
        task_service.delete_task(task_id)
        
        return StandardResponse(
            status="success",
            message="Task deleted successfully",
            data=None
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )
