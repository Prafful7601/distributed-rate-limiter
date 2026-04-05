import time
from app.storage.redis_client import redis_client

class RedisRateLimiter:

    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate

    def allow_request(self, user_id):

        key = f"rate_limit:{user_id}"

        tokens = redis_client.get(key)

        if tokens is None:
            redis_client.set(key, self.capacity - 1, ex=60)
            return True

        tokens = int(tokens)

        if tokens <= 0:
            return False

        redis_client.decr(key)
        return True