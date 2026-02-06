"""
Concurrency Patterns Demo in Python
=====================================
Demonstrates race conditions, locks, producer-consumer, thread pools,
deadlocks, and thread-safe singleton using the threading module.

Usage: python concurrency_demo.py
"""

import threading
import time
import queue
from concurrent.futures import ThreadPoolExecutor, as_completed


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ============================================================
# 1. RACE CONDITION DEMONSTRATION
# ============================================================

section("1. Race Condition Demonstration")


class UnsafeCounter:
    """NOT thread-safe - demonstrates race condition."""

    def __init__(self):
        self.count = 0

    def increment(self):
        # This is NOT atomic: read -> modify -> write
        current = self.count
        # Simulate some processing (makes race condition more visible)
        time.sleep(0.0001)
        self.count = current + 1


def demonstrate_race_condition():
    counter = UnsafeCounter()
    threads = []

    def worker():
        for _ in range(100):
            counter.increment()

    # Launch 5 threads, each incrementing 100 times
    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = 500
    actual = counter.count
    print(f"  Expected count: {expected}")
    print(f"  Actual count:   {actual}")
    print(f"  Lost updates:   {expected - actual}")
    print(f"  Race condition: {'YES - data lost!' if actual != expected else 'No (got lucky this time)'}")


print("Running unsafe counter with 5 threads x 100 increments...")
demonstrate_race_condition()


# ============================================================
# 2. FIX WITH LOCK
# ============================================================

section("2. Fix with threading.Lock")


class SafeCounter:
    """Thread-safe counter using a Lock."""

    def __init__(self):
        self.count = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:  # Only one thread can execute this block
            current = self.count
            time.sleep(0.0001)
            self.count = current + 1


def demonstrate_lock_fix():
    counter = SafeCounter()
    threads = []

    def worker():
        for _ in range(100):
            counter.increment()

    for _ in range(5):
        t = threading.Thread(target=worker)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    expected = 500
    actual = counter.count
    print(f"  Expected count: {expected}")
    print(f"  Actual count:   {actual}")
    print(f"  Race condition: {'YES' if actual != expected else 'NO - Lock works!'}")


print("Running safe counter with Lock (5 threads x 100 increments)...")
demonstrate_lock_fix()

# Also demonstrate RLock (reentrant lock)
print("\n--- RLock (Reentrant Lock) ---")


class ReentrantExample:
    """RLock allows the SAME thread to acquire the lock multiple times."""

    def __init__(self):
        self._lock = threading.RLock()
        self.value = 0

    def outer(self):
        with self._lock:
            print(f"  outer() acquired lock (thread: {threading.current_thread().name})")
            self.inner()  # Calls inner() which also acquires the lock

    def inner(self):
        with self._lock:  # Same thread can re-acquire RLock
            self.value += 1
            print(f"  inner() acquired same lock (value: {self.value})")


rlock_demo = ReentrantExample()
rlock_demo.outer()
print("  With a regular Lock, inner() would DEADLOCK because outer() holds the lock!")


# ============================================================
# 3. PRODUCER-CONSUMER WITH QUEUE
# ============================================================

section("3. Producer-Consumer with Queue")


def producer(q: queue.Queue, producer_id: int, items: int):
    """Produces items and puts them in the queue."""
    for i in range(items):
        item = f"item-{producer_id}-{i}"
        q.put(item)
        print(f"  Producer-{producer_id} produced: {item}")
        time.sleep(0.05)
    print(f"  Producer-{producer_id} DONE")


def consumer(q: queue.Queue, consumer_id: int, stop_event: threading.Event):
    """Consumes items from the queue until stop event is set."""
    while not stop_event.is_set() or not q.empty():
        try:
            item = q.get(timeout=0.1)
            print(f"  Consumer-{consumer_id} consumed: {item}")
            q.task_done()
            time.sleep(0.08)  # Simulate processing
        except queue.Empty:
            continue
    print(f"  Consumer-{consumer_id} DONE")


print("Running producer-consumer (2 producers, 2 consumers, 5 items each)...")
print()

work_queue = queue.Queue(maxsize=5)  # Bounded queue - blocks when full
stop = threading.Event()

# Start consumers first
consumers = []
for i in range(2):
    t = threading.Thread(target=consumer, args=(work_queue, i, stop))
    t.start()
    consumers.append(t)

# Start producers
producers = []
for i in range(2):
    t = threading.Thread(target=producer, args=(work_queue, i, 5))
    t.start()
    producers.append(t)

# Wait for producers to finish
for t in producers:
    t.join()

# Wait for queue to drain, then signal consumers to stop
work_queue.join()
stop.set()

for t in consumers:
    t.join()

print("\n  All items produced and consumed!")
print(f"  Queue size: {work_queue.qsize()} (should be 0)")


# ============================================================
# 4. THREAD POOL EXAMPLE
# ============================================================

section("4. Thread Pool with ThreadPoolExecutor")


def fetch_url(url: str) -> dict:
    """Simulate fetching a URL (in reality, use requests/aiohttp)."""
    delay = len(url) * 0.01  # Simulate variable response time
    time.sleep(delay)
    return {"url": url, "status": 200, "size": len(url) * 100}


urls = [
    "https://api.example.com/users",
    "https://api.example.com/products",
    "https://api.example.com/orders",
    "https://api.example.com/inventory",
    "https://api.example.com/analytics",
]

print("Fetching 5 URLs with ThreadPoolExecutor(max_workers=3)...")
print()

start_time = time.time()

with ThreadPoolExecutor(max_workers=3) as executor:
    # Submit all tasks
    future_to_url = {executor.submit(fetch_url, url): url for url in urls}

    # Process results as they complete (not in submission order)
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
            print(f"  Completed: {result['url']} (status={result['status']})")
        except Exception as e:
            print(f"  Failed: {url} ({e})")

elapsed = time.time() - start_time
print(f"\n  Total time: {elapsed:.2f}s (parallel)")
print(f"  Sequential would take: ~{sum(len(u) * 0.01 for u in urls):.2f}s")


# --- Map pattern ---
print("\n--- Map Pattern (simpler syntax) ---")


def square(n: int) -> int:
    time.sleep(0.05)  # Simulate work
    return n * n


numbers = list(range(10))
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(square, numbers))
    print(f"  Squares: {results}")


# ============================================================
# 5. DEADLOCK DEMONSTRATION AND FIX
# ============================================================

section("5. Deadlock Demonstration and Fix")

print("--- DEADLOCK SCENARIO ---")
print("Thread 1: locks A, then tries to lock B")
print("Thread 2: locks B, then tries to lock A")
print("Both wait forever!\n")

lock_a = threading.Lock()
lock_b = threading.Lock()
deadlock_detected = threading.Event()


def deadlock_thread_1():
    lock_a.acquire()
    print("  Thread-1: acquired lock A")
    time.sleep(0.1)  # Give thread 2 time to acquire lock B
    print("  Thread-1: trying to acquire lock B...")
    # Use timeout to avoid actual deadlock in demo
    acquired = lock_b.acquire(timeout=0.5)
    if not acquired:
        print("  Thread-1: TIMEOUT! Could not acquire lock B (DEADLOCK detected)")
        deadlock_detected.set()
    lock_a.release()
    if acquired:
        lock_b.release()


def deadlock_thread_2():
    lock_b.acquire()
    print("  Thread-2: acquired lock B")
    time.sleep(0.1)
    print("  Thread-2: trying to acquire lock A...")
    acquired = lock_a.acquire(timeout=0.5)
    if not acquired:
        print("  Thread-2: TIMEOUT! Could not acquire lock A (DEADLOCK detected)")
        deadlock_detected.set()
    lock_b.release()
    if acquired:
        lock_a.release()


t1 = threading.Thread(target=deadlock_thread_1)
t2 = threading.Thread(target=deadlock_thread_2)
t1.start()
t2.start()
t1.join()
t2.join()

if deadlock_detected.is_set():
    print("\n  Deadlock was detected via timeout!")

# --- Fix: Consistent Lock Ordering ---
print("\n--- FIX: Consistent Lock Ordering ---")
print("Always acquire locks in the SAME order (A before B)")

lock_x = threading.Lock()
lock_y = threading.Lock()


def safe_thread_1():
    with lock_x:  # Always lock X first
        print("  Safe-Thread-1: acquired lock X")
        time.sleep(0.1)
        with lock_y:  # Then lock Y
            print("  Safe-Thread-1: acquired lock Y")
            print("  Safe-Thread-1: doing work with both locks")


def safe_thread_2():
    with lock_x:  # Same order: lock X first
        print("  Safe-Thread-2: acquired lock X")
        time.sleep(0.1)
        with lock_y:  # Then lock Y
            print("  Safe-Thread-2: acquired lock Y")
            print("  Safe-Thread-2: doing work with both locks")


t1 = threading.Thread(target=safe_thread_1)
t2 = threading.Thread(target=safe_thread_2)
t1.start()
t2.start()
t1.join()
t2.join()
print("\n  No deadlock! Both threads completed successfully.")

# --- Fix 2: Context Manager Lock Ordering ---
print("\n--- FIX 2: Ordered Lock Acquisition ---")


class OrderedLock:
    """Acquires multiple locks in a consistent order to prevent deadlock."""
    _global_id = 0
    _global_lock = threading.Lock()

    def __init__(self, name: str = ""):
        with OrderedLock._global_lock:
            self._id = OrderedLock._global_id
            OrderedLock._global_id += 1
        self._lock = threading.Lock()
        self.name = name or f"Lock-{self._id}"

    @staticmethod
    def acquire_all(*locks: 'OrderedLock'):
        """Acquire multiple locks in a consistent order (by ID)."""
        sorted_locks = sorted(locks, key=lambda l: l._id)
        for lock in sorted_locks:
            lock._lock.acquire()
            print(f"  Acquired {lock.name}")

    @staticmethod
    def release_all(*locks: 'OrderedLock'):
        """Release all locks in reverse order."""
        for lock in reversed(sorted(locks, key=lambda l: l._id)):
            lock._lock.release()


lock_p = OrderedLock("Resource-P")
lock_q = OrderedLock("Resource-Q")

OrderedLock.acquire_all(lock_q, lock_p)  # Order doesn't matter - sorted internally
print("  Both locks acquired safely!")
OrderedLock.release_all(lock_q, lock_p)
print("  Both locks released.")


# ============================================================
# 6. THREAD-SAFE SINGLETON
# ============================================================

section("6. Thread-Safe Singleton")

# --- Naive Singleton (NOT thread-safe) ---
print("--- Naive Singleton (Race Condition) ---")


class NaiveSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Race condition: two threads can both see _instance as None
            time.sleep(0.01)  # Simulate slow initialization
            cls._instance = super().__new__(cls)
            cls._instance.value = id(cls._instance)
        return cls._instance


instances_naive = []


def create_naive():
    instances_naive.append(id(NaiveSingleton()))


threads = [threading.Thread(target=create_naive) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

unique_naive = len(set(instances_naive))
print(f"  Created {len(instances_naive)} instances")
print(f"  Unique instances: {unique_naive}")
print(f"  Thread-safe: {'YES' if unique_naive == 1 else 'NO - multiple instances created!'}")

# --- Thread-Safe Singleton with Lock ---
print("\n--- Thread-Safe Singleton (Double-Checked Locking) ---")


class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:  # First check (no lock)
            with cls._lock:  # Acquire lock
                if cls._instance is None:  # Second check (with lock)
                    time.sleep(0.01)  # Simulate slow init
                    cls._instance = super().__new__(cls)
                    cls._instance.value = id(cls._instance)
        return cls._instance


instances_safe = []


def create_safe():
    instances_safe.append(id(ThreadSafeSingleton()))


threads = [threading.Thread(target=create_safe) for _ in range(5)]
for t in threads:
    t.start()
for t in threads:
    t.join()

unique_safe = len(set(instances_safe))
print(f"  Created {len(instances_safe)} instances")
print(f"  Unique instances: {unique_safe}")
print(f"  Thread-safe: {'YES - only one instance!' if unique_safe == 1 else 'NO'}")

# --- Pythonic Singleton with metaclass ---
print("\n--- Pythonic Singleton (Metaclass) ---")


class SingletonMeta(type):
    """Metaclass that ensures only one instance per class."""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]


class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, host: str = "localhost"):
        self.host = host
        self.connection_id = id(self)
        print(f"  Initializing DB connection to {host} (id: {self.connection_id})")

    def query(self, sql: str) -> str:
        return f"  Result from {self.host}: executed '{sql}'"


# Multiple calls return the same instance
db1 = DatabaseConnection("prod-db.example.com")
db2 = DatabaseConnection("other-db.example.com")  # __init__ NOT called again

print(f"  db1 is db2: {db1 is db2}")
print(f"  db1.host: {db1.host}")
print(f"  db2.host: {db2.host}")  # Same as db1!
print(db1.query("SELECT * FROM users"))


# ============================================================
# BONUS: ReadWriteLock
# ============================================================

section("BONUS: ReadWriteLock Pattern")


class ReadWriteLock:
    """Allows multiple concurrent readers OR one exclusive writer."""

    def __init__(self):
        self._readers = 0
        self._readers_lock = threading.Lock()
        self._write_lock = threading.Lock()

    def acquire_read(self):
        with self._readers_lock:
            self._readers += 1
            if self._readers == 1:
                self._write_lock.acquire()  # Block writers

    def release_read(self):
        with self._readers_lock:
            self._readers -= 1
            if self._readers == 0:
                self._write_lock.release()  # Allow writers

    def acquire_write(self):
        self._write_lock.acquire()

    def release_write(self):
        self._write_lock.release()


class SharedCache:
    """Thread-safe cache using ReadWriteLock."""

    def __init__(self):
        self._data = {}
        self._rwlock = ReadWriteLock()

    def read(self, key: str) -> str:
        self._rwlock.acquire_read()
        try:
            value = self._data.get(key, "NOT FOUND")
            print(f"  [{threading.current_thread().name}] Read {key}: {value}")
            time.sleep(0.05)  # Simulate slow read
            return value
        finally:
            self._rwlock.release_read()

    def write(self, key: str, value: str):
        self._rwlock.acquire_write()
        try:
            print(f"  [{threading.current_thread().name}] Writing {key}={value}")
            time.sleep(0.1)  # Simulate slow write
            self._data[key] = value
        finally:
            self._rwlock.release_write()


cache = SharedCache()
cache.write("config", "v1")

threads = []
# Multiple readers can read concurrently
for i in range(3):
    t = threading.Thread(target=cache.read, args=("config",), name=f"Reader-{i}")
    threads.append(t)

# Writer waits for all readers to finish
t = threading.Thread(target=cache.write, args=("config", "v2"), name="Writer-0")
threads.append(t)

for t in threads:
    t.start()
for t in threads:
    t.join()

print("\n  ReadWriteLock allows concurrent reads but exclusive writes")


# ============================================================
# SUMMARY
# ============================================================

section("SUMMARY: Concurrency Patterns")

patterns = [
    ("Race Condition", "Multiple threads modify shared state without synchronization",
     "Use Lock, atomic operations, or thread-safe data structures"),
    ("Lock / RLock", "Mutual exclusion - only one thread enters critical section",
     "RLock allows same thread to re-acquire (reentrant)"),
    ("Producer-Consumer", "Decouple production from consumption via queue",
     "Use queue.Queue (thread-safe, bounded, blocking)"),
    ("Thread Pool", "Reuse threads for multiple tasks",
     "Use ThreadPoolExecutor with submit() or map()"),
    ("Deadlock", "Two+ threads wait for each other's locks forever",
     "Fix: consistent lock ordering, timeouts, or lock hierarchy"),
    ("Thread-Safe Singleton", "Ensure only one instance across threads",
     "Double-checked locking or metaclass approach"),
    ("ReadWriteLock", "Allow concurrent reads, exclusive writes",
     "Multiple readers OR one writer, not both"),
]

for name, problem, solution in patterns:
    print(f"  {name}")
    print(f"    Problem:  {problem}")
    print(f"    Solution: {solution}")
    print()

print("Key rules for thread safety:")
print("  1. Minimize shared mutable state")
print("  2. Lock the smallest scope necessary")
print("  3. Always acquire locks in consistent order")
print("  4. Prefer higher-level constructs (Queue, ThreadPoolExecutor)")
print("  5. Use 'with' statement for locks (auto-release on exception)")
