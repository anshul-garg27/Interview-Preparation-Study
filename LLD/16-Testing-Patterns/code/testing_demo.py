"""
Testing Patterns Demo
=====================
Runnable examples demonstrating:
1. Basic unit test structure (AAA pattern)
2. Mocking a dependency
3. TDD example (Red-Green-Refactor for a Stack)
4. Testing a Strategy pattern with mocked strategies

Run with:  python -m pytest testing_demo.py -v
    or:    python testing_demo.py
"""

import unittest
from unittest.mock import Mock, MagicMock, patch
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


# ============================================================
# PRODUCTION CODE — Classes we will test
# ============================================================

# --- Simple Calculator (for basic unit test demo) ---

class Calculator:
    """A simple calculator for demonstrating unit tests."""

    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


# --- Payment system (for mocking demo) ---

class PaymentGateway(ABC):
    """Interface for payment processing."""
    @abstractmethod
    def charge(self, card_token: str, amount: float) -> dict:
        pass


class PaymentService:
    """Service that uses a PaymentGateway dependency."""

    def __init__(self, gateway: PaymentGateway):
        self._gateway = gateway

    def process_payment(self, card_token: str, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if not card_token:
            raise ValueError("Card token is required")

        result = self._gateway.charge(card_token, amount)

        if result.get("status") == "success":
            return result["transaction_id"]
        else:
            raise RuntimeError(f"Payment failed: {result.get('error', 'Unknown')}")


# --- Stack (for TDD demo) ---

class Stack:
    """A stack built using TDD (Red-Green-Refactor)."""

    def __init__(self):
        self._items: list = []

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def push(self, item) -> None:
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek at empty stack")
        return self._items[-1]

    def size(self) -> int:
        return len(self._items)


# --- Strategy pattern (for strategy + mock testing demo) ---

class DiscountStrategy(ABC):
    """Strategy interface for discount calculation."""
    @abstractmethod
    def calculate(self, price: float) -> float:
        """Returns the discounted price."""
        pass


class NoDiscount(DiscountStrategy):
    def calculate(self, price: float) -> float:
        return price


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self._percent = percent

    def calculate(self, price: float) -> float:
        return price * (1 - self._percent / 100)


class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        if amount < 0:
            raise ValueError("Discount amount cannot be negative")
        self._amount = amount

    def calculate(self, price: float) -> float:
        return max(0, price - self._amount)


@dataclass
class Product:
    name: str
    price: float


class PriceCalculator:
    """Uses a DiscountStrategy to compute the final price."""

    def __init__(self, strategy: DiscountStrategy):
        self._strategy = strategy

    def compute_total(self, products: list[Product]) -> float:
        total = sum(p.price for p in products)
        return round(self._strategy.calculate(total), 2)

    def set_strategy(self, strategy: DiscountStrategy):
        self._strategy = strategy


# ============================================================
# TESTS
# ============================================================

# --- 1. Basic Unit Tests (AAA Pattern) ---

class TestCalculator(unittest.TestCase):
    """Demonstrates the AAA (Arrange, Act, Assert) pattern."""

    def setUp(self):
        """Arrange: runs before every test method."""
        self.calc = Calculator()

    def test_add_positive_numbers(self):
        # Act
        result = self.calc.add(2, 3)
        # Assert
        self.assertEqual(result, 5)

    def test_add_negative_numbers(self):
        result = self.calc.add(-1, -2)
        self.assertEqual(result, -3)

    def test_add_zero(self):
        result = self.calc.add(0, 0)
        self.assertEqual(result, 0)

    def test_subtract(self):
        result = self.calc.subtract(10, 3)
        self.assertEqual(result, 7)

    def test_multiply(self):
        result = self.calc.multiply(4, 5)
        self.assertEqual(result, 20)

    def test_divide_normal(self):
        result = self.calc.divide(10, 2)
        self.assertEqual(result, 5.0)

    def test_divide_by_zero_raises_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.calc.divide(10, 0)
        self.assertEqual(str(ctx.exception), "Cannot divide by zero")

    def test_divide_result_is_float(self):
        result = self.calc.divide(7, 2)
        self.assertAlmostEqual(result, 3.5)


# --- 2. Mocking Dependencies ---

class TestPaymentService(unittest.TestCase):
    """Demonstrates mocking an external dependency (PaymentGateway)."""

    def setUp(self):
        # Create a mock that respects the PaymentGateway interface
        self.mock_gateway = Mock(spec=PaymentGateway)
        self.service = PaymentService(self.mock_gateway)

    def test_successful_payment(self):
        # Arrange: configure mock to return success
        self.mock_gateway.charge.return_value = {
            "status": "success",
            "transaction_id": "TXN-42"
        }

        # Act
        txn_id = self.service.process_payment("card_abc", 99.99)

        # Assert: correct result
        self.assertEqual(txn_id, "TXN-42")
        # Assert: gateway was called with correct arguments
        self.mock_gateway.charge.assert_called_once_with("card_abc", 99.99)

    def test_failed_payment_raises_error(self):
        self.mock_gateway.charge.return_value = {
            "status": "failed",
            "error": "Insufficient funds"
        }

        with self.assertRaises(RuntimeError) as ctx:
            self.service.process_payment("card_abc", 50.00)

        self.assertIn("Insufficient funds", str(ctx.exception))

    def test_zero_amount_raises_without_calling_gateway(self):
        with self.assertRaises(ValueError):
            self.service.process_payment("card_abc", 0)

        # Gateway should NOT be called for invalid input
        self.mock_gateway.charge.assert_not_called()

    def test_negative_amount_raises(self):
        with self.assertRaises(ValueError):
            self.service.process_payment("card_abc", -10)

        self.mock_gateway.charge.assert_not_called()

    def test_empty_card_token_raises(self):
        with self.assertRaises(ValueError):
            self.service.process_payment("", 50.00)

        self.mock_gateway.charge.assert_not_called()

    def test_gateway_called_exactly_once(self):
        """Verify the gateway is not called multiple times."""
        self.mock_gateway.charge.return_value = {
            "status": "success",
            "transaction_id": "TXN-1"
        }

        self.service.process_payment("card_x", 25.00)

        self.assertEqual(self.mock_gateway.charge.call_count, 1)


# --- 3. TDD Example: Stack Tests ---

class TestStack(unittest.TestCase):
    """Tests written in TDD order (each test was RED before implementation)."""

    # TDD Step 1: New stack is empty
    def test_new_stack_is_empty(self):
        stack = Stack()
        self.assertTrue(stack.is_empty())

    # TDD Step 2: Stack not empty after push
    def test_not_empty_after_push(self):
        stack = Stack()
        stack.push(42)
        self.assertFalse(stack.is_empty())

    # TDD Step 3: Pop returns last pushed item
    def test_pop_returns_last_pushed(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        self.assertEqual(stack.pop(), 3)

    # TDD Step 4: Pop on empty stack raises
    def test_pop_empty_raises(self):
        stack = Stack()
        with self.assertRaises(IndexError) as ctx:
            stack.pop()
        self.assertEqual(str(ctx.exception), "pop from empty stack")

    # TDD Step 5: Peek returns top without removing
    def test_peek_returns_top(self):
        stack = Stack()
        stack.push(10)
        self.assertEqual(stack.peek(), 10)
        self.assertFalse(stack.is_empty())  # Item still there

    # TDD Step 6: Peek on empty raises
    def test_peek_empty_raises(self):
        stack = Stack()
        with self.assertRaises(IndexError):
            stack.peek()

    # TDD Step 7: Size tracking
    def test_size(self):
        stack = Stack()
        self.assertEqual(stack.size(), 0)
        stack.push("a")
        self.assertEqual(stack.size(), 1)
        stack.push("b")
        self.assertEqual(stack.size(), 2)
        stack.pop()
        self.assertEqual(stack.size(), 1)

    # TDD Step 8: LIFO order verification
    def test_lifo_order(self):
        stack = Stack()
        for i in range(5):
            stack.push(i)
        results = [stack.pop() for _ in range(5)]
        self.assertEqual(results, [4, 3, 2, 1, 0])


# --- 4. Testing Strategy Pattern with Mocked Strategies ---

class TestDiscountStrategies(unittest.TestCase):
    """Test individual strategy implementations."""

    def test_no_discount(self):
        strategy = NoDiscount()
        self.assertEqual(strategy.calculate(100), 100)

    def test_percentage_discount_10_percent(self):
        strategy = PercentageDiscount(10)
        self.assertEqual(strategy.calculate(100), 90.0)

    def test_percentage_discount_50_percent(self):
        strategy = PercentageDiscount(50)
        self.assertEqual(strategy.calculate(200), 100.0)

    def test_percentage_discount_invalid_raises(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(110)  # Over 100%

    def test_flat_discount(self):
        strategy = FlatDiscount(15)
        self.assertEqual(strategy.calculate(100), 85)

    def test_flat_discount_exceeds_price(self):
        strategy = FlatDiscount(200)
        self.assertEqual(strategy.calculate(100), 0)  # Should not go negative

    def test_flat_discount_negative_raises(self):
        with self.assertRaises(ValueError):
            FlatDiscount(-5)


class TestPriceCalculatorWithMock(unittest.TestCase):
    """Test PriceCalculator by mocking the strategy dependency."""

    def test_compute_total_delegates_to_strategy(self):
        # Arrange: mock strategy returns a fixed value
        mock_strategy = Mock(spec=DiscountStrategy)
        mock_strategy.calculate.return_value = 80.0

        calculator = PriceCalculator(mock_strategy)
        products = [Product("A", 50), Product("B", 50)]

        # Act
        total = calculator.compute_total(products)

        # Assert: strategy was called with the sum of prices
        mock_strategy.calculate.assert_called_once_with(100)
        self.assertEqual(total, 80.0)

    def test_strategy_can_be_swapped(self):
        # Start with no discount
        mock_no_discount = Mock(spec=DiscountStrategy)
        mock_no_discount.calculate.return_value = 100.0

        calculator = PriceCalculator(mock_no_discount)
        products = [Product("Widget", 100)]

        self.assertEqual(calculator.compute_total(products), 100.0)

        # Swap to a discount strategy
        mock_sale = Mock(spec=DiscountStrategy)
        mock_sale.calculate.return_value = 70.0

        calculator.set_strategy(mock_sale)
        self.assertEqual(calculator.compute_total(products), 70.0)

    def test_empty_product_list(self):
        mock_strategy = Mock(spec=DiscountStrategy)
        mock_strategy.calculate.return_value = 0.0

        calculator = PriceCalculator(mock_strategy)
        total = calculator.compute_total([])

        mock_strategy.calculate.assert_called_once_with(0)
        self.assertEqual(total, 0.0)

    def test_strategy_called_with_correct_total(self):
        """Spy-like verification: ensure the total passed to strategy is correct."""
        received_totals = []

        def capture_total(price):
            received_totals.append(price)
            return price  # No discount

        mock_strategy = Mock(spec=DiscountStrategy)
        mock_strategy.calculate.side_effect = capture_total

        calculator = PriceCalculator(mock_strategy)
        products = [Product("A", 10.5), Product("B", 20.5), Product("C", 30.0)]

        calculator.compute_total(products)

        self.assertEqual(len(received_totals), 1)
        self.assertAlmostEqual(received_totals[0], 61.0)


class TestPriceCalculatorIntegration(unittest.TestCase):
    """Integration tests using real strategy implementations (no mocks)."""

    def test_with_percentage_discount(self):
        calculator = PriceCalculator(PercentageDiscount(20))
        products = [Product("Laptop", 1000), Product("Mouse", 50)]
        total = calculator.compute_total(products)
        self.assertEqual(total, 840.0)  # 1050 * 0.8

    def test_with_flat_discount(self):
        calculator = PriceCalculator(FlatDiscount(100))
        products = [Product("Laptop", 1000), Product("Mouse", 50)]
        total = calculator.compute_total(products)
        self.assertEqual(total, 950.0)  # 1050 - 100

    def test_with_no_discount(self):
        calculator = PriceCalculator(NoDiscount())
        products = [Product("Book", 15.99)]
        total = calculator.compute_total(products)
        self.assertEqual(total, 15.99)


# ============================================================
# RUN TESTS
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  Testing Patterns Demo")
    print("  Run with: python -m pytest testing_demo.py -v")
    print("=" * 60)
    print()

    # Run all tests
    unittest.main(verbosity=2)
