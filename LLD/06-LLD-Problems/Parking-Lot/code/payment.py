"""
Payment classes for the Parking Lot system.
Uses the Strategy pattern: PaymentStrategy base with concrete implementations.
"""

from abc import ABC, abstractmethod
from datetime import timedelta

from enums import PaymentStatus
from parking_ticket import ParkingTicket


class PaymentStrategy(ABC):
    """Abstract base for all payment methods (Strategy pattern)."""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """Process a payment of the given amount. Returns True on success."""
        pass


class CreditCardPayment(PaymentStrategy):
    """Pay via credit card."""

    def __init__(self, card_number: str) -> None:
        self._card_number = card_number

    def pay(self, amount: float) -> bool:
        print(f"    [Payment] Charged ${amount:.2f} to Credit Card ending {self._card_number[-4:]}")
        return True


class CashPayment(PaymentStrategy):
    """Pay with cash."""

    def pay(self, amount: float) -> bool:
        print(f"    [Payment] Received ${amount:.2f} in Cash")
        return True


class UPIPayment(PaymentStrategy):
    """Pay via UPI."""

    def __init__(self, upi_id: str) -> None:
        self._upi_id = upi_id

    def pay(self, amount: float) -> bool:
        print(f"    [Payment] Charged ${amount:.2f} via UPI ({self._upi_id})")
        return True


class PaymentProcessor:
    """Processes payment for a parking ticket using a given strategy."""

    def __init__(self, ticket: ParkingTicket, strategy: PaymentStrategy) -> None:
        self._ticket = ticket
        self._strategy = strategy
        self.status: PaymentStatus = PaymentStatus.PENDING

    def process(self, simulated_hours: int = 1) -> bool:
        """Simulate time passage, calculate fee, and process payment."""
        self._ticket.exit_time = self._ticket.entry_time + timedelta(hours=simulated_hours)
        amount = self._ticket.calculate_fee(self._ticket.exit_time)
        if self._strategy.pay(amount):
            self._ticket.mark_paid(amount)
            self.status = PaymentStatus.COMPLETED
            return True
        self.status = PaymentStatus.FAILED
        return False
