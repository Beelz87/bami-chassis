from src.infrastructure.config.settings import settings


def resolve_service_name(alias: str) -> str:
    try:
        return settings.service_name_map[alias]
    except KeyError:
        raise ValueError(
            f"Alias '{alias}' not found in SERVICE_NAME_MAP. "
            f"Available: {list(settings.service_name_map.keys())}"
        )
