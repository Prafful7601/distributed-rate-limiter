import time
from app.storage.redis_client import redis_client


LUA_SCRIPT = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

redis.call('ZREMRANGEBYSCORE', key, 0, now - window)

local count = redis.call('ZCARD', key)

if count >= limit then
    return {0, count}
end

redis.call('ZADD', key, now, now)
redis.call('EXPIRE', key, window)

return {1, count + 1}
"""


class RedisLuaLimiter:

    def __init__(self):

        self.script = redis_client.register_script(LUA_SCRIPT)

    def allow_request(self, user_id, limit, window):

        key = f"rate:{user_id}"

        now = time.time()

        result = self.script(
            keys=[key],
            args=[limit, window, now]
        )

        allowed = result[0]
        current = result[1]

        return allowed == 1, current