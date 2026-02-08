from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom handler for HTTP exceptions
    """
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": exc.status_code}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom handler for validation exceptions
    """
    logger.error(f"Validation Exception: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "error_code": 422
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Custom handler for general exceptions
    """
    error_msg = str(exc)
    logger.error(f"General Exception: {error_msg}", exc_info=True)
    
    # Handle specific bcrypt password length error
    if "password cannot be longer than 72 bytes" in error_msg:
        return JSONResponse(
            status_code=400,
            content={
                "detail": "Password exceeds maximum length of 72 bytes. Please use a shorter password.",
                "error_code": 400
            }
        )
    
    # Print the full traceback to see the actual error
    import traceback
    print(f"Full traceback for request {request.method} {request.url}:")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error_code": 500
        }
    )