import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.storage.redis_client import redis_client
from app.limiter.redis_limiter import RedisRateLimiter
from app.limiter.fixed_window_limiter import FixedWindowLimiter
from app.limiter.sliding_window_limiter import SlidingWindowLimiter


token_limiter = RedisRateLimiter(capacity=10, refill_rate=0.2)
fixed_limiter = FixedWindowLimiter(limit=10)
sliding_limiter = SlidingWindowLimiter(limit=10, window=60)


EXCLUDED_PATHS = {
    "/dashboard",
    "/stats",
    "/system",
    "/top_ips",
    "/docs",
    "/openapi.json"
}


class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path

        if path in EXCLUDED_PATHS:
            return await call_next(request)

        # identify client
        api_key = request.query_params.get("api_key")

        if api_key:
            user_id = f"key:{api_key}"
        else:
            user_id = request.client.host

        # choose algorithm
        algorithm = request.query_params.get("algorithm", "token")

        if algorithm == "fixed":
            allowed = fixed_limiter.allow_request(user_id)

        elif algorithm == "sliding":
            allowed = sliding_limiter.allow_request(user_id)

        else:
            allowed = token_limiter.allow_request(user_id)

        # analytics
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