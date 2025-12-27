from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest
from typing import Dict
from bami_chassis.infrastructure.config.settings import settings


registry = CollectorRegistry(auto_describe=True)

# === HTTP Metrics ===
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["service", "environment", "method", "path", "status_code"],
    registry=registry,
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["service", "environment", "method", "path"],
    registry=registry,
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests in progress",
    ["service", "environment", "method", "path"],
    registry=registry,
)

HTTP_REQUEST_EXCEPTIONS_TOTAL = Counter(
    "http_request_exceptions_total",
    "Total HTTP exceptions raised",
    ["service", "environment", "method", "path"],
    registry=registry,
)


def get_service_label() -> Dict[str, str]:
    return {
        "service": getattr(settings, "service_name", "bami-service"),
        "environment": settings.environment,
    }


def export_metrics():
    output = generate_latest(registry)
    return CONTENT_TYPE_LATEST, output


def create_counter(name: str, description: str, label_names: list[str]):
    return Counter(name, description, label_names + ["service", "environment"], registry=registry)


def create_gauge(name: str, description: str, label_names: list[str]):
    return Gauge(name, description, label_names + ["service", "environment"], registry=registry)


def create_histogram(name: str, description: str, label_names: list[str]):
    return Histogram(name, description, label_names + ["service", "environment"], registry=registry)