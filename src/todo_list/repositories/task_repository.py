from typing import List, Optional
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import and_

from todo_list.models.task import Task, TaskStatus
from todo_list.models.project import Project
from todo_list.exceptions import NotFoundException


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def create(self, title: str, project_id: int, description: str = None, 
               deadline: datetime = None) -> Task:
        project = self.session.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise NotFoundException(f"Project with id {project_id} not found")
        
        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            deadline=deadline,
            status=TaskStatus.PENDING.value
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
    
    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.session.query(Task).filter(Task.id == task_id).first()
    
    def get_all(self) -> List[Task]:
        return self.session.query(Task).all()
    
    def get_overdue_tasks(self) -> List[Task]:
        return self.session.query(Task).filter(
            and_(
                Task.deadline.isnot(None),
                Task.deadline < datetime.now(),
                Task.status != TaskStatus.DONE.value,
                Task.closed_at.is_(None)
            )
        ).all()
    
    def close_task(self, task_id: int) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found")
        
        task.status = TaskStatus.DONE.value
        task.closed_at = datetime.now()
        self.session.commit()
        return task
    
    def update(self, task_id: int, **kwargs) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            raise NotFoundException(f"Task with id {task_id} not found")
        
        for key, value in kwargs.items():
            if hasattr(task, key) and value is not None:
                setattr(task, key, value)
        
        self.session.commit()
        self.session.refresh(task)
        return task
