# core/handlers.py

from fastapi.responses import JSONResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError

from app.exception.exception import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException
):

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
            "meta": exc.meta,
            "errors": exc.errors
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):

    formatted = {}

    for err in exc.errors():
        field = ".".join(str(x) for x in err["loc"][1:])
        formatted.setdefault(field, []).append(err["msg"])

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "data": None,
            "meta": None,
            "errors": formatted
        }
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception
):

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "data": None,
            "meta": None,
            "errors": {
                "detail": str(exc)
            }
        }
    )