from typing import List, Optional

from todo_list.repositories.project_repository import ProjectRepository
from todo_list.exceptions import ValidationException, BusinessRuleException


class ProjectService:
    def __init__(self, project_repository: ProjectRepository):
        self.project_repository = project_repository
    
    def create_project(self, name: str, description: str = None):
        if not name or len(name.strip()) == 0:
            raise ValidationException("Project name cannot be empty")
        
        if len(name) > 100:
            raise ValidationException("Project name cannot exceed 100 characters")
        
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
        
        if name and len(name) > 100:
            raise ValidationException("Project name cannot exceed 100 characters")
        
        return self.project_repository.update(project_id, name, description)
    
    def delete_project(self, project_id: int):
        project = self.project_repository.get_by_id(project_id)
        if project and project.tasks:
            raise BusinessRuleException("Cannot delete project with existing tasks")
        
        return self.project_repository.delete(project_id)
