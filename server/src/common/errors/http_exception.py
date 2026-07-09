from fastapi import status
from common.errors.business_codes import ErrorCode

class AppBaseException(Exception):
    def __init__(self, message: str, status_code: int, error_code: ErrorCode, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class NotFoundException(AppBaseException):
    def __init__(self, message: str = "Requested resource was not found.", error_code: ErrorCode = ErrorCode.ROUTE_NOT_FOUND):
        super().__init__(message, status.HTTP_404_NOT_FOUND, error_code)

class BadRequestException(AppBaseException):
    def __init__(self, message: str, error_code: ErrorCode):
        super().__init__(message, status.HTTP_400_BAD_REQUEST, error_code)

class UnauthorizedException(AppBaseException):
    def __init__(self, message: str = "Unauthorized access. Please log in first.", error_code: ErrorCode = ErrorCode.UNAUTHORIZED):
        super().__init__(message, status.HTTP_401_UNAUTHORIZED, error_code)

class ForbiddenException(AppBaseException):
    def __init__(self, message: str = "You do not have permission to perform this action.", error_code: ErrorCode = ErrorCode.FORBIDDEN):
        super().__init__(message, status.HTTP_403_FORBIDDEN, error_code)

class ConflictException(AppBaseException):
    def __init__(self, message: str, error_code: ErrorCode):
        super().__init__(message, status.HTTP_409_CONFLICT, error_code)
