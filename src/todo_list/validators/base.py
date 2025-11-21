from datetime import datetime
from typing import Optional

from ..exceptions.base import ValidationError
from ..config import Config


def validate_project_name(name: str) -> None:
    """Validate project name."""
    if not name or not name.strip():
        raise ValidationError("Project name cannot be empty")
    
    if len(name) > Config.MAX_PROJECT_NAME_LENGTH:
        raise ValidationError(
            f"Project name cannot exceed {Config.MAX_PROJECT_NAME_LENGTH} characters"
        )


def validate_project_description(description: str) -> None:
    """Validate project description."""
    if not description or not description.strip():
        raise ValidationError("Project description cannot be empty")
    
    if len(description) > Config.MAX_PROJECT_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"Project description cannot exceed {Config.MAX_PROJECT_DESCRIPTION_LENGTH} characters"
        )


def validate_task_title(title: str) -> None:
    """Validate task title."""
    if not title or not title.strip():
        raise ValidationError("Task title cannot be empty")
    
    if len(title) > Config.MAX_TASK_TITLE_LENGTH:
        raise ValidationError(
            f"Task title cannot exceed {Config.MAX_TASK_TITLE_LENGTH} characters"
        )


def validate_task_description(description: str) -> None:
    """Validate task description."""
    if not description or not description.strip():
        raise ValidationError("Task description cannot be empty")
    
    if len(description) > Config.MAX_TASK_DESCRIPTION_LENGTH:
        raise ValidationError(
            f"Task description cannot exceed {Config.MAX_TASK_DESCRIPTION_LENGTH} characters"
        )


def validate_deadline(deadline: Optional[datetime]) -> None:
    """Validate task deadline."""
    if deadline and deadline < datetime.now():
        raise ValidationError("Deadline cannot be in the past")
