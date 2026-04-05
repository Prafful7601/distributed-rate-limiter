# Distributed Rate Limiter

This project implements a **distributed API rate limiting system** designed to protect backend services from excessive traffic, abuse, and denial-of-service scenarios.

The system enforces request quotas across clients using **Redis-backed distributed algorithms**, ensuring consistent rate limits even when the API runs across multiple server instances.

It includes:

- Multiple rate limiting algorithms
- Redis-based distributed state management
- Atomic Lua scripts to eliminate race conditions
- Monitoring dashboard with traffic analytics
- Deployment-ready architecture

---

# Live Deployment

- API Service

https://distributed-rate-limiter-a7yr.onrender.com/

- Monitoring Dashboard

https://distributed-rate-limiter-a7yr.onrender.com/dashboard

- Repository

https://github.com/Prafful7601/distributed-rate-limiter

---

# System Architecture

The system uses **FastAPI middleware to intercept requests** and enforce rate limits using Redis as a shared state store.

Client Requests
      │
      ▼
FastAPI Middleware
      │
      ▼
Rate Limiting Engine
(Token Bucket / Sliding Window / Fixed Window)
      │
      ▼
Redis (Central State Store)
      │
      ▼
Analytics & Monitoring APIs
      │
      ▼
Dashboard UI


Redis allows **multiple API servers to share rate limit state**, enabling horizontal scaling.

---

# Monitoring Dashboard

The project includes a **real-time monitoring dashboard** that visualizes API traffic and rate limiting behavior.

Dashboard URL
- https://distributed-rate-limiter-a7yr.onrender.com/dashboard


Dashboard displays:

- Allowed Requests
- Blocked Requests
- Total Requests
- Requests Per Minute
- Active Clients
- Top IP Addresses
- Traffic Graph


---

# Dashboard Preview

![Dashboard Image 1](image.png)
![Dashboard Image 2](image-1.png)

---

## Features

• Distributed rate limiting across multiple API instances  
• Token Bucket, Fixed Window, and Sliding Window algorithms  
• Redis-backed request tracking  
• Atomic Lua execution to prevent race conditions  
• API key based rate limiting support  
• Real-time traffic analytics dashboard  
• Top client IP tracking  
• Requests per minute monitoring  
• Dockerized deployment  
• Live cloud deployment on Render

---

## Atomic Rate Limiting with Redis Lua

To ensure correct behavior under high concurrency, rate limiting operations are executed using **Redis Lua scripts**.

Advantages:

- Atomic execution
- Eliminates race conditions
- Ensures consistent request counts
- Works correctly in distributed environments

Lua scripts allow the limiter to:

1. Read request history
2. Update counters
3. Apply rate limiting logic

All in a **single atomic Redis operation**.

---

## Multiple Rate Limiting Algorithms

The system supports several commonly used algorithms.

### Token Bucket

- Allows bursts of traffic
- Tokens refill gradually
- Smooth traffic shaping

Example configuration:
capacity = 10 tokens
refill_rate = 0.2 tokens/sec

---

### Fixed Window
Counts requests within a time window
Resets after expiration

---

### Sliding Window
More accurate rate limiting
Prevents burst spikes at window edges

Algorithms can be switched dynamically.

Example:
/api/data?algorithm=token
/api/data?algorithm=fixed
/api/data?algorithm=sliding

---

# API Key Based Rate Limiting

Clients can use API keys to receive independent rate limits.

Example request:
/api/data?api_key=user1

Each API key has its own request quota.

---

# API Usage

Basic request

GET /api/data

Example response:
{
"message": "Request successful"
}

---

Switch algorithm

GET /api/data?algorithm=sliding

---

Use API key

GET /api/data?api_key=user1

---

## API Endpoints

Main API

GET /
Test endpoint protected by rate limiting.

Monitoring APIs

GET /stats
Returns allowed and blocked request statistics.

GET /top_ips
Returns most active client IP addresses.

GET /active_clients
Returns currently active clients.

GET /system
Returns system metrics.

Dashboard

GET /dashboard
Visual dashboard for monitoring rate limiting metrics.

---

# Analytics Endpoints

Traffic statistics

GET /stats

Example response:

{
"allowed": 120,
"blocked": 32,
"total": 152,
"requests_per_minute": 28
}

---

Top IP addresses
GET /top_ips

---

Active clients
GET /active_clients

---

System configuration
GET /system

---

# Load Testing

This project includes load testing using **Locust**.

Run Locust

locust -f load_test.py

Open Locust UI:
http://localhost:8089

Example test configuration:
Users: 100
Spawn Rate: 10

This simulates burst traffic and demonstrates the limiter blocking excessive requests.

---
## Monitoring Dashboard

The project includes a monitoring dashboard that visualizes system traffic.

Metrics displayed:

- Allowed requests
- Blocked requests
- Total traffic
- Requests per minute
- Top client IPs

Dashboard URL:

http://localhost:8000/dashboard

---

# Run Locally

Clone repository

git clone https://github.com/Prafful7601/distributed-rate-limiter

cd distributed-rate-limiter

Install dependencies

pip install -r requirements.txt

Start Redis

docker run -p 6379:6379 redis

Start API server

uvicorn app.main:app --reload

Open dashboard:
http://localhost:8000/dashboard

---

# Project Structure

distributed-rate-limiter/
│
├── app/
│   │
│   ├── main.py
│   │   FastAPI application entry point
│   │   Registers middleware, routes, and dashboard endpoints
│   │
│   ├── middleware/
│   │   └── rate_limiter.py
│   │       Global middleware that intercepts requests and applies rate limiting
│   │
│   ├── limiter/
│   │   ├── redis_lua_limiter.py
│   │   │   Distributed rate limiter implemented with Redis Lua scripts
│   │   │
│   │   ├── fixed_window_limiter.py
│   │   │   Fixed window rate limiting algorithm
│   │   │
│   │   └── sliding_window_limiter.py
│   │       Sliding window rate limiting algorithm
│   │
│   ├── storage/
│   │   └── redis_client.py
│   │       Redis connection setup used across the system
│   │
│   └── dashboard/
│       ├── index.html
│       │   Monitoring dashboard UI
│       │
│       └── styles.css
│           Dashboard styling
│
├── requirements.txt
│   Python dependencies
│
├── Dockerfile
│   Container configuration for deployment
│
└── README.md
    Project documentation

load_test.py
Dockerfile
docker-compose.yml
README.md

---

## Tech Stack

Backend
- Python
- FastAPI
- Starlette Middleware

Distributed Systems
- Redis
- Redis Lua scripting

Algorithms
- Token Bucket
- Sliding Window
- Fixed Window

Infrastructure
- Docker
- Render Cloud

Frontend
- HTML
- CSS
- Chart.js

---

# Learning Outcomes

This project demonstrates knowledge of:

- Distributed systems design
- Rate limiting algorithms
- Redis data structures
- Middleware architecture
- API observability
- Cloud deployment

---

# Author

Prafful Gupta
Backend developer focused on distributed systems and scalable backend infrastructure.

LinkedIn
https://www.linkedin.com/in/prafful-gupta-67a3b0203/

© Prafful Gupta