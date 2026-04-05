import time
from app.storage.redis_client import redis_client


class RedisRateLimiter:

    def __init__(self, capacity=10, refill_rate=1):
        self.capacity = capacity
        self.refill_rate = refill_rate

    def allow_request(self, user_id):

        key = f"rate_limit:{user_id}"

        data = redis_client.hgetall(key)

        now = time.time()

        if not data:

            redis_client.hset(key, mapping={
                "tokens": self.capacity - 1,
                "timestamp": now
            })

            redis_client.expire(key, 60)

            return True

        tokens = float(data["tokens"])
        last = float(data["timestamp"])

        elapsed = now - last

        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)

        if tokens < 1:

            redis_client.hset(key, mapping={
                "tokens": tokens,
                "timestamp": now
            })

            return False

        tokens -= 1

        redis_client.hset(key, mapping={
            "tokens": tokens,
            "timestamp": now
        })

        return True