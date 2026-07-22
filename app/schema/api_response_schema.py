from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from fastapi import Response
from fastapi.responses import JSONResponse

T = TypeVar("T")


# ─── Pydantic Schema (for docs & validation) ───────────────────────────────

class MetaData(BaseModel):
    """Pagination / metadata block."""
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    total: int = Field(default=0, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {"page": 1, "limit": 20, "total": 100}
        }


class APIResponse(BaseModel, Generic[T]):
    """
    Every single response matches this.
    """
    success: bool = Field(..., description="True for success, False for error")
    message: str = Field(..., description="Human-readable status message")
    data: Optional[T] = Field(default=None, description="Payload on success")
    meta: Optional[MetaData] = Field(default=None, description="Pagination info")
    errors: Optional[Any] = Field(default=None, description="Error details on failure")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Users fetched",
                "data": [],
                "meta": {"page": 1, "limit": 20, "total": 100},
                "errors": None
            }
        }


# ─── Builder Functions (what your routes actually call) ─────────────────────

def success_response(
    data: Any = None,
    message: str = "Success",
    meta: Optional[MetaData] = None,
    status_code: int = 200
) -> JSONResponse:
    """
    Use this in EVERY route that succeeds.
    
    Args:
        data: Your actual payload (list, dict, model, whatever)
        message: Human-readable success message
        meta: Pagination metadata (omit if not paginated)
        status_code: HTTP status (usually 200, 201 for created)
    """
    body = {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta.model_dump() if meta else None,
        "errors": None
    }
    return JSONResponse(content=body, status_code=status_code)


def error_response(
    message: str = "An error occurred",
    errors: Any = None,
    status_code: int = 500
) -> JSONResponse:
    """
    Use this manually if needed, but usually the global handler calls this.
    """
    body = {
        "success": False,
        "message": message,
        "data": None,
        "meta": None,
        "errors": errors
    }
    return JSONResponse(content=body, status_code=status_code)


# ─── Decorator (Optional but powerful) ────────────────────────────────────

from functools import wraps
from fastapi import Request

def standard_response(func):
    """
    Decorator that auto-wraps route return values.
    If your route returns raw data, this wraps it.
    If your route already returns a Response, it passes through.
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
        
        # If it's already a Response, don't touch it
        if isinstance(result, Response):
            return result
        
        # If it's a tuple (data, status_code), handle it
        if isinstance(result, tuple) and len(result) == 2:
            data, status_code = result
            return success_response(data=data, status_code=status_code)
        
        # Otherwise wrap the raw data
        return success_response(data=result)
    
    return wrapper