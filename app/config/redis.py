import redis.asyncio as redis

from app.settings.redis import redis_settings


redis_client = None


async def init_redis():
    global redis_client

    redis_client = redis.from_url(
        redis_settings.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )

    await redis_client.ping()


async def close_redis():
    global redis_client

    if redis_client:
        await redis_client.close()