from typing import Dict, List, Optional

from ..models.base import Project, Task
from ..exceptions.base import ProjectNotFoundError, TaskNotFoundError
from . import StorageProtocol


class InMemoryStorage(StorageProtocol):
    """In-memory storage for projects and tasks."""
    
    def __init__(self) -> None:
        self._projects: Dict[int, Project] = {}
        self._tasks: Dict[int, Task] = {}
        self._project_counter = 0
        self._task_counter = 0
        self._project_name_index: Dict[str, int] = {}
    
    def create_project(self, project: Project) -> Project:
        """Store a new project."""
        self._project_counter += 1
        project.project_id = self._project_counter
        self._projects[project.project_id] = project
        self._project_name_index[project.name.lower()] = project.project_id
        return project
    
    def get_project(self, project_id: int) -> Optional[Project]:
        """Get a project by ID."""
        return self._projects.get(project_id)
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects."""
        return list(self._projects.values())
    
    def update_project(self, project: Project) -> Project:
        """Update an existing project."""
        if project.project_id not in self._projects:
            raise ProjectNotFoundError(f"Project with ID {project.project_id} not found")
        
        old_project = self._projects[project.project_id]
        del self._project_name_index[old_project.name.lower()]
        
        self._projects[project.project_id] = project
        self._project_name_index[project.name.lower()] = project.project_id
        return project
    
    def delete_project(self, project_id: int) -> bool:
        """Delete a project and all its tasks (cascade delete)."""
        if project_id not in self._projects:
            return False
        
        project = self._projects[project_id]
        del self._project_name_index[project.name.lower()]
        del self._projects[project_id]
        
        task_ids_to_delete = [
            task_id for task_id, task in self._tasks.items() 
            if task.project_id == project_id
        ]
        for task_id in task_ids_to_delete:
            del self._tasks[task_id]
        
        return True
    
    def project_name_exists(self, name: str, exclude_project_id: Optional[int] = None) -> bool:
        """Check if a project name already exists."""
        name_lower = name.lower()
        if name_lower not in self._project_name_index:
            return False
        
        if exclude_project_id:
            return self._project_name_index[name_lower] != exclude_project_id
        
        return True
    
    def create_task(self, task: Task) -> Task:
        """Store a new task."""
        self._task_counter += 1
        task.task_id = self._task_counter
        self._tasks[task.task_id] = task
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return self._tasks.get(task_id)
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """Get all tasks for a specific project."""
        return [task for task in self._tasks.values() if task.project_id == project_id]
    
    def update_task(self, task: Task) -> Task:
        """Update an existing task."""
        if task.task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task.task_id} not found")
        
        self._tasks[task.task_id] = task
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        if task_id not in self._tasks:
            return False
        
        del self._tasks[task_id]
        return True
    
    def get_project_count(self) -> int:
        """Get total number of projects."""
        return len(self._projects)
    
    def get_task_count(self, project_id: Optional[int] = None) -> int:
        """Get total number of tasks."""
        if project_id:
            return len(self.get_tasks_by_project(project_id))
        return len(self._tasks)
