from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.limiter.redis_limiter import RedisRateLimiter
from app.storage.redis_client import redis_client


limiter = RedisRateLimiter(capacity=10, refill_rate=0.1)


EXCLUDED_PATHS = {
    "/dashboard",
    "/stats",
    "/docs",
    "/openapi.json",
    "/favicon.ico"
}


class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path

        # Skip rate limiting for dashboard and stats
        if path in EXCLUDED_PATHS:
            return await call_next(request)

        user_ip = request.client.host

        allowed = limiter.allow_request(user_ip)

        if not allowed:

            redis_client.incr("blocked_requests")

            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        redis_client.incr("allowed_requests")

        response = await call_next(request)

        return response