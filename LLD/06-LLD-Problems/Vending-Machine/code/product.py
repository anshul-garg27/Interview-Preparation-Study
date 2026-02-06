"""Product sold by the vending machine."""


class Product:
    """A product with a code, name, and price."""

    def __init__(self, code: str, name: str, price: float):
        self.code = code
        self.name = name
        self.price = price

    def __repr__(self) -> str:
        return f"{self.code}: {self.name} (${self.price:.2f})"
