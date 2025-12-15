import httpx

from infrastructure.circuit_breaker.breaker import circuit_breaker


@circuit_breaker
def http_get(url: str):
    try:
        response = httpx.get(url, timeout=3)
        response.raise_for_status()
        return response.json()
    except Exception as exc:
        raise exc
