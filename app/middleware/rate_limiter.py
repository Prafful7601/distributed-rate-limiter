from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.limiter.token_bucket import TokenBucket

buckets = {}

def get_bucket(user_id):
    if user_id not in buckets:
        buckets[user_id] = TokenBucket(capacity=5, refill_rate=1)
    return buckets[user_id]


class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        user_ip = request.client.host
        bucket = get_bucket(user_ip)

        if not bucket.allow_request():
            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        response = await call_next(request)
        return response