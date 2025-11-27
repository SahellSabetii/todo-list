import os
from typing import List, Optional

from todo_list.repositories.project_repository import ProjectRepository
from todo_list.exceptions import ValidationException, BusinessRuleException


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
        self.max_projects = int(os.getenv('MAX_NUMBER_OF_PROJECTS', 100))
        self.max_project_name_length = int(os.getenv('MAX_PROJECT_NAME_LENGTH', 100))
        self.max_project_description_length = int(os.getenv('MAX_PROJECT_DESCRIPTION_LENGTH', 1000))
    
    def create_project(self, name: str, description: str = None):
        if not name or len(name.strip()) == 0:
            raise ValidationException("Project name cannot be empty")
        
        if len(name) > self.max_project_name_length:
            raise ValidationException(f"Project name cannot exceed {self.max_project_name_length} characters")
        
        if description and len(description) > self.max_project_description_length:
            raise ValidationException(f"Project description cannot exceed {self.max_project_description_length} characters")
        
        all_projects = self.project_repository.get_all()
        if len(all_projects) >= self.max_projects:
            raise BusinessRuleException(f"Cannot create more than {self.max_projects} projects")
        
        return self.project_repository.create(name, description)
    
    def get_project(self, project_id: int):
        return self.project_repository.get_by_id(project_id)
    
    def get_project_by_name(self, name: str):
        return self.project_repository.get_by_name(name)
    
    def get_all_projects(self) -> List:
        return self.project_repository.get_all()
    
    def update_project(self, project_id: int, name: str = None, description: str = None):
        if name and len(name.strip()) == 0:
            raise ValidationException("Project name cannot be empty")
        
        if name and len(name) > self.max_project_name_length:
            raise ValidationException(f"Project name cannot exceed {self.max_project_name_length} characters")
        
        if description and len(description) > self.max_project_description_length:
            raise ValidationException(f"Project description cannot exceed {self.max_project_description_length} characters")
        
        return self.project_repository.update(project_id, name, description)
    
    def delete_project(self, project_id: int):
        project = self.project_repository.get_by_id(project_id)
        if project and project.tasks:
            raise BusinessRuleException("Cannot delete project with existing tasks")
        
        return self.project_repository.delete(project_id)
