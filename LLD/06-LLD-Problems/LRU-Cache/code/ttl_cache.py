"""
TTL (Time-To-Live) Cache variation.
Entries automatically expire after a configurable duration.
"""

import time


class TTLCache:
    """
    Cache with time-based expiration.
    - get(key): O(1) - returns value or -1 if expired/missing
    - put(key, value): O(1) - stores with current timestamp
    Expired entries are lazily evicted on access.
    """

    def __init__(self, capacity: int, ttl_seconds: float) -> None:
        self._capacity = capacity
        self._ttl = ttl_seconds
        self._cache: dict[int, tuple[int, float]] = {}  # key -> (value, timestamp)
        self._trace: bool = True

    def _is_expired(self, key: int) -> bool:
        """Check if a key has expired."""
        if key not in self._cache:
            return True
        _, ts = self._cache[key]
        return (time.time() - ts) > self._ttl

    def _print_state(self, operation: str) -> None:
        if self._trace:
            now = time.time()
            items = [
                f"{k}:{v}({self._ttl - (now - ts):.1f}s left)"
                for k, (v, ts) in self._cache.items()
                if (now - ts) <= self._ttl
            ]
            print(f"    {operation:35s} -> [{', '.join(items)}]")

    def _evict_expired(self) -> None:
        """Remove all expired entries."""
        expired = [k for k in self._cache if self._is_expired(k)]
        for k in expired:
            del self._cache[k]

    def get(self, key: int) -> int:
        """Get value by key. Returns -1 if expired or missing."""
        if key in self._cache and not self._is_expired(key):
            val, ts = self._cache[key]
            self._print_state(f"GET({key}) = {val}")
            return val
        if key in self._cache:
            del self._cache[key]
        self._print_state(f"GET({key}) = -1 (expired/miss)")
        return -1

    def put(self, key: int, value: int) -> None:
        """Store a value with the current timestamp."""
        self._evict_expired()
        if key not in self._cache and len(self._cache) >= self._capacity:
            # Evict oldest entry
            oldest_key = min(self._cache, key=lambda k: self._cache[k][1])
            del self._cache[oldest_key]
        self._cache[key] = (value, time.time())
        self._print_state(f"PUT({key},{value}) stored")
