"""
LRU Cache System - Demo
========================
Demonstrates: LRU Cache, Thread-safe Cache, LFU Cache, TTL Cache.
Step-by-step operations showing cache state after each action.

Run: cd code/ && python demo.py
"""

import time
import threading

from lru_cache import LRUCache
from thread_safe_lru_cache import ThreadSafeLRUCache
from lfu_cache import LFUCache
from ttl_cache import TTLCache


if __name__ == "__main__":
    print("=" * 70)
    print("  LRU CACHE SYSTEM - Modular LLD Demo")
    print("=" * 70)

    # ---- Scenario 1: Basic LRU Cache ----
    print("\n[Scenario 1: Basic LRU Cache (capacity=3)]")
    print("  Operations trace (MRU <-- left ... right --> LRU):\n")
    cache = LRUCache(capacity=3)

    cache.put(1, 10)
    cache.put(2, 20)
    cache.put(3, 30)
    cache.get(1)        # Access 1, making it MRU
    cache.put(4, 40)    # Evicts key 2 (LRU)
    cache.get(2)         # Miss - was evicted
    cache.put(5, 50)    # Evicts key 3
    cache.get(3)         # Miss - was evicted
    cache.get(4)         # Hit
    cache.put(1, 100)   # Update existing key
    cache.get(1)         # Hit with updated value

    # ---- Scenario 2: Edge Cases ----
    print(f"\n{'_'*70}")
    print("\n[Scenario 2: Edge Cases]")

    print("\n  --- Capacity 1 cache ---")
    tiny = LRUCache(capacity=1)
    tiny.put(1, 1)
    tiny.put(2, 2)     # Evicts 1
    tiny.get(1)          # Miss
    tiny.get(2)          # Hit

    print("\n  --- Overwrite same key repeatedly ---")
    cache2 = LRUCache(capacity=2)
    cache2.put(1, 10)
    cache2.put(1, 20)
    cache2.put(1, 30)
    cache2.get(1)

    # ---- Scenario 3: Thread Safety ----
    print(f"\n{'_'*70}")
    print("\n[Scenario 3: Thread-Safe Concurrent Access (capacity=3)]")
    ts_cache = ThreadSafeLRUCache(capacity=3)
    ts_cache._trace = False

    def writer(c: ThreadSafeLRUCache, start: int, count: int) -> None:
        for i in range(start, start + count):
            c.put(i, i * 10)

    t1 = threading.Thread(target=writer, args=(ts_cache, 1, 5))
    t2 = threading.Thread(target=writer, args=(ts_cache, 3, 5))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    ts_cache._trace = True
    print("  State after concurrent writes from two threads:\n")
    for key in range(1, 8):
        ts_cache.get(key)

    # ---- Scenario 4: LeetCode 146 Verification ----
    print(f"\n{'_'*70}")
    print("\n[Scenario 4: LeetCode 146 - LRU Cache Verification]")
    print("  Ops: [put(1,1), put(2,2), get(1), put(3,3), get(2), put(4,4), get(1), get(3), get(4)]")
    print("  Expected: [null, null, 1, null, -1, null, -1, 3, 4]\n")

    lc = LRUCache(capacity=2)
    lc.put(1, 1)
    lc.put(2, 2)
    r1 = lc.get(1)       # 1
    lc.put(3, 3)          # evicts 2
    r2 = lc.get(2)        # -1
    lc.put(4, 4)          # evicts 1
    r3 = lc.get(1)        # -1
    r4 = lc.get(3)        # 3
    r5 = lc.get(4)        # 4

    print(f"\n  Results: get(1)={r1}, get(2)={r2}, get(1)={r3}, get(3)={r4}, get(4)={r5}")
    expected = [1, -1, -1, 3, 4]
    actual = [r1, r2, r3, r4, r5]
    print(f"  All correct: {actual == expected}")

    # ---- Scenario 5: LFU Cache ----
    print(f"\n{'_'*70}")
    print("\n[Scenario 5: LFU Cache (capacity=3)]")
    print("  Evicts least frequently used; ties broken by LRU:\n")
    lfu = LFUCache(capacity=3)
    lfu.put(1, 10)
    lfu.put(2, 20)
    lfu.put(3, 30)
    lfu.get(1)          # freq(1)=2
    lfu.get(1)          # freq(1)=3
    lfu.get(2)          # freq(2)=2
    lfu.put(4, 40)      # Evicts key 3 (freq=1, lowest)
    lfu.get(3)          # Miss

    # ---- Scenario 6: TTL Cache ----
    print(f"\n{'_'*70}")
    print("\n[Scenario 6: TTL Cache (capacity=3, ttl=1s)]")
    print("  Entries expire after 1 second:\n")
    ttl = TTLCache(capacity=3, ttl_seconds=1.0)
    ttl.put(1, 100)
    ttl.put(2, 200)
    ttl.get(1)           # Hit
    print("    ... sleeping 0.5s ...")
    time.sleep(0.5)
    ttl.get(1)           # Still valid
    print("    ... sleeping 0.6s (total > 1s for key 1) ...")
    time.sleep(0.6)
    ttl.get(1)           # Expired
    ttl.get(2)           # Expired
    ttl.put(3, 300)      # Fresh entry
    ttl.get(3)           # Hit

    print("\nDemo complete!")
