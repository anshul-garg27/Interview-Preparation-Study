"""Payment strategies for BookMyShow (Strategy Pattern)."""

from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """Abstract payment method."""

    @abstractmethod
    def pay(self, amount: float, user_name: str) -> bool:
        """Process payment. Returns True on success."""
        pass


class CreditCardPayment(PaymentStrategy):
    """Pay via credit card."""

    def pay(self, amount: float, user_name: str) -> bool:
        print(f"      [Payment] {user_name}: ${amount:.2f} charged to Credit Card")
        return True


class UPIPayment(PaymentStrategy):
    """Pay via UPI."""

    def pay(self, amount: float, user_name: str) -> bool:
        print(f"      [Payment] {user_name}: ${amount:.2f} charged via UPI")
        return True


class WalletPayment(PaymentStrategy):
    """Pay via digital wallet."""

    def pay(self, amount: float, user_name: str) -> bool:
        print(f"      [Payment] {user_name}: ${amount:.2f} deducted from Wallet")
        return True
