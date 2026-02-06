"""UPI payment strategy."""

from strategy import PaymentStrategy


class UPIPayment(PaymentStrategy):
    def __init__(self, upi_id: str):
        self._upi_id = upi_id

    def validate(self) -> bool:
        return "@" in self._upi_id

    def pay(self, amount: float) -> str:
        return f"Paid ${amount:.2f} via UPI ({self._upi_id})"
