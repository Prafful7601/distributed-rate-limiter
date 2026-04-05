# Distributed Rate Limiter API

A distributed rate limiting system built with FastAPI, Redis, and Docker.

## Architecture

Client → FastAPI → Middleware → Redis → Rate Limit Decision

## Features

- Token Bucket rate limiting
- Redis-backed distributed counters
- FastAPI middleware integration
- Docker containerization
- Multi-container architecture with Docker Compose

## Tech Stack

- FastAPI
- Redis
- Python
- Docker
- Docker Compose

## Run Locally

Start the system:

docker compose up --build

API runs at:

http://localhost:8000

## Rate Limiting

- 10 requests allowed
- 1 token refill per second
- Excess requests return HTTP 429

## Project Structure

app/
 ├── limiter/
 │   ├── token_bucket.py
 │   └── redis_limiter.py
 ├── middleware/
 │   └── rate_limiter.py
 ├── storage/
 │   └── redis_client.py
 └── main.py

## Future Improvements

- Sliding window algorithm
- User authentication based limits
- Global distributed limiter using Redis cluster