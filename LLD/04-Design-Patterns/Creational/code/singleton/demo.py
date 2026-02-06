"""Demo: All four Singleton variants."""

from singleton_naive import NaiveSingleton
from singleton_metaclass import MetaSingleton
from singleton_thread_safe import ThreadSafeSingleton
from singleton_decorator import AppConfig


def main():
    print("=" * 50)
    print("SINGLETON PATTERN - 4 Variants")
    print("=" * 50)

    # 1. Naive
    print("\n--- Naive Singleton ---")
    n1, n2 = NaiveSingleton(), NaiveSingleton()
    n1.value = "naive"
    print(f"Same? {n1 is n2} | value: {n2.value}")

    # 2. Metaclass
    print("\n--- Metaclass Singleton ---")
    m1, m2 = MetaSingleton(), MetaSingleton()
    m1.value = "meta"
    print(f"Same? {m1 is m2} | value: {m2.value}")

    # 3. Thread-safe
    print("\n--- Thread-Safe Singleton ---")
    t1, t2 = ThreadSafeSingleton(), ThreadSafeSingleton()
    t1.value = "safe"
    print(f"Same? {t1 is t2} | value: {t2.value}")

    # 4. Decorator
    print("\n--- Decorator Singleton ---")
    c1, c2 = AppConfig(), AppConfig()
    c1.set("env", "prod")
    print(f"Same? {c1 is c2} | env: {c2.get('env')}")

    print("\n" + "=" * 50)
    print("All variants guarantee a single instance!")


if __name__ == "__main__":
    main()
