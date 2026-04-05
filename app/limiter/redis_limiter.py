import time
from app.storage.redis_client import redis_client


class RedisRateLimiter:

    def __init__(self, capacity=10, refill_rate=0.2):
        self.capacity = capacity
        self.refill_rate = refill_rate

    def allow_request(self, user_id):

        key = f"rate_limit:{user_id}"

        script = """
        local key = KEYS[1]

        local capacity = tonumber(ARGV[1])
        local refill_rate = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        local data = redis.call("HMGET", key, "tokens", "timestamp")

        local tokens = tonumber(data[1])
        local timestamp = tonumber(data[2])

        if tokens == nil then
            tokens = capacity
            timestamp = now
        end

        local delta = math.max(0, now - timestamp)
        local refill = delta * refill_rate

        tokens = math.min(capacity, tokens + refill)

        if tokens < 1 then
            redis.call("HMSET", key, "tokens", tokens, "timestamp", now)
            redis.call("EXPIRE", key, 120)
            return 0
        end

        tokens = tokens - 1

        redis.call("HMSET", key, "tokens", tokens, "timestamp", now)
        redis.call("EXPIRE", key, 120)

        return 1
        """

        now = time.time()

        result = redis_client.eval(
            script,
            1,
            key,
            self.capacity,
            self.refill_rate,
            now
        )

        return result == 1