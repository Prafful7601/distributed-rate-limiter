from app.storage.redis_client import redis_client
import time


class SlidingWindowLimiter:

    def __init__(self, limit=10, window=60):
        self.limit = limit
        self.window = window

    def allow_request(self, user_id):

        key = f"rate:{user_id}"

        now = time.time()
        window_start = now - self.window

        redis_client.zremrangebyscore(key, 0, window_start)

        count = redis_client.zcard(key)

        if count >= self.limit:
            return False

        redis_client.zadd(key, {str(now): now})
        redis_client.expire(key, self.window)

        return True