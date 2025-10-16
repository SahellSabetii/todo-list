import os
from typing import Dict, Any

from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for ToDoList application."""
    
    MAX_NUMBER_OF_PROJECTS = int(os.getenv('MAX_NUMBER_OF_PROJECTS', '10'))
    MAX_NUMBER_OF_TASKS_PER_PROJECT = int(os.getenv('MAX_NUMBER_OF_TASKS_PER_PROJECT', '50'))
    MAX_PROJECT_NAME_LENGTH = int(os.getenv('MAX_PROJECT_NAME_LENGTH', '30'))
    MAX_PROJECT_DESCRIPTION_LENGTH = int(os.getenv('MAX_PROJECT_DESCRIPTION_LENGTH', '150'))
    MAX_TASK_TITLE_LENGTH = int(os.getenv('MAX_TASK_TITLE_LENGTH', '30'))
    MAX_TASK_DESCRIPTION_LENGTH = int(os.getenv('MAX_TASK_DESCRIPTION_LENGTH', '150'))
    
    @classmethod
    def get_all_limits(cls) -> Dict[str, Any]:
        """Get all configuration limits."""
        return {
            'max_projects': cls.MAX_NUMBER_OF_PROJECTS,
            'max_tasks_per_project': cls.MAX_NUMBER_OF_TASKS_PER_PROJECT,
            'max_project_name_length': cls.MAX_PROJECT_NAME_LENGTH,
            'max_project_description_length': cls.MAX_PROJECT_DESCRIPTION_LENGTH,
            'max_task_title_length': cls.MAX_TASK_TITLE_LENGTH,
            'max_task_description_length': cls.MAX_TASK_DESCRIPTION_LENGTH,
        }
