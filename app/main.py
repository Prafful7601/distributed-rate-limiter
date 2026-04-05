import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

from app.middleware.rate_limiter import RateLimiterMiddleware
from app.storage.redis_client import redis_client


app = FastAPI()

app.add_middleware(RateLimiterMiddleware)


@app.get("/")
def home():

    return {
        "service": "Distributed Rate Limiter",
        "status": "running"
    }


@app.get("/api/data")
def api_data():

    return {
        "message": "Request successful"
    }


@app.get("/stats")
def stats():

    allowed = int(redis_client.get("allowed_requests") or 0)
    blocked = int(redis_client.get("blocked_requests") or 0)

    now = time.time()
    window = now - 60

    redis_client.zremrangebyscore(
        "request_timestamps",
        0,
        window
    )

    rpm = redis_client.zcard("request_timestamps")

    return {
        "allowed": allowed,
        "blocked": blocked,
        "total": allowed + blocked,
        "requests_per_minute": rpm
    }


@app.get("/top_ips")
def top_ips():

    data = redis_client.zrevrange(
        "top_ips",
        0,
        4,
        withscores=True
    )

    return [
        {"ip": ip, "requests": int(score)}
        for ip, score in data
    ]


@app.get("/active_clients")
def active_clients():

    count = redis_client.zcard("top_ips")

    return {"active_clients": count}


@app.get("/system")
def system():

    return {
        "default_algorithm": "Token Bucket",
        "capacity": 10,
        "refill_rate": 0.2,
        "backend": "Redis",
        "framework": "FastAPI"
    }


@app.get("/dashboard")
def dashboard():

    path = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"

    return FileResponse(path)