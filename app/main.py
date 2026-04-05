from fastapi import FastAPI, Request
from app.limiter.token_bucket import TokenBucket

app = FastAPI()

buckets = {}

def get_bucket(user_id):
    if user_id not in buckets:
        buckets[user_id] = TokenBucket(capacity=5, refill_rate=1)
    return buckets[user_id]

@app.get("/")
def home(request: Request):

    user_ip = request.client.host
    bucket = get_bucket(user_ip)

    if not bucket.allow_request():
        return {"error": "Rate limit exceeded"}

    return {"message": "Request successful", "user": user_ip}