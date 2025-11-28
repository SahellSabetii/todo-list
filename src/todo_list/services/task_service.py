import os
from typing import List, Optional
from datetime import datetime

from todo_list.repositories.task_repository import TaskRepository
from todo_list.exceptions import ValidationException


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
        self.max_tasks_per_project = int(os.getenv('MAX_NUMBER_OF_TASKS_PER_PROJECT', 100))
        self.max_task_title_length = int(os.getenv('MAX_TASK_TITLE_LENGTH', 200))
        self.max_task_description_length = int(os.getenv('MAX_TASK_DESCRIPTION_LENGTH', 2000))
    
    def create_task(self, title: str, project_id: int, description: str = None, 
                   deadline: datetime = None):
        if not title or len(title.strip()) == 0:
            raise ValidationException("Task title cannot be empty")
        
        if len(title) > self.max_task_title_length:
            raise ValidationException(f"Task title cannot exceed {self.max_task_title_length} characters")
        
        if description and len(description) > self.max_task_description_length:
            raise ValidationException(f"Task description cannot exceed {self.max_task_description_length} characters")
        
        if deadline and deadline < datetime.now():
            raise ValidationException("Deadline cannot be in the past")
        
        project_tasks = self.task_repository.get_by_project(project_id)
        if len(project_tasks) >= self.max_tasks_per_project:
            raise ValidationException(f"Cannot create more than {self.max_tasks_per_project} tasks per project")
        
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
        if 'title' in kwargs:
            if not kwargs['title'] or len(kwargs['title'].strip()) == 0:
                raise ValidationException("Task title cannot be empty")
            if len(kwargs['title']) > self.max_task_title_length:
                raise ValidationException(f"Task title cannot exceed {self.max_task_title_length} characters")
        
        if 'description' in kwargs and kwargs['description'] and len(kwargs['description']) > self.max_task_description_length:
            raise ValidationException(f"Task description cannot exceed {self.max_task_description_length} characters")
        
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
