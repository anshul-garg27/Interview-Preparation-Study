# Rate Limiter - Low Level Design

## Problem Statement
Design a rate limiter that can restrict the number of requests a client can make within a time window. Support multiple algorithms: Token Bucket, Sliding Window, Fixed Window, and Leaky Bucket. The system should be thread-safe, configurable, and support per-user limits.

---

## Functional Requirements
1. **Limit Requests** - Allow or deny based on rate limit rules
2. **Multiple Algorithms** - Token Bucket, Sliding Window, Fixed Window, Leaky Bucket
3. **Per-User Limiting** - Different limits per client/API key
4. **Configurable Limits** - Requests per second/minute/hour
5. **Thread-Safe** - Handle concurrent requests correctly
6. **Rate Limit Headers** - Return remaining quota, reset time

## Non-Functional Requirements
- Sub-millisecond decision time
- Minimal memory per client
- Accurate under high concurrency
- Graceful degradation

---

## Design Patterns Used

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Strategy** | Algorithm selection (Token Bucket, Sliding Window, etc.) | Swap algorithms without changing client code |
| **Singleton** | Global rate limiter instance | Single point of enforcement |
| **Factory** | Create appropriate limiter per config | Encapsulate creation logic |

---

## How Each Algorithm Works

### 1. Token Bucket

```mermaid
graph LR
    subgraph Token Bucket
        B[Bucket<br/>Capacity: 10]
        R[Refill: 2 tokens/sec]
    end
    R -->|add tokens| B
    Req[Request] -->|consume 1 token| B
    B -->|tokens > 0| A[ALLOWED]
    B -->|tokens = 0| D[DENIED]
```

- Bucket holds tokens up to a max capacity
- Tokens are added at a fixed rate
- Each request consumes one token
- **Pros**: Allows bursts up to bucket size
- **Best for**: APIs that allow short bursts

### 2. Fixed Window

```mermaid
graph TD
    subgraph "Fixed Window (1 min)"
        W1["Window 12:00-12:01<br/>Count: 8/10"]
        W2["Window 12:01-12:02<br/>Count: 3/10"]
    end
    Req1[Request at 12:00:45] --> W1
    Req2[Request at 12:01:15] --> W2
    W1 -->|count < limit| A1[ALLOWED]
    W2 -->|count < limit| A2[ALLOWED]
```

- Divide time into fixed windows (e.g., per minute)
- Count requests in current window
- Reset count at window boundary
- **Cons**: Boundary problem (2x burst at window edges)
- **Best for**: Simple rate limiting

### 3. Sliding Window Log

```mermaid
graph TD
    subgraph "Sliding Window (last 60 seconds)"
        Log["Timestamp Log:<br/>12:00:15, 12:00:30,<br/>12:00:45, 12:01:05"]
    end
    Req["Request at 12:01:10"]
    Req --> Log
    Log -->|"Remove < 12:00:10<br/>Count remaining"| Check{Count < Limit?}
    Check -->|Yes| A[ALLOWED]
    Check -->|No| D[DENIED]
```

- Keep a log of all request timestamps
- For each request, remove timestamps outside the window
- Count remaining entries
- **Pros**: Most accurate, no boundary issues
- **Cons**: Memory-intensive (stores all timestamps)
- **Best for**: Strict accuracy requirements

### 4. Leaky Bucket

```mermaid
graph TD
    subgraph "Leaky Bucket"
        Q["Queue<br/>(max size: 10)"]
        Leak["Process: 2 req/sec"]
    end
    Req[Request] --> Q
    Q -->|"queue full"| D[DENIED]
    Q -->|"queue not full"| A[QUEUED]
    Q -->|"drain at fixed rate"| Leak
    Leak --> Process[Process Request]
```

- Requests enter a queue (bucket)
- Queue drains at a fixed rate
- If queue is full, requests are rejected
- **Pros**: Smooth output rate, no bursts
- **Best for**: Protecting downstream services from bursts

---

## Class Diagram

```mermaid
classDiagram
    class RateLimiter {
        <<interface>>
        +allow_request(client_id) bool
        +get_remaining(client_id) int
        +get_reset_time(client_id) float
    }

    class TokenBucketLimiter {
        -int capacity
        -float refill_rate
        -Map~String, Bucket~ buckets
        +allow_request(client_id) bool
    }

    class FixedWindowLimiter {
        -int max_requests
        -float window_size_sec
        -Map~String, WindowData~ windows
        +allow_request(client_id) bool
    }

    class SlidingWindowLimiter {
        -int max_requests
        -float window_size_sec
        -Map~String, Deque~ logs
        +allow_request(client_id) bool
    }

    class LeakyBucketLimiter {
        -int capacity
        -float leak_rate
        -Map~String, BucketData~ buckets
        +allow_request(client_id) bool
    }

    class Bucket {
        -float tokens
        -float last_refill_time
    }

    class RateLimiterConfig {
        -String algorithm
        -int max_requests
        -float window_seconds
        -int bucket_capacity
        -float refill_rate
    }

    class RateLimiterFactory {
        +create(config) RateLimiter
    }

    class RateLimitMiddleware {
        -Map~String, RateLimiter~ limiters
        +check(client_id, endpoint) RateLimitResult
    }

    class RateLimitResult {
        -bool allowed
        -int remaining
        -float retry_after
    }

    RateLimiter <|.. TokenBucketLimiter
    RateLimiter <|.. FixedWindowLimiter
    RateLimiter <|.. SlidingWindowLimiter
    RateLimiter <|.. LeakyBucketLimiter
    TokenBucketLimiter --> Bucket
    RateLimiterFactory --> RateLimiter
    RateLimiterFactory --> RateLimiterConfig
    RateLimitMiddleware --> RateLimiter
    RateLimitMiddleware --> RateLimitResult
```

---

## Sequence Diagram - Request Flow

```mermaid
sequenceDiagram
    participant C as Client
    participant M as Middleware
    participant RL as RateLimiter (Token Bucket)
    participant B as Bucket

    C->>M: HTTP Request (client_id=user123)
    M->>RL: allow_request("user123")
    RL->>B: get_or_create_bucket("user123")
    B-->>RL: bucket (tokens=5, last_refill=T1)
    RL->>B: refill_tokens(elapsed_time)
    Note over B: tokens = min(capacity, tokens + elapsed * rate)
    RL->>B: try_consume(1)
    alt tokens > 0
        B-->>RL: True (tokens=4)
        RL-->>M: RateLimitResult(allowed=True, remaining=4)
        M-->>C: 200 OK + X-RateLimit-Remaining: 4
    else tokens = 0
        B-->>RL: False
        RL-->>M: RateLimitResult(allowed=False, retry_after=0.5s)
        M-->>C: 429 Too Many Requests + Retry-After: 0.5
    end
```

---

## Algorithm Comparison

| Algorithm | Burst Handling | Memory | Accuracy | Complexity |
|-----------|---------------|--------|----------|------------|
| Token Bucket | Allows bursts | O(1) per user | Good | Low |
| Fixed Window | Boundary burst | O(1) per user | Moderate | Low |
| Sliding Window | No bursts | O(n) per user | Best | Medium |
| Leaky Bucket | Smooths output | O(1) per user | Good | Low |

---

## Edge Cases
1. **Clock skew** - Use monotonic clock, not wall clock
2. **Distributed system** - Need Redis/centralized store for consistency
3. **Race conditions** - Lock per client_id, not global lock
4. **Large number of clients** - Lazy cleanup of expired state
5. **Negative refill** - Handle system clock going backward
6. **0-capacity bucket** - Reject all requests immediately
7. **Burst at window boundary** - Fixed window allows 2x burst; use sliding window
8. **Long idle clients** - Cap token refill at max capacity

## Extensions
- Distributed rate limiting with Redis
- Rate limiting by IP, API key, or endpoint
- Dynamic rate limit adjustment based on load
- Rate limit tiers (free vs premium)
- Exponential backoff recommendations in 429 responses
- Rate limit dashboard and monitoring

---

## Interview Tips

1. **Know all 4 algorithms** - Be ready to explain trade-offs between each
2. **Start with Token Bucket** - Most commonly asked, best balance of simplicity and features
3. **Discuss thread safety** - Critical for production; mention locks or atomic operations
4. **Mention distributed case** - "In production, I'd use Redis with Lua scripts for atomicity"
5. **Draw the bucket diagram** - Visual explanation is very effective
6. **Common follow-up**: "How to rate limit in a microservices architecture?" - API gateway, sidecar proxy
7. **Common follow-up**: "Token Bucket vs Leaky Bucket?" - Token allows bursts, Leaky smooths output
