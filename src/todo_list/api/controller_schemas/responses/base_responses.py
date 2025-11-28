from typing import Optional, Any

from pydantic import BaseModel


class StandardResponse(BaseModel):
    """Standard response format for all API responses"""
    status: str
    message: str
    data: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Operation completed successfully",
                "data": {"id": 1, "name": "example"}
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response format"""
    status: str
    message: str
    error_code: Optional[str] = None
    details: Optional[Any] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "error",
                "message": "Resource not found",
                "error_code": "NOT_FOUND",
                "details": {"resource": "project", "id": 999}
            }
        }
