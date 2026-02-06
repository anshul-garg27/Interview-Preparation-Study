"""Abstraction - Real-world: Abstract PaymentProcessor with multiple implementations."""

from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    """Abstract payment interface - hides complexity of each payment method."""

    @abstractmethod
    def validate(self, amount: float) -> bool:
        pass

    @abstractmethod
    def process(self, amount: float) -> str:
        pass

    def pay(self, amount: float) -> str:
        """Template method: validate then process."""
        if not self.validate(amount):
            return f"FAILED: Invalid payment of ${amount:.2f}"
        return self.process(amount)


class CreditCardProcessor(PaymentProcessor):
    def __init__(self, card_number: str):
        self.card_number = card_number

    def validate(self, amount: float) -> bool:
        return amount > 0 and len(self.card_number) == 16

    def process(self, amount: float) -> str:
        masked = "****" + self.card_number[-4:]
        return f"Charged ${amount:.2f} to credit card {masked}"


class PayPalProcessor(PaymentProcessor):
    def __init__(self, email: str):
        self.email = email

    def validate(self, amount: float) -> bool:
        return amount > 0 and "@" in self.email

    def process(self, amount: float) -> str:
        return f"Sent ${amount:.2f} via PayPal to {self.email}"


class UPIProcessor(PaymentProcessor):
    def __init__(self, upi_id: str):
        self.upi_id = upi_id

    def validate(self, amount: float) -> bool:
        return amount > 0 and "@" in self.upi_id

    def process(self, amount: float) -> str:
        return f"Transferred ${amount:.2f} via UPI to {self.upi_id}"


def checkout(processor: PaymentProcessor, amount: float) -> None:
    """Client code only knows about the abstract PaymentProcessor."""
    print(f"  {processor.pay(amount)}")


if __name__ == "__main__":
    print("=== Abstract PaymentProcessor ===\n")

    processors: list[PaymentProcessor] = [
        CreditCardProcessor("1234567890123456"),
        PayPalProcessor("alice@example.com"),
        UPIProcessor("alice@upi"),
    ]

    for proc in processors:
        checkout(proc, 49.99)

    # Validation failure
    print("\n--- Validation Failures ---")
    bad_card = CreditCardProcessor("123")  # Too short
    checkout(bad_card, 49.99)
