"""
Thread-safe version of LRU Cache using RLock.
Wraps all operations with a reentrant lock for concurrent access.
"""

import threading

from lru_cache import LRUCache


class ThreadSafeLRUCache(LRUCache):
    """Thread-safe LRU Cache using RLock for concurrent access."""

    def __init__(self, capacity: int) -> None:
        super().__init__(capacity)
        self._lock = threading.RLock()

    def get(self, key: int) -> int:
        """Thread-safe get."""
        with self._lock:
            return super().get(key)

    def put(self, key: int, value: int) -> None:
        """Thread-safe put."""
        with self._lock:
            super().put(key, value)
