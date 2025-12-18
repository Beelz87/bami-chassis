from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.infrastructure.logging.correlation_id import set_correlation_id
from src.infrastructure.logging.logger import get_logger

logger = get_logger("bami.request")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        correlation_id = (
            request.headers.get("X-Correlation-ID") or
            request.headers.get("X-Request-ID") or
            set_correlation_id()
        )

        set_correlation_id(correlation_id)

        logger.info(
            "Incoming request",
            extra={
                "method": request.method,
                "path": request.url.path,
                "client": request.client.host,
                "correlation_id": correlation_id,
            }
        )

        response = await call_next(request)
        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(
            "Response sent",
            extra={
                "status_code": response.status_code,
                "correlation_id": correlation_id,
            }
        )

        return response
