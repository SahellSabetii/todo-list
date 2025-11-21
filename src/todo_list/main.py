from typing import List
from datetime import datetime

from .core.entities import Project, Task, TaskStatus
from .core.exceptions import (
    ValidationError, DuplicateProjectError, ProjectNotFoundError,
    TaskNotFoundError, LimitExceededError, InvalidStatusError
)
from .core.validators import (
    validate_project_name, validate_project_description,
    validate_task_title, validate_task_description, validate_deadline
)
from .db.in_memory_storage import InMemoryStorage
from .config import Config


class ToDoListApp:
    """Main application class for ToDoList."""
    
    def __init__(self) -> None:
        """Initialize the application with storage and configuration."""
        self.storage = InMemoryStorage()
        self.max_projects = Config.MAX_NUMBER_OF_PROJECTS
        self.max_tasks_per_project = Config.MAX_NUMBER_OF_TASKS_PER_PROJECT
    
    def create_project(self, name: str, description: str) -> Project:
        """Create a new project."""
        if self.storage.get_project_count() >= self.max_projects:
            raise LimitExceededError(f"Cannot create more than {self.max_projects} projects")
        
        validate_project_name(name)
        validate_project_description(description)
        
        if self.storage.project_name_exists(name):
            raise DuplicateProjectError(f"Project with name '{name}' already exists")
        
        project = Project(0, name, description)
        return self.storage.create_project(project)
    
    def edit_project(self, project_id: int, name: str, description: str) -> Project:
        """Edit an existing project."""
        project = self.storage.get_project(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        
        validate_project_name(name)
        validate_project_description(description)
        
        if self.storage.project_name_exists(name, project_id):
            raise DuplicateProjectError(f"Project with name '{name}' already exists")
        
        project.name = name
        project.description = description
        return self.storage.update_project(project)
    
    def delete_project(self, project_id: int) -> bool:
        """Delete a project and all its tasks."""
        return self.storage.delete_project(project_id)
    
    def add_task(
        self, 
        project_id: int, 
        title: str, 
        description: str, 
        deadline: datetime = None
    ) -> Task:
        """Add a new task to a project."""
        project = self.storage.get_project(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        
        if self.storage.get_task_count(project_id) >= self.max_tasks_per_project:
            raise LimitExceededError(
                f"Cannot create more than {self.max_tasks_per_project} tasks per project"
            )
        
        validate_task_title(title)
        validate_task_description(description)
        validate_deadline(deadline)
        
        task = Task(0, project_id, title, description, TaskStatus.TODO, deadline)
        return self.storage.create_task(task)
    
    def change_task_status(self, task_id: int, new_status: TaskStatus) -> Task:
        """Change the status of a task."""
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        
        task.change_status(new_status)
        return self.storage.update_task(task)
    
    def edit_task(
        self, 
        task_id: int, 
        title: str, 
        description: str, 
        status: TaskStatus,
        deadline: datetime = None
    ) -> Task:
        """Edit an existing task."""
        task = self.storage.get_task(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
        
        validate_task_title(title)
        validate_task_description(description)
        validate_deadline(deadline)
        
        task.title = title
        task.description = description
        task.status = status
        task.deadline = deadline
        
        return self.storage.update_task(task)
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        return self.storage.delete_task(task_id)
    
    def list_projects(self) -> List[Project]:
        """List all projects."""
        return self.storage.get_all_projects()
    
    def list_tasks(self, project_id: int) -> List[Task]:
        """List all tasks for a project."""
        project = self.storage.get_project(project_id)
        if not project:
            raise ProjectNotFoundError(f"Project with ID {project_id} not found")
        
        return self.storage.get_tasks_by_project(project_id)
    
    def get_task_status_from_string(self, status_str: str) -> TaskStatus:
        """Convert string to TaskStatus."""
        try:
            return TaskStatus(status_str.lower())
        except ValueError:
            raise InvalidStatusError(
                f"Invalid status: {status_str}. Must be one of: "
                f"{', '.join(status.value for status in TaskStatus)}"
            )


if __name__ == "__main__":
    print("ToDoList Application")
    print("This is the core module. Use the CLI interface to interact with the application.")
