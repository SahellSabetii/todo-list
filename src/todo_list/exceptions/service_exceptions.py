from .base import BaseException


class ValidationException(BaseException):
    """Raised when validation fails"""
    pass


class BusinessRuleException(BaseException):
    """Raised when business rules are violated"""
    pass
