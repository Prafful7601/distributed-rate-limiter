from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

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
def protected_api():
    return {"data": "Protected resource"}


@app.get("/stats")
def stats():

    allowed = redis_client.get("allowed_requests") or 0
    blocked = redis_client.get("blocked_requests") or 0

    return {
        "allowed": int(allowed),
        "blocked": int(blocked),
        "total": int(allowed) + int(blocked)
    }


@app.get("/system")
def system_info():

    return {
        "algorithm": "Token Bucket",
        "capacity": 10,
        "refill_rate": 0.1,
        "backend": "Redis",
        "framework": "FastAPI"
    }


@app.get("/dashboard")
def dashboard():

    dashboard_path = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"

    return FileResponse(dashboard_path)