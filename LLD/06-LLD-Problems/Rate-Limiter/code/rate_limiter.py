"""
Rate Limiter - Low Level Design
Run: python rate_limiter.py

Patterns: Strategy (algorithm selection), Factory (limiter creation)
Key: 4 algorithms - Token Bucket, Fixed Window, Sliding Window, Leaky Bucket
All are thread-safe.
"""
from abc import ABC, abstractmethod
from collections import defaultdict, deque
from dataclasses import dataclass
import threading
import time


# ─── Result ──────────────────────────────────────────────────────────
@dataclass
class RateLimitResult:
    allowed: bool
    remaining: int = 0
    retry_after: float = 0.0


# ─── Strategy Interface ─────────────────────────────────────────────
class RateLimiter(ABC):
    @abstractmethod
    def allow_request(self, client_id: str) -> RateLimitResult:
        pass


# ─── Algorithm 1: Token Bucket ──────────────────────────────────────
class TokenBucketLimiter(RateLimiter):
    """
    Bucket holds tokens up to capacity. Refills at a constant rate.
    Each request consumes 1 token. Allows bursts up to bucket size.
    """
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity          # max tokens
        self.refill_rate = refill_rate    # tokens per second
        self._buckets: dict[str, list] = {}  # client -> [tokens, last_time]
        self._lock = threading.Lock()

    def allow_request(self, client_id: str) -> RateLimitResult:
        with self._lock:
            now = time.monotonic()
            if client_id not in self._buckets:
                self._buckets[client_id] = [self.capacity, now]

            tokens, last_time = self._buckets[client_id]
            # Refill tokens based on elapsed time
            elapsed = now - last_time
            tokens = min(self.capacity, tokens + elapsed * self.refill_rate)

            if tokens >= 1:
                tokens -= 1
                self._buckets[client_id] = [tokens, now]
                return RateLimitResult(True, remaining=int(tokens))
            else:
                # How long until 1 token is available?
                wait = (1 - tokens) / self.refill_rate
                self._buckets[client_id] = [tokens, now]
                return RateLimitResult(False, remaining=0, retry_after=round(wait, 2))


# ─── Algorithm 2: Fixed Window ──────────────────────────────────────
class FixedWindowLimiter(RateLimiter):
    """
    Divide time into fixed windows. Count requests per window.
    Simple but has boundary burst problem.
    """
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._windows: dict[str, list] = {}  # client -> [count, window_start]
        self._lock = threading.Lock()

    def _get_window_start(self, now: float) -> float:
        return now - (now % self.window_seconds)

    def allow_request(self, client_id: str) -> RateLimitResult:
        with self._lock:
            now = time.monotonic()
            window_start = self._get_window_start(now)

            if client_id not in self._windows:
                self._windows[client_id] = [0, window_start]

            count, win_start = self._windows[client_id]

            # Reset if new window
            if window_start != win_start:
                count = 0
                win_start = window_start

            if count < self.max_requests:
                count += 1
                self._windows[client_id] = [count, win_start]
                return RateLimitResult(True, remaining=self.max_requests - count)
            else:
                retry = self.window_seconds - (now - win_start)
                self._windows[client_id] = [count, win_start]
                return RateLimitResult(False, remaining=0,
                                       retry_after=round(retry, 2))


# ─── Algorithm 3: Sliding Window Log ────────────────────────────────
class SlidingWindowLimiter(RateLimiter):
    """
    Keep a log of request timestamps. Most accurate, no boundary issues.
    Memory: O(max_requests) per client.
    """
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._logs: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def allow_request(self, client_id: str) -> RateLimitResult:
        with self._lock:
            now = time.monotonic()
            log = self._logs[client_id]

            # Evict timestamps outside the window
            cutoff = now - self.window_seconds
            while log and log[0] <= cutoff:
                log.popleft()

            if len(log) < self.max_requests:
                log.append(now)
                return RateLimitResult(True,
                                       remaining=self.max_requests - len(log))
            else:
                # Retry after oldest entry expires
                retry = log[0] + self.window_seconds - now
                return RateLimitResult(False, remaining=0,
                                       retry_after=round(retry, 2))


# ─── Algorithm 4: Leaky Bucket ──────────────────────────────────────
class LeakyBucketLimiter(RateLimiter):
    """
    Requests fill a bucket that leaks at a constant rate.
    Smooths output rate - no bursts allowed.
    """
    def __init__(self, capacity: int, leak_rate: float):
        self.capacity = capacity      # max queue size
        self.leak_rate = leak_rate    # requests drained per second
        self._buckets: dict[str, list] = {}  # client -> [water_level, last_time]
        self._lock = threading.Lock()

    def allow_request(self, client_id: str) -> RateLimitResult:
        with self._lock:
            now = time.monotonic()
            if client_id not in self._buckets:
                self._buckets[client_id] = [0.0, now]

            water, last_time = self._buckets[client_id]
            # Leak water based on elapsed time
            elapsed = now - last_time
            water = max(0, water - elapsed * self.leak_rate)

            if water < self.capacity:
                water += 1
                self._buckets[client_id] = [water, now]
                return RateLimitResult(True,
                                       remaining=int(self.capacity - water))
            else:
                retry = (water - self.capacity + 1) / self.leak_rate
                self._buckets[client_id] = [water, now]
                return RateLimitResult(False, remaining=0,
                                       retry_after=round(retry, 2))


# ─── Factory ─────────────────────────────────────────────────────────
class RateLimiterFactory:
    @staticmethod
    def create(algorithm: str, **kwargs) -> RateLimiter:
        if algorithm == "token_bucket":
            return TokenBucketLimiter(
                capacity=kwargs.get("capacity", 10),
                refill_rate=kwargs.get("refill_rate", 1.0))
        elif algorithm == "fixed_window":
            return FixedWindowLimiter(
                max_requests=kwargs.get("max_requests", 10),
                window_seconds=kwargs.get("window_seconds", 60))
        elif algorithm == "sliding_window":
            return SlidingWindowLimiter(
                max_requests=kwargs.get("max_requests", 10),
                window_seconds=kwargs.get("window_seconds", 60))
        elif algorithm == "leaky_bucket":
            return LeakyBucketLimiter(
                capacity=kwargs.get("capacity", 10),
                leak_rate=kwargs.get("leak_rate", 1.0))
        raise ValueError(f"Unknown algorithm: {algorithm}")


# ─── Demo Helper ─────────────────────────────────────────────────────
def test_limiter(name: str, limiter: RateLimiter, num_requests: int,
                 delay: float = 0):
    print(f"\n{'=' * 60}")
    print(f"  {name}")
    print(f"{'=' * 60}")
    allowed_count = 0
    for i in range(1, num_requests + 1):
        result = limiter.allow_request("user1")
        status = "ALLOWED" if result.allowed else "DENIED"
        extra = (f"remaining={result.remaining}" if result.allowed
                 else f"retry_after={result.retry_after}s")
        print(f"  Request {i:2d}: {status:7s} ({extra})")
        if result.allowed:
            allowed_count += 1
        if delay:
            time.sleep(delay)
    print(f"  Result: {allowed_count}/{num_requests} requests allowed")
    return allowed_count


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("RATE LIMITER DEMO")
    print("=" * 60)

    # 1. Token Bucket: capacity=5, refill=2/sec
    limiter = RateLimiterFactory.create("token_bucket", capacity=5, refill_rate=2)
    test_limiter("TOKEN BUCKET (capacity=5, refill=2/sec)", limiter, 8)
    # Wait for refill and try again
    print("  --- Waiting 2 seconds for refill ---")
    time.sleep(2)
    result = limiter.allow_request("user1")
    print(f"  After wait: {'ALLOWED' if result.allowed else 'DENIED'} "
          f"(remaining={result.remaining})")

    # 2. Fixed Window: 5 requests per 2-second window
    limiter = RateLimiterFactory.create("fixed_window", max_requests=5,
                                         window_seconds=2)
    test_limiter("FIXED WINDOW (5 req / 2 sec)", limiter, 8)

    # 3. Sliding Window: 5 requests per 2-second window
    limiter = RateLimiterFactory.create("sliding_window", max_requests=5,
                                         window_seconds=2)
    test_limiter("SLIDING WINDOW (5 req / 2 sec)", limiter, 8)

    # 4. Leaky Bucket: capacity=5, leak=2/sec
    limiter = RateLimiterFactory.create("leaky_bucket", capacity=5, leak_rate=2)
    test_limiter("LEAKY BUCKET (capacity=5, leak=2/sec)", limiter, 8)

    # 5. Per-user isolation
    print(f"\n{'=' * 60}")
    print("  PER-USER ISOLATION")
    print(f"{'=' * 60}")
    limiter = RateLimiterFactory.create("token_bucket", capacity=3, refill_rate=1)
    for uid in ["alice", "bob"]:
        for i in range(5):
            r = limiter.allow_request(uid)
            print(f"  {uid} request {i+1}: "
                  f"{'ALLOWED' if r.allowed else 'DENIED'}")

    # 6. Thread safety demo
    print(f"\n{'=' * 60}")
    print("  THREAD SAFETY (10 threads, 3 req each, limit=10)")
    print(f"{'=' * 60}")
    limiter = RateLimiterFactory.create("token_bucket", capacity=10, refill_rate=0)
    results = []
    lock = threading.Lock()

    def worker(thread_id):
        for _ in range(3):
            r = limiter.allow_request("shared_user")
            with lock:
                results.append(r.allowed)

    threads = [threading.Thread(target=worker, args=(i,))
               for i in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    allowed = sum(1 for r in results if r)
    print(f"  Total requests: {len(results)}, Allowed: {allowed}, "
          f"Denied: {len(results) - allowed}")
    print(f"  Expected: exactly 10 allowed (bucket capacity)")


if __name__ == "__main__":
    main()
