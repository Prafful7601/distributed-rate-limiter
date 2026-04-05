from app.storage.redis_client import redis_client


class FixedWindowLimiter:

    def __init__(self, limit=10):
        self.limit = limit

    def allow_request(self, user_id):

        key = f"fw:{user_id}"

        count = redis_client.get(key)

        if count is None:
            redis_client.set(key, 1, ex=60)
            return True

        count = int(count)

        if count >= self.limit:
            return False

        redis_client.incr(key)

        return True