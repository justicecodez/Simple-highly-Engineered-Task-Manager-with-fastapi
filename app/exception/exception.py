from fastapi import status

class AppExceptions(Exception):
    def __init__(self, message:str="An error occured", status_code:int=status.HTTP_500_INTERNAL_SERVER_ERROR, errors:list|dict|None=None):
        self.message=message
        self.status_code=status_code
        self.errors=errors
        super().__init__(self.message)

class NotFoundException(AppExceptions):
    """404 - Resource doesn't exist."""
    def __init__(self, message: str = "Resource not found", errors=None):
        super().__init__(message, status.HTTP_404_NOT_FOUND, errors)


class ValidationException(AppExceptions):
    """422 - Bad input data."""
    def __init__(self, message: str = "Validation failed", errors=None):
        super().__init__(message, status.HTTP_422_UNPROCESSABLE_ENTITY, errors)


class UnauthorizedException(AppExceptions):
    """401 - Not authenticated."""
    def __init__(self, message: str = "Authentication required", errors=None):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, errors)


class ForbiddenException(AppExceptions):
    """403 - No permission."""
    def __init__(self, message: str = "Access denied", errors=None):
        super().__init__(message, status.HTTP_403_FORBIDDEN, errors)


class ConflictException(AppExceptions):
    """409 - Resource conflict (e.g., duplicate email)."""
    def __init__(self, message: str = "Resource conflict", errors=None):
        super().__init__(message, status.HTTP_409_CONFLICT, errors)


class BadRequestException(AppExceptions):
    """400 - Generic bad request."""
    def __init__(self, message: str = "Bad request", errors=None):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, errors)