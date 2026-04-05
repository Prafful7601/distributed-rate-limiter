import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.storage.redis_client import redis_client
from app.limiter.sliding_window_limiter import SlidingWindowLimiter


limiter = SlidingWindowLimiter(limit=10, window=60)


EXCLUDED_PATH_PREFIXES = [
    "/dashboard",
    "/stats",
    "/top_ips",
    "/active_clients",
    "/system",
    "/docs",
    "/openapi.json",
    "/static"
]


class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path

        for prefix in EXCLUDED_PATH_PREFIXES:
            if path.startswith(prefix):
                return await call_next(request)

        user_id = request.client.host

        allowed = limiter.allow_request(user_id)

        redis_client.zincrby("top_ips", 1, user_id)

        redis_client.zadd(
            "request_timestamps",
            {str(time.time()): time.time()}
        )

        if not allowed:

            redis_client.incr("blocked_requests")

            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        redis_client.incr("allowed_requests")

        response = await call_next(request)

        return response