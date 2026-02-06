# Concurrency Practice Exercises

10 hands-on concurrency problems with Python threading solutions.

---

## Problem 1: Thread-Safe Counter

**Problem:** Implement a counter that can be safely incremented by multiple threads simultaneously. Without synchronization, the counter will produce incorrect results due to race conditions.

**Hints:**
- Use `threading.Lock` to protect the critical section
- The increment operation (`counter += 1`) is NOT atomic in Python
- Test with many threads to verify correctness

**Solution:**

```python
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._count += 1

    def decrement(self):
        with self._lock:
            self._count -= 1

    @property
    def value(self):
        with self._lock:
            return self._count

# --- Demonstration of the race condition ---

class UnsafeCounter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1  # NOT atomic: read, add, write

def test_counter(counter_class, num_threads=100, increments_per_thread=1000):
    counter = counter_class()
    expected = num_threads * increments_per_thread

    def worker():
        for _ in range(increments_per_thread):
            counter.increment()

    threads = [threading.Thread(target=worker) for _ in range(num_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    actual = counter.value if hasattr(counter, 'value') else counter.count
    status = "PASS" if actual == expected else "FAIL"
    print(f"{counter_class.__name__}: expected={expected}, actual={actual} [{status}]")

test_counter(UnsafeCounter)       # Likely FAIL (race condition)
test_counter(ThreadSafeCounter)   # Always PASS
```

---

## Problem 2: Bounded Blocking Queue

**Problem:** Implement a thread-safe queue with a fixed capacity. Producers block when the queue is full. Consumers block when the queue is empty.

**Hints:**
- Use `threading.Condition` (or two conditions: not_full and not_empty)
- `Condition.wait()` releases the lock and waits for notification
- `Condition.notify()` wakes up one waiting thread

**Solution:**

```python
import threading
import time
import random

class BoundedBlockingQueue:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._queue = []
        self._lock = threading.Lock()
        self._not_full = threading.Condition(self._lock)
        self._not_empty = threading.Condition(self._lock)

    def put(self, item):
        with self._not_full:
            while len(self._queue) >= self._capacity:
                self._not_full.wait()
            self._queue.append(item)
            self._not_empty.notify()

    def get(self):
        with self._not_empty:
            while len(self._queue) == 0:
                self._not_empty.wait()
            item = self._queue.pop(0)
            self._not_full.notify()
            return item

    def size(self):
        with self._lock:
            return len(self._queue)

# Test
queue = BoundedBlockingQueue(capacity=5)
produced = []
consumed = []
produced_lock = threading.Lock()
consumed_lock = threading.Lock()

def producer(pid, count):
    for i in range(count):
        item = f"P{pid}-{i}"
        queue.put(item)
        with produced_lock:
            produced.append(item)
        time.sleep(random.uniform(0, 0.01))

def consumer(cid, count):
    for _ in range(count):
        item = queue.get()
        with consumed_lock:
            consumed.append(item)
        time.sleep(random.uniform(0, 0.01))

# 3 producers x 10 items = 30 total, 2 consumers x 15 items = 30 total
threads = []
for i in range(3):
    threads.append(threading.Thread(target=producer, args=(i, 10)))
for i in range(2):
    threads.append(threading.Thread(target=consumer, args=(i, 15)))

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Produced: {len(produced)}, Consumed: {len(consumed)}")
print(f"All items consumed: {sorted(produced) == sorted(consumed)}")
print(f"Queue empty: {queue.size() == 0}")
```

---

## Problem 3: Readers-Writer Lock

**Problem:** Implement a lock that allows multiple concurrent readers OR a single exclusive writer. Readers should not block each other. Writers need exclusive access.

**Hints:**
- Track the number of active readers
- Writer must wait for all readers to finish
- New readers must wait if a writer is waiting (to prevent writer starvation)

**Solution:**

```python
import threading
import time

class ReadWriteLock:
    def __init__(self):
        self._lock = threading.Lock()
        self._readers_done = threading.Condition(self._lock)
        self._active_readers = 0
        self._waiting_writers = 0
        self._active_writer = False

    def acquire_read(self):
        with self._lock:
            # Wait if a writer is active or waiting (prevents writer starvation)
            while self._active_writer or self._waiting_writers > 0:
                self._readers_done.wait()
            self._active_readers += 1

    def release_read(self):
        with self._lock:
            self._active_readers -= 1
            if self._active_readers == 0:
                self._readers_done.notify_all()

    def acquire_write(self):
        with self._lock:
            self._waiting_writers += 1
            while self._active_readers > 0 or self._active_writer:
                self._readers_done.wait()
            self._waiting_writers -= 1
            self._active_writer = True

    def release_write(self):
        with self._lock:
            self._active_writer = False
            self._readers_done.notify_all()

# Test
rw_lock = ReadWriteLock()
shared_data = {"value": 0}
log = []
log_lock = threading.Lock()

def reader(rid):
    for _ in range(5):
        rw_lock.acquire_read()
        val = shared_data["value"]
        with log_lock:
            log.append(f"R{rid} read {val}")
        time.sleep(0.001)
        rw_lock.release_read()

def writer(wid):
    for i in range(3):
        rw_lock.acquire_write()
        shared_data["value"] += 1
        with log_lock:
            log.append(f"W{wid} wrote {shared_data['value']}")
        time.sleep(0.002)
        rw_lock.release_write()

threads = []
for i in range(5):
    threads.append(threading.Thread(target=reader, args=(i,)))
for i in range(2):
    threads.append(threading.Thread(target=writer, args=(i,)))

for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Final value: {shared_data['value']}")
print(f"Total operations: {len(log)}")
```

---

## Problem 4: Thread-Safe LRU Cache

**Problem:** Implement an LRU (Least Recently Used) cache that supports concurrent reads and writes safely.

**Hints:**
- Use `OrderedDict` for O(1) get/put with LRU ordering
- Protect all operations with a lock
- `move_to_end()` marks recent access

**Solution:**

```python
import threading
from collections import OrderedDict

class ThreadSafeLRUCache:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._cache = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, key):
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._hits += 1
                return self._cache[key]
            self._misses += 1
            return None

    def put(self, key, value):
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key] = value
            else:
                if len(self._cache) >= self._capacity:
                    self._cache.popitem(last=False)  # Remove LRU
                self._cache[key] = value

    def size(self):
        with self._lock:
            return len(self._cache)

    def stats(self):
        with self._lock:
            total = self._hits + self._misses
            ratio = self._hits / total if total > 0 else 0
            return {"hits": self._hits, "misses": self._misses, "hit_ratio": ratio}

# Test
cache = ThreadSafeLRUCache(capacity=3)

def worker(wid, ops):
    for i in range(ops):
        key = f"key_{i % 5}"
        if i % 3 == 0:
            cache.put(key, f"val_{wid}_{i}")
        else:
            cache.get(key)

threads = [threading.Thread(target=worker, args=(i, 100)) for i in range(10)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Cache size: {cache.size()}")
print(f"Stats: {cache.stats()}")
```

---

## Problem 5: Dining Philosophers (Deadlock-Free)

**Problem:** Five philosophers sit at a table. Each needs two forks to eat. Design a deadlock-free solution.

**Hints:**
- Classic deadlock: each philosopher picks up left fork, waits for right → circular wait
- Solution 1: Resource ordering — always pick up lower-numbered fork first
- Solution 2: Use a semaphore to limit concurrent diners to N-1

**Solution (Resource Ordering):**

```python
import threading
import time
import random

class DiningPhilosophers:
    def __init__(self, num_philosophers: int = 5):
        self._num = num_philosophers
        self._forks = [threading.Lock() for _ in range(num_philosophers)]
        self._eat_count = [0] * num_philosophers

    def philosopher(self, pid: int, meals: int):
        left = pid
        right = (pid + 1) % self._num

        # Key insight: always acquire lower-numbered fork first
        # This breaks circular wait condition
        first = min(left, right)
        second = max(left, right)

        for _ in range(meals):
            # Think
            time.sleep(random.uniform(0, 0.01))

            # Pick up forks in order
            self._forks[first].acquire()
            self._forks[second].acquire()

            # Eat
            self._eat_count[pid] += 1
            time.sleep(random.uniform(0, 0.005))

            # Put down forks
            self._forks[second].release()
            self._forks[first].release()

    def run(self, meals_per_philosopher: int = 10):
        threads = []
        for i in range(self._num):
            t = threading.Thread(target=self.philosopher, args=(i, meals_per_philosopher))
            threads.append(t)

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        print("All philosophers finished eating!")
        for i, count in enumerate(self._eat_count):
            print(f"  Philosopher {i}: {count} meals")
        total = sum(self._eat_count)
        print(f"  Total meals: {total} (expected: {self._num * meals_per_philosopher})")

dp = DiningPhilosophers(5)
dp.run(meals_per_philosopher=20)
```

**Why it works:** By always acquiring the lower-numbered fork first, we impose a total ordering on resource acquisition. This breaks the circular wait condition, one of the four necessary conditions for deadlock.

---

## Problem 6: Rate Limiter (Token Bucket)

**Problem:** Implement a thread-safe token bucket rate limiter that allows N requests per second.

**Hints:**
- Bucket starts full with N tokens
- Each request consumes one token
- Tokens refill at a constant rate
- Use time-based calculation instead of a background thread

**Solution:**

```python
import threading
import time

class TokenBucketRateLimiter:
    def __init__(self, rate: float, capacity: int):
        """
        rate: tokens added per second
        capacity: maximum tokens in bucket
        """
        self._rate = rate
        self._capacity = capacity
        self._tokens = capacity
        self._last_refill = time.monotonic()
        self._lock = threading.Lock()

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self._last_refill
        new_tokens = elapsed * self._rate
        self._tokens = min(self._capacity, self._tokens + new_tokens)
        self._last_refill = now

    def allow(self) -> bool:
        with self._lock:
            self._refill()
            if self._tokens >= 1:
                self._tokens -= 1
                return True
            return False

    def wait_for_token(self, timeout: float = None) -> bool:
        """Block until a token is available or timeout."""
        deadline = time.monotonic() + timeout if timeout else float('inf')
        while True:
            if self.allow():
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.01)

# Test
limiter = TokenBucketRateLimiter(rate=10, capacity=10)  # 10 requests/sec

allowed = 0
denied = 0
lock = threading.Lock()

def make_requests(count):
    global allowed, denied
    for _ in range(count):
        result = limiter.allow()
        with lock:
            if result:
                allowed += 1
            else:
                denied += 1
        time.sleep(0.005)  # 5ms between requests

threads = [threading.Thread(target=make_requests, args=(50,)) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"Allowed: {allowed}, Denied: {denied}, Total: {allowed + denied}")
```

---

## Problem 7: Producer-Consumer with Multiple Producers

**Problem:** Implement a producer-consumer system with multiple producers and consumers, with a poison pill mechanism for graceful shutdown.

**Hints:**
- Use a shared blocking queue
- Sentinel value (poison pill) signals consumers to stop
- Number of poison pills = number of consumers

**Solution:**

```python
import threading
import time
import random
from queue import Queue

POISON_PILL = None

class ProducerConsumerSystem:
    def __init__(self, queue_size: int, num_producers: int, num_consumers: int):
        self._queue = Queue(maxsize=queue_size)
        self._num_producers = num_producers
        self._num_consumers = num_consumers
        self._produced = []
        self._consumed = []
        self._prod_lock = threading.Lock()
        self._cons_lock = threading.Lock()

    def producer(self, pid: int, items: int):
        for i in range(items):
            item = f"item-{pid}-{i}"
            self._queue.put(item)
            with self._prod_lock:
                self._produced.append(item)
            time.sleep(random.uniform(0, 0.005))
        print(f"Producer {pid} finished producing {items} items")

    def consumer(self, cid: int):
        while True:
            item = self._queue.get()
            if item is POISON_PILL:
                print(f"Consumer {cid} received poison pill, shutting down")
                break
            with self._cons_lock:
                self._consumed.append(item)
            # Simulate processing
            time.sleep(random.uniform(0, 0.005))

    def run(self, items_per_producer: int):
        producers = []
        consumers = []

        # Start consumers first
        for i in range(self._num_consumers):
            t = threading.Thread(target=self.consumer, args=(i,))
            consumers.append(t)
            t.start()

        # Start producers
        for i in range(self._num_producers):
            t = threading.Thread(target=self.producer, args=(i, items_per_producer))
            producers.append(t)
            t.start()

        # Wait for all producers to finish
        for t in producers:
            t.join()

        # Send poison pills to all consumers
        for _ in range(self._num_consumers):
            self._queue.put(POISON_PILL)

        # Wait for all consumers to finish
        for t in consumers:
            t.join()

        print(f"\nResults:")
        print(f"  Produced: {len(self._produced)}")
        print(f"  Consumed: {len(self._consumed)}")
        print(f"  All consumed: {sorted(self._produced) == sorted(self._consumed)}")

system = ProducerConsumerSystem(queue_size=10, num_producers=3, num_consumers=2)
system.run(items_per_producer=20)
```

---

## Problem 8: Thread Pool

**Problem:** Implement a simple thread pool that manages a fixed number of worker threads and processes submitted tasks.

**Hints:**
- Workers pull tasks from a shared queue
- Support submitting callables with results (Future-like)
- Use poison pill to shut down workers

**Solution:**

```python
import threading
from queue import Queue
from dataclasses import dataclass
from typing import Callable, Any

class Future:
    def __init__(self):
        self._result = None
        self._exception = None
        self._done = threading.Event()

    def set_result(self, result):
        self._result = result
        self._done.set()

    def set_exception(self, exc):
        self._exception = exc
        self._done.set()

    def result(self, timeout=None):
        self._done.wait(timeout)
        if not self._done.is_set():
            raise TimeoutError("Future did not complete in time")
        if self._exception:
            raise self._exception
        return self._result

    @property
    def done(self):
        return self._done.is_set()

SHUTDOWN = object()

class ThreadPool:
    def __init__(self, num_workers: int):
        self._num_workers = num_workers
        self._task_queue = Queue()
        self._workers = []
        self._is_shutdown = False

        for i in range(num_workers):
            t = threading.Thread(target=self._worker, args=(i,), daemon=True)
            self._workers.append(t)
            t.start()

    def _worker(self, worker_id):
        while True:
            task = self._task_queue.get()
            if task is SHUTDOWN:
                break
            func, args, kwargs, future = task
            try:
                result = func(*args, **kwargs)
                future.set_result(result)
            except Exception as e:
                future.set_exception(e)

    def submit(self, func: Callable, *args, **kwargs) -> Future:
        if self._is_shutdown:
            raise RuntimeError("ThreadPool is shut down")
        future = Future()
        self._task_queue.put((func, args, kwargs, future))
        return future

    def shutdown(self, wait=True):
        self._is_shutdown = True
        for _ in range(self._num_workers):
            self._task_queue.put(SHUTDOWN)
        if wait:
            for t in self._workers:
                t.join()

# Test
import time

def slow_square(n):
    time.sleep(0.05)
    return n * n

def will_fail():
    raise ValueError("Intentional error")

pool = ThreadPool(num_workers=4)

# Submit tasks
futures = [pool.submit(slow_square, i) for i in range(20)]

# Collect results
results = [f.result() for f in futures]
print(f"Squares: {results}")

# Test error handling
error_future = pool.submit(will_fail)
try:
    error_future.result()
except ValueError as e:
    print(f"Caught expected error: {e}")

pool.shutdown()
print("Thread pool shut down cleanly.")
```

---

## Problem 9: Concurrent Hash Map

**Problem:** Implement a hash map that supports concurrent reads and writes with fine-grained locking (lock striping).

**Hints:**
- Divide the hash space into segments, each with its own lock
- This allows concurrent access to different segments
- More segments = more concurrency, but more memory for locks

**Solution:**

```python
import threading
from typing import Any

class ConcurrentHashMap:
    def __init__(self, num_segments: int = 16, initial_capacity: int = 64):
        self._num_segments = num_segments
        self._segments = [[] for _ in range(initial_capacity)]
        self._locks = [threading.Lock() for _ in range(num_segments)]
        self._size = 0
        self._size_lock = threading.Lock()
        self._capacity = initial_capacity

    def _get_segment_index(self, key) -> int:
        return hash(key) % self._num_segments

    def _get_bucket_index(self, key) -> int:
        return hash(key) % self._capacity

    def _get_lock(self, key) -> threading.Lock:
        return self._locks[self._get_segment_index(key)]

    def put(self, key, value) -> Any:
        lock = self._get_lock(key)
        with lock:
            bucket_idx = self._get_bucket_index(key)
            bucket = self._segments[bucket_idx]
            for i, (k, v) in enumerate(bucket):
                if k == key:
                    old_value = v
                    bucket[i] = (key, value)
                    return old_value
            bucket.append((key, value))
            with self._size_lock:
                self._size += 1
            return None

    def get(self, key, default=None) -> Any:
        lock = self._get_lock(key)
        with lock:
            bucket_idx = self._get_bucket_index(key)
            bucket = self._segments[bucket_idx]
            for k, v in bucket:
                if k == key:
                    return v
            return default

    def remove(self, key) -> Any:
        lock = self._get_lock(key)
        with lock:
            bucket_idx = self._get_bucket_index(key)
            bucket = self._segments[bucket_idx]
            for i, (k, v) in enumerate(bucket):
                if k == key:
                    bucket.pop(i)
                    with self._size_lock:
                        self._size -= 1
                    return v
            return None

    def __contains__(self, key) -> bool:
        return self.get(key) is not None

    def __len__(self) -> int:
        with self._size_lock:
            return self._size

# Test
cmap = ConcurrentHashMap(num_segments=8)

def writer(wid, count):
    for i in range(count):
        cmap.put(f"key-{wid}-{i}", f"val-{wid}-{i}")

def reader(rid, keys):
    results = []
    for key in keys:
        val = cmap.get(key)
        results.append((key, val))
    return results

# Concurrent writes
write_threads = [threading.Thread(target=writer, args=(i, 100)) for i in range(8)]
for t in write_threads:
    t.start()
for t in write_threads:
    t.join()

print(f"Size after writes: {len(cmap)}")
print(f"Sample get: {cmap.get('key-0-0')}")
print(f"Contains key-3-50: {'key-3-50' in cmap}")

# Remove
cmap.remove("key-0-0")
print(f"After remove: {cmap.get('key-0-0', 'NOT FOUND')}")
```

---

## Problem 10: Fix the Race Condition

**Problem:** The following code has a race condition. Identify it and fix it.

### Buggy Code

```python
import threading
import time

class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if self.balance >= amount:
            # Simulate some processing time
            time.sleep(0.001)
            self.balance -= amount
            return True
        return False

    def deposit(self, amount):
        temp = self.balance
        time.sleep(0.001)
        self.balance = temp + amount

def transfer(from_account, to_account, amount):
    if from_account.withdraw(amount):
        to_account.deposit(amount)
        return True
    return False

# Test: Two accounts, concurrent transfers
account_a = BankAccount(1000)
account_b = BankAccount(1000)

threads = []
for _ in range(10):
    t1 = threading.Thread(target=transfer, args=(account_a, account_b, 100))
    t2 = threading.Thread(target=transfer, args=(account_b, account_a, 50))
    threads.extend([t1, t2])

for t in threads:
    t.start()
for t in threads:
    t.join()

total = account_a.balance + account_b.balance
print(f"Account A: {account_a.balance}")
print(f"Account B: {account_b.balance}")
print(f"Total: {total} (should be 2000)")
# Total will likely NOT be 2000 — money was created or destroyed!
```

### What's Wrong?

Three race conditions:

1. **withdraw — check-then-act:** Between checking `balance >= amount` and subtracting, another thread can modify the balance, allowing double withdrawal.

2. **deposit — read-modify-write:** `deposit` reads balance into `temp`, sleeps, then writes `temp + amount`. If two concurrent deposits happen, one overwrites the other's result. Example:
   - Balance is 500
   - Thread A reads 500, Thread B reads 500
   - Thread A writes 600 (+100), Thread B writes 550 (+50)
   - Final balance: 550 (should be 650) — $100 was lost

3. **transfer — non-atomic:** The `withdraw` and `deposit` in `transfer` are not atomic. If a crash happens between them, money disappears.

### Fixed Code

```python
import threading
import time

class BankAccount:
    _id_counter = 0
    _id_lock = threading.Lock()

    def __init__(self, balance):
        self.balance = balance
        self.lock = threading.Lock()
        # Assign a unique ID for consistent lock ordering
        with BankAccount._id_lock:
            self._id = BankAccount._id_counter
            BankAccount._id_counter += 1

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                time.sleep(0.001)
                self.balance -= amount
                return True
            return False

    def deposit(self, amount):
        with self.lock:
            time.sleep(0.001)
            self.balance += amount

def transfer(from_account, to_account, amount):
    # Lock ordering: always acquire lower ID first to prevent deadlock
    first = from_account if from_account._id < to_account._id else to_account
    second = to_account if from_account._id < to_account._id else from_account

    with first.lock:
        with second.lock:
            if from_account.balance >= amount:
                from_account.balance -= amount
                to_account.balance += amount
                return True
            return False

# Test: Same scenario
account_a = BankAccount(1000)
account_b = BankAccount(1000)

threads = []
for _ in range(10):
    t1 = threading.Thread(target=transfer, args=(account_a, account_b, 100))
    t2 = threading.Thread(target=transfer, args=(account_b, account_a, 50))
    threads.extend([t1, t2])

for t in threads:
    t.start()
for t in threads:
    t.join()

total = account_a.balance + account_b.balance
print(f"Account A: {account_a.balance}")
print(f"Account B: {account_b.balance}")
print(f"Total: {total} (should be 2000)")
assert total == 2000, f"Money conservation violated! Total: {total}"
print("PASS: Money conservation maintained.")
```

### Key Fixes
1. **Lock on each account:** Protects individual read-modify-write operations
2. **Lock ordering in transfer:** Both accounts locked simultaneously using consistent ID ordering prevents deadlock
3. **Atomic transfer:** Withdraw and deposit happen within the same lock scope, so no money disappears between them
