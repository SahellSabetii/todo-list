from typing import List, Optional
from datetime import datetime

from todo_list.repositories.task_repository import TaskRepository
from todo_list.exceptions import ValidationException


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def create_task(self, title: str, project_id: int, description: str = None, 
                   deadline: datetime = None):
        if not title or len(title.strip()) == 0:
            raise ValidationException("Task title cannot be empty")
        
        if len(title) > 200:
            raise ValidationException("Task title cannot exceed 200 characters")
        
        if deadline and deadline < datetime.now():
            raise ValidationException("Deadline cannot be in the past")
        
        return self.task_repository.create(title, project_id, description, deadline)
    
    def get_task(self, task_id: int):
        return self.task_repository.get_by_id(task_id)
    
    def get_tasks_by_project(self, project_id: int) -> List:
        return self.task_repository.get_by_project(project_id)
    
    def get_all_tasks(self) -> List:
        return self.task_repository.get_all()
    
    def get_overdue_tasks(self) -> List:
        return self.task_repository.get_overdue_tasks()
    
    def update_task(self, task_id: int, **kwargs):
        if 'title' in kwargs and (not kwargs['title'] or len(kwargs['title'].strip()) == 0):
            raise ValidationException("Task title cannot be empty")
        
        if 'title' in kwargs and len(kwargs['title']) > 200:
            raise ValidationException("Task title cannot exceed 200 characters")
        
        if 'deadline' in kwargs and kwargs['deadline'] and kwargs['deadline'] < datetime.now():
            raise ValidationException("Deadline cannot be in the past")
        
        return self.task_repository.update(task_id, **kwargs)
    
    def delete_task(self, task_id: int):
        return self.task_repository.delete(task_id)
    
    def close_task(self, task_id: int):
        return self.task_repository.close_task(task_id)
    
    def auto_close_overdue_tasks(self) -> int:
        overdue_tasks = self.get_overdue_tasks()
        closed_count = 0
        
        for task in overdue_tasks:
            self.close_task(task.id)
            closed_count += 1
        
        return closed_count
