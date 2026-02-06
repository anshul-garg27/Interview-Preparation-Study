"""ShoppingCart context that uses a payment strategy."""

from strategy import PaymentStrategy


class ShoppingCart:
    """Context that delegates payment to a strategy."""

    def __init__(self):
        self._items: list[tuple[str, float]] = []
        self._strategy: PaymentStrategy = None

    def add_item(self, name: str, price: float):
        self._items.append((name, price))

    def get_total(self) -> float:
        return sum(price for _, price in self._items)

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def checkout(self) -> str:
        if not self._strategy:
            return "No payment method set"
        if not self._strategy.validate():
            return "Payment validation failed"
        return self._strategy.pay(self.get_total())
