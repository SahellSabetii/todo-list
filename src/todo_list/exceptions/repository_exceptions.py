from .base import BaseException


class NotFoundException(BaseException):
    """Raised when a resource is not found"""
    pass


class DuplicateEntryException(BaseException):
    """Raised when trying to create a duplicate entry"""
    pass
