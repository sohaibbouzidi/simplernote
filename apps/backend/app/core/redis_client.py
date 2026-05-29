import json
from typing import Any, Optional
from redis import Redis

from app.core.config import settings

redis_client: Optional[Redis] = None


def init_redis() -> Redis:
    global redis_client
    redis_client = Redis.from_url(str(settings.REDIS_URL), decode_responses=True)
    return redis_client


def close_redis():
    global redis_client
    if redis_client:
        redis_client.close()
        redis_client = None


def get_redis() -> Optional[Redis]:
    return redis_client


def cache_get(key: str) -> Optional[Any]:
    r = get_redis()
    if not r:
        return None
    data = r.get(key)
    if data is None:
        return None
    try:
        return json.loads(data)
    except (json.JSONDecodeError, TypeError):
        return None


def cache_set(key: str, value: Any, ttl: int = 300) -> bool:
    r = get_redis()
    if not r:
        return False
    data = json.dumps(value, default=str)
    return r.setex(key, ttl, data)


def cache_delete(key: str) -> bool:
    r = get_redis()
    if not r:
        return False
    return bool(r.delete(key))


def cache_invalidate_pattern(pattern: str) -> int:
    r = get_redis()
    if not r:
        return 0
    keys = r.keys(pattern)
    if keys:
        return r.delete(*keys)
    return 0
