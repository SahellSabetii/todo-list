class ToDoListError(Exception):
    """Base exception for ToDoList application."""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class ValidationError(ToDoListError):
    """Raised when validation fails."""
    pass


class DuplicateProjectError(ToDoListError):
    """Raised when trying to create a project with duplicate name."""
    pass


class ProjectNotFoundError(ToDoListError):
    """Raised when project is not found."""
    pass


class TaskNotFoundError(ToDoListError):
    """Raised when task is not found."""
    pass


class LimitExceededError(ToDoListError):
    """Raised when maximum number of projects or tasks is exceeded."""
    pass


class InvalidStatusError(ToDoListError):
    """Raised when an invalid task status is provided."""
    pass
