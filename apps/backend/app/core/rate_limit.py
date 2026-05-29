from fastapi import Depends, HTTPException, Request, Response, status
from app.core.redis_client import get_redis


def rate_limit(max_requests: int = 60, window_seconds: int = 60):
    async def dependency(request: Request, response: Response):
        r = get_redis()
        if not r:
            return

        client_key = request.client.host if request.client else "unknown"
        auth_header = request.headers.get("authorization", "")
        token_key = auth_header.replace("Bearer ", "")[:20] if auth_header.startswith("Bearer") else "anon"
        rate_key = f"ratelimit:{token_key}:{client_key}"

        current = r.get(rate_key)
        if current is None:
            r.setex(rate_key, window_seconds, 1)
            remaining = max_requests - 1
        elif int(current) >= max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded. Max {max_requests} requests per {window_seconds}s",
            )
        else:
            r.incr(rate_key)
            remaining = max_requests - int(current) - 1

        response.headers["X-RateLimit-Limit"] = str(max_requests)
        response.headers["X-RateLimit-Remaining"] = str(max(remaining, 0))
        response.headers["X-RateLimit-Reset"] = str(window_seconds)

    return dependency
