from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from todo_list.services.project_service import ProjectService
from todo_list.api.controller_schemas.requests.project_requests import ProjectCreate, ProjectUpdate
from todo_list.api.controller_schemas.responses.project_responses import ProjectResponse, ProjectListResponse
from todo_list.api.controller_schemas.responses.base_responses import StandardResponse, ErrorResponse
from todo_list.api.dependencies.services import get_project_service
from todo_list.exceptions import NotFoundException, DuplicateEntryException, ValidationException, BusinessRuleException


router = APIRouter(prefix="/projects", tags=["projects"])

@router.post(
    "/",
    response_model=StandardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    responses={
        201: {"model": StandardResponse, "description": "Project created successfully"},
        400: {"model": ErrorResponse, "description": "Validation error"},
        409: {"model": ErrorResponse, "description": "Project with this name already exists"}
    }
)
async def create_project(
    project_data: ProjectCreate,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project with the given name and description.
    
    - **name**: Project name
    - **description**: Optional project description
    """
    try:
        project = project_service.create_project(
            name=project_data.name,
            description=project_data.description
        )
        
        response_data = ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
            task_count=len(project.tasks)
        )
        
        return StandardResponse(
            status="success",
            message="Project created successfully",
            data=response_data
        )
        
    except DuplicateEntryException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"status": "error", "message": str(e)}
        )
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )

@router.get(
    "/",
    response_model=StandardResponse,
    summary="Get all projects",
    responses={
        200: {"model": StandardResponse, "description": "Projects retrieved successfully"}
    }
)
async def get_all_projects(
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Retrieve all projects with their task counts.
    """
    projects = project_service.get_all_projects()
    
    project_responses = []
    for project in projects:
        project_responses.append(
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                created_at=project.created_at,
                updated_at=project.updated_at,
                task_count=len(project.tasks)
            )
        )
    
    response_data = ProjectListResponse(
        projects=project_responses,
        total=len(project_responses)
    )
    
    return StandardResponse(
        status="success",
        message="Projects retrieved successfully",
        data=response_data
    )

@router.get(
    "/{project_id}",
    response_model=StandardResponse,
    summary="Get project by ID",
    responses={
        200: {"model": StandardResponse, "description": "Project retrieved successfully"},
        404: {"model": ErrorResponse, "description": "Project not found"}
    }
)
async def get_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Retrieve a specific project by its ID.
    
    - **project_id**: Project ID (integer)
    """
    try:
        project = project_service.get_project(project_id)
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        response_data = ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
            task_count=len(project.tasks)
        )
        
        return StandardResponse(
            status="success",
            message="Project retrieved successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )

@router.put(
    "/{project_id}",
    response_model=StandardResponse,
    summary="Update project",
    responses={
        200: {"model": StandardResponse, "description": "Project updated successfully"},
        404: {"model": ErrorResponse, "description": "Project not found"},
        409: {"model": ErrorResponse, "description": "Project name already exists"}
    }
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Update an existing project.
    
    - **project_id**: Project ID to update (integer)
    - **name**: New project name (optional)
    - **description**: New project description (optional)
    """
    try:
        project = project_service.update_project(
            project_id=project_id,
            name=project_data.name,
            description=project_data.description
        )
        
        response_data = ProjectResponse(
            id=project.id,
            name=project.name,
            description=project.description,
            created_at=project.created_at,
            updated_at=project.updated_at,
            task_count=len(project.tasks)
        )
        
        return StandardResponse(
            status="success",
            message="Project updated successfully",
            data=response_data
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )
    except (DuplicateEntryException, ValidationException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )

@router.delete(
    "/{project_id}",
    response_model=StandardResponse,
    summary="Delete project",
    responses={
        200: {"model": StandardResponse, "description": "Project deleted successfully"},
        404: {"model": ErrorResponse, "description": "Project not found"},
        400: {"model": ErrorResponse, "description": "Cannot delete project with tasks"}
    }
)
async def delete_project(
    project_id: int,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Delete a project by its ID.
    
    - **project_id**: Project ID to delete (integer)
    - **Note**: Projects with existing tasks cannot be deleted
    """
    try:
        project_service.delete_project(project_id)
        
        return StandardResponse(
            status="success",
            message="Project deleted successfully",
            data=None
        )
        
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": str(e)}
        )
    except BusinessRuleException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": str(e)}
        )
