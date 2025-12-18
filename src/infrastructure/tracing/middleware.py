from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from opentelemetry import trace
from opentelemetry.trace import SpanKind

tracer = trace.get_tracer(__name__)


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        path = request.url.path
        method = request.method

        with tracer.start_as_current_span(
            name=f"HTTP {method} {path}",
            kind=SpanKind.SERVER
        ) as span:

            span.set_attribute("http.method", method)
            span.set_attribute("http.url", str(request.url))
            span.set_attribute("client.ip", request.client.host)

            response = await call_next(request)

            span.set_attribute("http.status_code", response.status_code)

            return response
