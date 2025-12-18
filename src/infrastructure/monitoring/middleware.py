import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.infrastructure.monitoring.metrics import (
    HTTP_REQUESTS_TOTAL,
    HTTP_REQUEST_DURATION_SECONDS,
    HTTP_REQUESTS_IN_PROGRESS,
    HTTP_REQUEST_EXCEPTIONS_TOTAL,
    get_service_label,
)


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()

        path = request.url.path
        method = request.method.upper()

        base_labels = get_service_label()
        labels = {
            "service": base_labels["service"],
            "environment": base_labels["environment"],
            "method": method,
            "path": path,
        }

        HTTP_REQUESTS_IN_PROGRESS.labels(**labels).inc()

        try:
            response: Response = await call_next(request)
            status_code = response.status_code

        except Exception:
            HTTP_REQUEST_EXCEPTIONS_TOTAL.labels(**labels).inc()
            HTTP_REQUESTS_IN_PROGRESS.labels(**labels).dec()
            raise

        duration = time.perf_counter() - start_time

        HTTP_REQUEST_DURATION_SECONDS.labels(**labels).observe(duration)

        HTTP_REQUESTS_TOTAL.labels(
            service=labels["service"],
            environment=labels["environment"],
            method=method,
            path=path,
            status_code=status_code,
        ).inc()

        HTTP_REQUESTS_IN_PROGRESS.labels(**labels).dec()

        return response
