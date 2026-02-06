"""
Singleton Pattern - Ensures a class has only one instance.

Four implementations:
1. Naive Singleton (not thread-safe)
2. Thread-safe Singleton (with lock)
3. Metaclass Singleton
4. Decorator Singleton

Demo: DatabaseConnection pool that only creates one connection.
"""
import threading


# --- 1. Naive Singleton ---
class NaiveSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


# --- 2. Thread-Safe Singleton ---
class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:  # Double-checked locking
                    cls._instance = super().__new__(cls)
        return cls._instance


# --- 3. Metaclass Singleton ---
class SingletonMeta(type):
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class MetaSingleton(metaclass=SingletonMeta):
    pass


# --- 4. Decorator Singleton ---
def singleton(cls):
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


# --- Practical Example: Database Connection ---
class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        self.host = "localhost"
        self.port = 5432
        self.connected = True
        print(f"  [DB] New connection created to {self.host}:{self.port}")

    def query(self, sql):
        return f"  [DB] Executing: {sql}"


@singleton
class ConfigManager:
    def __init__(self):
        self.settings = {"theme": "dark", "language": "en"}
        print(f"  [Config] Loaded settings: {self.settings}")


if __name__ == "__main__":
    print("=" * 60)
    print("SINGLETON PATTERN DEMO")
    print("=" * 60)

    # 1. Naive Singleton
    print("\n1. Naive Singleton:")
    a = NaiveSingleton()
    b = NaiveSingleton()
    print(f"  Instance A id: {id(a)}")
    print(f"  Instance B id: {id(b)}")
    print(f"  Same instance? {a is b}")

    # 2. Thread-Safe Singleton
    print("\n2. Thread-Safe Singleton:")
    results = []

    def create_instance():
        results.append(ThreadSafeSingleton())

    threads = [threading.Thread(target=create_instance) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"  All 5 threads got same instance? {len(set(id(r) for r in results)) == 1}")

    # 3. Metaclass Singleton
    print("\n3. Metaclass Singleton:")
    c = MetaSingleton()
    d = MetaSingleton()
    print(f"  Same instance? {c is d}")

    # 4. Decorator Singleton
    print("\n4. Decorator Singleton (ConfigManager):")
    cfg1 = ConfigManager()
    cfg2 = ConfigManager()
    print(f"  Same instance? {cfg1 is cfg2}")

    # Practical: Database Connection
    print("\n5. Database Connection Singleton:")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"  Same connection? {db1 is db2}")
    print(db1.query("SELECT * FROM users"))
