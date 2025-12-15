from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from application.exceptions.base import ApplicationException
from infrastructure.config.settings import settings
from infrastructure.logging.request_logging_middleware import RequestLoggingMiddleware
from infrastructure.tracing.instrumentation import instrument_app
from infrastructure.tracing.middleware import TracingMiddleware
from infrastructure.tracing.tracer import init_tracer
from interfaces.api.error_handlers import application_exception_handler, unhandled_exception_handler, \
    validation_error_handler
from interfaces.api.metrics_router import router as metrics_router
from interfaces.api.middlewares.auth_middleware import AuthMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    from infrastructure.database.base import Base
    from infrastructure.database.session import engine
    Base.metadata.create_all(bind=engine)

    yield

    # Shutdown
    engine.dispose()


def create_app():
    app = FastAPI(
        title="FastAPI Base Framework",
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    # app.add_middleware(AuthMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
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