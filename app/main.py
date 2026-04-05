from fastapi import FastAPI
from app.middleware.rate_limiter import RateLimiterMiddleware

app = FastAPI()

# Add middleware
app.add_middleware(RateLimiterMiddleware)


@app.get("/")
def home():
    return {"message": "Request successful"}