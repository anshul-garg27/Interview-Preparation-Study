"""PayPal payment strategy."""

from strategy import PaymentStrategy


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self._email = email

    def validate(self) -> bool:
        return "@" in self._email

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via PayPal ({self._email})"
