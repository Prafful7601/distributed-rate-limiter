import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.middleware.rate_limiter import RateLimiterMiddleware
from app.storage.redis_client import redis_client


app = FastAPI()

app.add_middleware(RateLimiterMiddleware)

# serve css/js files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
    <head>
        <title>Distributed Rate Limiter</title>
    </head>

    <body style="font-family:Arial;padding:40px">

    <h1>Distributed Rate Limiter</h1>

    <p>Production style distributed rate limiting system.</p>

    <h3>Navigation</h3>

    <ul>
        <li><a href="/api/data">Test API</a></li>
        <li><a href="/dashboard">Monitoring Dashboard</a></li>
        <li><a href="/docs">API Docs</a></li>
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


@app.get("/dashboard")
def dashboard():

    path = Path(__file__).resolve().parent.parent / "dashboard" / "index.html"

    return FileResponse(path)