"""OCP Fixed - Open for extension, closed for modification."""

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Abstract discount - new types extend, don't modify."""

    @abstractmethod
    def calculate(self, amount: float) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class RegularDiscount(DiscountStrategy):
    @property
    def name(self) -> str:
        return "Regular"

    def calculate(self, amount: float) -> float:
        return 0.0


class SilverDiscount(DiscountStrategy):
    @property
    def name(self) -> str:
        return "Silver"

    def calculate(self, amount: float) -> float:
        return amount * 0.10


class GoldDiscount(DiscountStrategy):
    @property
    def name(self) -> str:
        return "Gold"

    def calculate(self, amount: float) -> float:
        return amount * 0.20


# Adding new type - ZERO changes to existing code!
class PlatinumDiscount(DiscountStrategy):
    @property
    def name(self) -> str:
        return "Platinum"

    def calculate(self, amount: float) -> float:
        return amount * 0.35


class DiscountCalculator:
    """CLOSED for modification - never needs to change."""

    def apply(self, strategy: DiscountStrategy, amount: float) -> float:
        return strategy.calculate(amount)


if __name__ == "__main__":
    print("GOOD DESIGN: Open/Closed Principle\n")

    calc = DiscountCalculator()
    amount = 100.0

    strategies = [RegularDiscount(), SilverDiscount(), GoldDiscount(), PlatinumDiscount()]
    for s in strategies:
        discount = calc.apply(s, amount)
        print(f"  {s.name:10s}: ${amount:.0f} - ${discount:.0f} = ${amount - discount:.0f}")

    print("\nBENEFITS:")
    print("  1. Added Platinum WITHOUT modifying existing code")
    print("  2. Each discount is isolated and testable")
    print("  3. No if/elif chain to maintain")
    print("  4. DiscountCalculator never changes")
