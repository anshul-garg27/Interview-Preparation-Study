"""Stock - concrete subject that observers watch."""

from subject import Subject


class Stock(Subject):
    """A stock whose price changes notify observers."""

    def __init__(self, symbol: str, price: float):
        super().__init__()
        self._symbol = symbol
        self._price = price

    @property
    def symbol(self):
        return self._symbol

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price: float):
        old_price = self._price
        self._price = new_price
        if old_price != new_price:
            print(f"\n  [{self._symbol}] Price: ${old_price:.2f} -> ${new_price:.2f}")
            self.notify(self._symbol, new_price)
