"""
Decorator Pattern - Attaches additional responsibilities to objects
dynamically. Provides a flexible alternative to subclassing.

Examples:
1. Coffee Shop: Base coffee + decorators (Milk, Sugar, etc.)
2. Logger decorator for functions
"""
from abc import ABC, abstractmethod
import functools
import time


# --- Coffee Shop ---
class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass


class Espresso(Coffee):
    def cost(self) -> float:
        return 2.00

    def description(self) -> str:
        return "Espresso"


class Americano(Coffee):
    def cost(self) -> float:
        return 2.50

    def description(self) -> str:
        return "Americano"


class CoffeeDecorator(Coffee, ABC):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee


class Milk(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.50

    def description(self) -> str:
        return self._coffee.description() + " + Milk"


class Sugar(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.25

    def description(self) -> str:
        return self._coffee.description() + " + Sugar"


class WhippedCream(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.75

    def description(self) -> str:
        return self._coffee.description() + " + Whipped Cream"


class Caramel(CoffeeDecorator):
    def cost(self) -> float:
        return self._coffee.cost() + 0.60

    def description(self) -> str:
        return self._coffee.description() + " + Caramel"


# --- Function Logger Decorator ---
def logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"    [LOG] Calling {func.__name__}({args}, {kwargs})")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"    [LOG] {func.__name__} returned {result} in {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"    [RETRY] Attempt {attempt}/{max_attempts} failed: {e}")
            raise Exception(f"All {max_attempts} attempts failed")
        return wrapper
    return decorator


@logger
def add(a, b):
    return a + b


call_count = 0

@retry(max_attempts=3)
@logger
def flaky_api_call():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("Server unavailable")
    return {"data": "success"}


if __name__ == "__main__":
    print("=" * 60)
    print("DECORATOR PATTERN DEMO")
    print("=" * 60)

    # Coffee orders
    print("\n--- Coffee Shop ---")
    orders = [
        Espresso(),
        Milk(Espresso()),
        Caramel(WhippedCream(Milk(Espresso()))),
        Sugar(Sugar(Milk(Americano()))),
    ]
    for coffee in orders:
        print(f"  {coffee.description()}")
        print(f"    -> ${coffee.cost():.2f}")

    # Function decorators
    print("\n--- Logger Decorator ---")
    add(3, 5)

    print("\n--- Retry + Logger Decorator ---")
    call_count = 0
    result = flaky_api_call()
    print(f"    Final result: {result}")
