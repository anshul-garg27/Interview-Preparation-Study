"""OrderItem - snapshot of a product at time of purchase."""

from product import Product


class OrderItem:
    """Immutable record of a product in an order."""

    def __init__(self, product: Product, quantity: int, price_at_purchase: float):
        self.product = product
        self.quantity = quantity
        self.price_at_purchase = price_at_purchase

    @property
    def subtotal(self) -> float:
        return self.price_at_purchase * self.quantity

    def __repr__(self) -> str:
        return f"{self.product.name} x{self.quantity} = ${self.subtotal:.2f}"
