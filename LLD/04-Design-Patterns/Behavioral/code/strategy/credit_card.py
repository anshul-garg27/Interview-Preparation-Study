"""CreditCard payment strategy."""

from strategy import PaymentStrategy


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, name: str):
        self._card_number = card_number
        self._name = name

    def validate(self) -> bool:
        return len(self._card_number) == 16 and self._card_number.isdigit()

    def pay(self, amount: float) -> str:
        last4 = self._card_number[-4:]
        return f"Paid ${amount:.2f} via Credit Card ending in {last4}"
