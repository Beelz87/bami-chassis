import redis.asyncio as redis
from bami_chassis.infrastructure.config.settings import settings

_redis_client = None

async def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = await redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10
        )
    return _redis_client

async def close_redis():
    global _redis_client
    if _redis_client:
        await _redis_client.close()
