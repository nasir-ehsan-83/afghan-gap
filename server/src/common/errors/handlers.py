import logging
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from common.errors.http_exception import AppBaseException
from common.errors.business_codes import ErrorCode

logger = logging.getLogger("gapgram_app")

def init_error_handlers(app: FastAPI) -> None:
    
    # custom application business exceptions
    @app.exception_handler(AppBaseException)
    async def app_exception_handler(request: Request, exc: AppBaseException):
        return JSONResponse(
            status_code = exc.status_code,
            content = {
                "success": False,
                "error": {
                    "code": exc.error_code.value,
                    "message": exc.message,
                    "details": exc.details
                }
            }
        )

    # input validation exceptions
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        formatted_errors = {}
        for error in exc.errors():
            field_name = " -> ".join(str(loc) for loc in error["loc"] if loc != "body")
            formatted_errors[field_name] = error["msg"]

        return JSONResponse(
            status_code = status.HTTP_422_UNPROCESSABLE_ENTITY,
            content = {
                "success": False,
                "error": {
                    "code": ErrorCode.VALIDATION_ERROR.value,
                    "message": "The provided input data is invalid.",
                    "details": formatted_errors
                }
            }
        )

    # default web server built-in route/http-exceptions
    @app.exception_handler(StarletteHTTPException)
    async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException):
        if exc.status_code == 404:
            code = ErrorCode.ROUTE_NOT_FOUND.value
            message = f"The route {request.method} {request.url.path} does not exist on this server."
        elif exc.status_code == 405:
            code = ErrorCode.METHOD_NOT_ALLOWED.value
            message = "The HTTP method used is not allowed for this endpoint."
        else:
            code = "HTTP_ERROR"
            message = exc.detail

        return JSONResponse(
            status_code = exc.status_code,
            content = {
                "success": False,
                "error": {
                    "code": code,
                    "message": message,
                    "details": {}
                }
            }
        )

    # global fallback handler for uncaught runtime crashes (500 Internal Server Errors)
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # logs full traceback with error context to make backend debugging simple
        logger.error(f"Critical System Crash on {request.method} {request.url.path}: {str(exc)}", exc_info = True)
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content = {
                "success": False,
                "error": {
                    "code": ErrorCode.INTERNAL_SERVER_ERROR.value,
                    "message": "An unexpected internal server error occurred. Please try again later.",
                    "details": {}
                }
            }
        )
