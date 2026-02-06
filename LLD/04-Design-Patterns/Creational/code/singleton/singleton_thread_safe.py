"""Thread-safe Singleton with double-checked locking."""

import threading


class ThreadSafeSingleton:
    """Singleton safe for multi-threaded environments."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Double-checked locking
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.value = None

    def __repr__(self):
        return f"ThreadSafeSingleton(value={self.value}, id={id(self)})"


if __name__ == "__main__":
    results = []

    def create():
        s = ThreadSafeSingleton()
        results.append(id(s))

    threads = [threading.Thread(target=create) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"All same instance: {len(set(results)) == 1}")
    print(f"Unique IDs: {set(results)}")
