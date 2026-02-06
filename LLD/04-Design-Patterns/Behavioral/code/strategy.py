"""
Strategy Pattern - Defines a family of algorithms, encapsulates each one,
and makes them interchangeable at runtime.

Examples:
1. Payment strategies: CreditCard, PayPal, Bitcoin, UPI
2. Sorting strategies: BubbleSort, QuickSort, MergeSort
3. Navigation strategies: Car, Walking, PublicTransport
"""
from abc import ABC, abstractmethod


# --- Payment Strategies ---
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


class CreditCard(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card = card_number[-4:]

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via Credit Card ****{self.card}"


class PayPal(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via PayPal ({self.email})"


class Bitcoin(PaymentStrategy):
    def __init__(self, wallet: str):
        self.wallet = wallet[:8]

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via Bitcoin (wallet: {self.wallet}...)"


class UPI(PaymentStrategy):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via UPI ({self.upi_id})"


class PaymentContext:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def checkout(self, amount: float) -> str:
        return self._strategy.pay(amount)


# --- Sorting Strategies ---
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class BubbleSort(SortStrategy):
    def sort(self, data: list) -> list:
        arr = list(data)
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    def name(self) -> str:
        return "BubbleSort O(n^2)"


class QuickSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        mid = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)

    def name(self) -> str:
        return "QuickSort O(n log n)"


class MergeSort(SortStrategy):
    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)

    def _merge(self, left, right):
        result, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i]); i += 1
            else:
                result.append(right[j]); j += 1
        return result + left[i:] + right[j:]

    def name(self) -> str:
        return "MergeSort O(n log n)"


# --- Navigation Strategies ---
class RouteStrategy(ABC):
    @abstractmethod
    def calculate(self, start: str, end: str) -> str:
        pass


class CarRoute(RouteStrategy):
    def calculate(self, start, end):
        return f"  Car: {start} -> Highway -> {end} (25 min, 15 km)"


class WalkingRoute(RouteStrategy):
    def calculate(self, start, end):
        return f"  Walk: {start} -> Park Path -> {end} (90 min, 5 km)"


class PublicTransport(RouteStrategy):
    def calculate(self, start, end):
        return f"  Bus: {start} -> Route 42 -> Metro -> {end} (45 min, 12 km)"


if __name__ == "__main__":
    print("=" * 60)
    print("STRATEGY PATTERN DEMO")
    print("=" * 60)

    # Payment
    print("\n--- Payment Strategies ---")
    ctx = PaymentContext(CreditCard("4111111111111234"))
    print(f"  {ctx.checkout(99.99)}")
    ctx.set_strategy(PayPal("user@email.com"))
    print(f"  {ctx.checkout(49.50)}")
    ctx.set_strategy(Bitcoin("1A2b3C4d5E6f7G8h"))
    print(f"  {ctx.checkout(0.005)}")
    ctx.set_strategy(UPI("user@upi"))
    print(f"  {ctx.checkout(500.00)}")

    # Sorting
    print("\n--- Sorting Strategies ---")
    data = [64, 34, 25, 12, 22, 11, 90]
    for strategy in [BubbleSort(), QuickSort(), MergeSort()]:
        result = strategy.sort(data)
        print(f"  {strategy.name()}: {data} -> {result}")

    # Navigation
    print("\n--- Navigation Strategies ---")
    for route in [CarRoute(), WalkingRoute(), PublicTransport()]:
        print(route.calculate("Home", "Office"))
