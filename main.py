from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from bami_chassis.application.exceptions.base import ApplicationException
from bami_chassis.infrastructure.config import settings
from bami_chassis.infrastructure.logging.request_logging_middleware import RequestLoggingMiddleware
from bami_chassis.infrastructure.tracing.instrumentation import instrument_app
from bami_chassis.infrastructure.tracing.middleware import TracingMiddleware
from bami_chassis.infrastructure.tracing.tracer import init_tracer
from bami_chassis.interfaces import application_exception_handler, unhandled_exception_handler, \
    validation_error_handler
from bami_chassis.interfaces import router as health_router
from bami_chassis.interfaces.api.metrics_router import router as metrics_router
# from interfaces.api.middlewares.auth_middleware import AuthMiddleware


def create_app():
    app = FastAPI(
        title="Bami Framework",
        debug=settings.debug
    )

    # app.add_middleware(AuthMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(health_router)
    app.include_router(metrics_router)

    # 1. Init global tracer
    init_tracer()

    # 2. Instrument auto instrumentation
    instrument_app(app)

    # 3. Add middleware for inbound request tracing
    app.add_middleware(TracingMiddleware)

    # 4. Register exception handlers
    app.add_exception_handler(ApplicationException, application_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)

    return app

app = create_app()