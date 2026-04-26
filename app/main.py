import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.middleware.rate_limiter import RateLimiterMiddleware
from app.storage.redis_client import redis_client


app = FastAPI(title="Distributed Rate Limiter")

app.add_middleware(RateLimiterMiddleware)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
    <head>
        <title>Distributed Rate Limiter</title>
        <style>
        body{
        font-family:Arial;
        background:#0f172a;
        color:white;
        padding:40px
        }
        a{
        color:#38bdf8;
        text-decoration:none
        }
        </style>
    </head>

    <body>

    <h1>Distributed Rate Limiter</h1>

    <p>Production style API rate limiter built with FastAPI and Redis.</p>

    <h3>Navigation</h3>

    <ul>
        <li><a href="/api/data">Test API Endpoint</a></li>
        <li><a href="/dashboard">Monitoring Dashboard</a></li>
        <li><a href="/docs">Swagger API Docs</a></li>
    </ul>

    </body>
    </html>
    """


@app.get("/api/data")
def api_data():

    return {"message": "Request successful"}


@app.get("/stats")
def stats():

    allowed = int(redis_client.get("allowed_requests") or 0)
    blocked = int(redis_client.get("blocked_requests") or 0)

    now = time.time()
    window = now - 60

    redis_client.zremrangebyscore("request_timestamps", 0, window)

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

    redis_client.ping()

    return {
        "redis": "connected",
        "framework": "FastAPI",
        "rate_limiter": "Redis Lua Script",
        "deployment": "Render"
    }


@app.get("/health")
def health():

    return {"status": "healthy"}


@app.get("/dashboard")
def dashboard():

    path = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"

    return FileResponse(path)