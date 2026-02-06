"""Dependency Injection - Constructor injection for testability."""

from abc import ABC, abstractmethod


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float) -> str:
        pass


class StripeGateway(PaymentGateway):
    def charge(self, amount: float) -> str:
        return f"Stripe charged ${amount:.2f}"


class PayPalGateway(PaymentGateway):
    def charge(self, amount: float) -> str:
        return f"PayPal charged ${amount:.2f}"


class Logger(ABC):
    @abstractmethod
    def log(self, msg: str) -> None:
        pass


class ConsoleLogger(Logger):
    def log(self, msg: str) -> None:
        print(f"  [LOG] {msg}")


class MockLogger(Logger):
    def __init__(self):
        self.messages: list[str] = []

    def log(self, msg: str) -> None:
        self.messages.append(msg)


class OrderService:
    """All dependencies injected via constructor - fully testable."""

    def __init__(self, payment: PaymentGateway, logger: Logger):
        self._payment = payment
        self._logger = logger

    def place_order(self, item: str, amount: float) -> str:
        self._logger.log(f"Placing order for {item}")
        result = self._payment.charge(amount)
        self._logger.log(f"Payment: {result}")
        return f"Order '{item}' complete. {result}"


if __name__ == "__main__":
    print("=== Dependency Injection ===\n")

    # Production setup
    print("--- Production ---")
    prod_service = OrderService(StripeGateway(), ConsoleLogger())
    print(prod_service.place_order("Laptop", 999.99))

    # Different provider, same service
    print("\n--- Different Provider ---")
    paypal_service = OrderService(PayPalGateway(), ConsoleLogger())
    print(paypal_service.place_order("Mouse", 29.99))

    # Testing setup - no real payments, no console output
    print("\n--- Testing ---")
    mock_logger = MockLogger()

    class MockPayment(PaymentGateway):
        def charge(self, amount: float) -> str:
            return f"MOCK charged ${amount:.2f}"

    test_service = OrderService(MockPayment(), mock_logger)
    result = test_service.place_order("Test Item", 10.00)
    print(f"  Result: {result}")
    print(f"  Logged: {mock_logger.messages}")
    print("\n  No real payments made. No console logs. Fully isolated test.")
