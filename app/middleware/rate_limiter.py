import time

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse

from app.limiter.redis_lua_limiter import RedisLuaLimiter
from app.storage.redis_client import redis_client
from app.services.api_key_service import get_api_key_config
from app.utils.logger import logger


limiter = RedisLuaLimiter()


EXCLUDED_PATH_PREFIXES = [
    "/dashboard",
    "/stats",
    "/top_ips",
    "/active_clients",
    "/system",
    "/health",
    "/docs",
    "/openapi.json",
    "/static"
]


def get_client_ip(request):

    forwarded = request.headers.get("x-forwarded-for")

    if forwarded:
        return forwarded.split(",")[0].strip()

    return request.client.host


class RateLimiterMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request, call_next):

        path = request.url.path

        for prefix in EXCLUDED_PATH_PREFIXES:
            if path.startswith(prefix):
                return await call_next(request)

        start = time.time()

        api_key = request.query_params.get("api_key")

        if api_key:
            user_id = api_key
        else:
            user_id = get_client_ip(request)

        config = get_api_key_config(api_key)

        limit = config["limit"]
        window = config["window"]

        allowed, current = limiter.allow_request(
            user_id,
            limit,
            window
        )

        redis_client.zincrby("top_ips", 1, user_id)

        redis_client.zadd(
            "request_timestamps",
            {str(time.time()): time.time()}
        )

        if not allowed:

            redis_client.incr("blocked_requests")

            logger.warning(f"BLOCKED {user_id}")

            return JSONResponse(
                status_code=429,
                content={"error": "Rate limit exceeded"}
            )

        redis_client.incr("allowed_requests")

        response = await call_next(request)

        latency = round((time.time() - start) * 1000, 2)

        logger.info(f"{user_id} allowed latency={latency}ms")

        response.headers["X-RateLimit-Limit"] = str(limit)
        response.headers["X-RateLimit-Remaining"] = str(limit - current)
        response.headers["X-RateLimit-Window"] = str(window)

        return response