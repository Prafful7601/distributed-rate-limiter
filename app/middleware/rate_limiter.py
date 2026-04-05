from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.limiter.redis_limiter import RedisRateLimiter

limiter = RedisRateLimiter(capacity=10, refill_rate=1)

class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        user_ip = request.client.host

        if not limiter.allow_request(user_ip):
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        response = await call_next(request)
        return response