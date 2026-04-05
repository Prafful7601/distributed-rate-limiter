from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.middleware.rate_limiter import RateLimiterMiddleware
from app.storage.redis_client import redis_client

app = FastAPI()

app.add_middleware(RateLimiterMiddleware)


@app.get("/")
def home():
    return {"message": "Request successful"}


@app.get("/api/data")
def get_data():
    return {"data": "Protected resource"}


@app.get("/stats")
def stats():

    allowed = redis_client.get("allowed_requests") or 0
    blocked = redis_client.get("blocked_requests") or 0

    return {
        "allowed_requests": int(allowed),
        "blocked_requests": int(blocked)
    }


@app.get("/dashboard")
def dashboard():
    return FileResponse("dashboard/index.html")