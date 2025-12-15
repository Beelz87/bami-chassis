from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
import json
from typing import Dict


class Settings(BaseSettings):
    # --- Environment ---
    service_name: str = "bami-service"
    environment: str = "dev"
    log_level: str = "debug"

    # --- Security ---
    public_key: str = ""
    auth_audience: str = "bami-auth-service"
    token_leeway_seconds: int = 30

    # --- Databases ---
    db_url_postgres: str = "localhost:5432"

    # --- Redis ---
    redis_url: str = "redis://localhost:6379"

    # --- Kafka ---
    kafka_bootstrap_servers: str = "localhost:9092"

    # --- Service Registry Mapping ---
    # JSON string format: {"user": "user-service", "order": "order-service"}
    service_name_map: Dict[str, str] = {}

    # --- Pydantic Settings Config ---
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
        env_nested_delimiter="__"
    )

    # --- Validators ---
    @field_validator("service_name_map", mode="before")
    def parse_service_name_map(cls, value):
        if value is None:
            return {}
        if isinstance(value, dict):
            return value
        if isinstance(value, str):
            try:
                return json.loads(value)
            except Exception:
                raise ValueError("SERVICE_NAME_MAP must be valid JSON string")
        raise ValueError("SERVICE_NAME_MAP must be dict or JSON string")

    # --- Tracing ---
    otlp_endpoint: str = "http://opentelemetry-collector:4318/v1/traces"
    trace_debug_console: bool = False


# Instance settings global
settings = Settings()
