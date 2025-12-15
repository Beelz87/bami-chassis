import logging
import json
import sys
from datetime import datetime
from typing import Any, Dict
from infrastructure.config.settings import settings
from infrastructure.logging.correlation_id import get_correlation_id


class JsonFormatter(logging.Formatter):

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "service": settings.service_name if hasattr(settings, "service_name") else "bami-service",
            "environment": settings.environment,
            "correlation_id": get_correlation_id(),
        }

        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Allow extra fields
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_entry.update(record.extra)

        return json.dumps(log_entry)


def get_logger(name: str = "bami") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(settings.log_level.upper())

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)

    logger.propagate = False  # tránh duplicate logs
    return logger
