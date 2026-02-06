"""Payment processing for rides."""

from enums import PaymentMethod


class Payment:
    """Represents a payment transaction for a ride."""

    def __init__(self, ride_id: str, amount: float, method: PaymentMethod):
        self.ride_id = ride_id
        self.amount = amount
        self.method = method
        self.is_completed = False

    def process(self) -> bool:
        """Process the payment and mark as completed."""
        self.is_completed = True
        print(f"    [Payment] Ride {self.ride_id}: ${self.amount:.2f} via {self.method.value}")
        return True

    def __repr__(self) -> str:
        status = "Completed" if self.is_completed else "Pending"
        return f"Payment({self.ride_id}, ${self.amount:.2f}, {status})"
