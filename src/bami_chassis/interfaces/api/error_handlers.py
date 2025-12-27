from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from bami_chassis.application.exceptions.base import ApplicationException
from bami_chassis.infrastructure.logging.logger import get_logger

logger = get_logger("bami.error")


async def application_exception_handler(
    request: Request,
    exc: ApplicationException,
):
    logger.warning(
        exc.message,
        extra={
            "error_code": exc.code,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
            }
        },
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "internal_error",
                "message": "Internal server error",
            }
        },
    )


async def validation_error_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "request_validation_error",
                "message": "Invalid request payload",
                "details": exc.errors(),
            }
        },
    )