"""Strategy Pattern: Payment processors for different methods."""

from abc import ABC, abstractmethod
from enums import PaymentMethod


class PaymentProcessor(ABC):
    """Abstract payment processing strategy."""

    @abstractmethod
    def process(self, amount: float, user_name: str) -> bool:
        pass


class CreditCardProcessor(PaymentProcessor):
    """Process payment via credit card."""

    def process(self, amount: float, user_name: str) -> bool:
        print(f"      [Payment] {user_name}: ${amount:.2f} via Credit Card")
        return True


class UPIProcessor(PaymentProcessor):
    """Process payment via UPI."""

    def process(self, amount: float, user_name: str) -> bool:
        print(f"      [Payment] {user_name}: ${amount:.2f} via UPI")
        return True


class CODProcessor(PaymentProcessor):
    """Cash on delivery - payment collected at doorstep."""

    def process(self, amount: float, user_name: str) -> bool:
        print(f"      [Payment] {user_name}: ${amount:.2f} Cash on Delivery")
        return True


class PaymentFactory:
    """Factory for creating payment processors."""

    _processors = {
        PaymentMethod.CREDIT_CARD: CreditCardProcessor,
        PaymentMethod.UPI: UPIProcessor,
        PaymentMethod.COD: CODProcessor,
    }

    @staticmethod
    def create(method: PaymentMethod) -> PaymentProcessor:
        cls = PaymentFactory._processors.get(method)
        if not cls:
            raise ValueError(f"Unsupported payment method: {method}")
        return cls()
