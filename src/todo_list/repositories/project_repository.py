from typing import List, Optional

from sqlalchemy.orm import Session

from todo_list.models.project import Project
from todo_list.exceptions import NotFoundException, DuplicateEntryException


class ProjectRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, name: str, description: str = None) -> Project:
        if self.get_by_name(name):
            raise DuplicateEntryException(f"Project with name '{name}' already exists")
        
        project = Project(name=name, description=description)
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)
        return project
    
    def get_by_id(self, project_id: int) -> Optional[Project]:
        return self.session.query(Project).filter(Project.id == project_id).first()
    
    def get_by_name(self, name: str) -> Optional[Project]:
        return self.session.query(Project).filter(Project.name == name).first()
    
    def get_all(self) -> List[Project]:
        return self.session.query(Project).all()
    
    def update(self, project_id: int, name: str = None, description: str = None) -> Optional[Project]:
        project = self.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        if name and name != project.name:
            if self.get_by_name(name):
                raise DuplicateEntryException(f"Project with name '{name}' already exists")
            project.name = name
        
        if description is not None:
            project.description = description
        
        self.session.commit()
        self.session.refresh(project)
        return project
    
    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        self.session.delete(project)
        self.session.commit()
        return True
