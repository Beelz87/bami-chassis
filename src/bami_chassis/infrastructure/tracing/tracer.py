from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

from bami_chassis.infrastructure.config.settings import settings


def init_tracer():
    resource = Resource.create({
        "service.name": settings.service_name,
        "deployment.environment": settings.environment,
    })

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # OTLP exporter (send to Collector / Tempo / Jaeger)
    otlp_exporter = OTLPSpanExporter(endpoint=settings.otlp_endpoint)

    processor = BatchSpanProcessor(otlp_exporter)
    provider.add_span_processor(processor)

    # Optional: debug exporter
    if settings.trace_debug_console:
        provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    return trace.get_tracer(settings.service_name)
