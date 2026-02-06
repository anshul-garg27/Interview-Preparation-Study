"""CartItem class - a product with quantity in a shopping cart."""

from product import Product


class CartItem:
    """A single item in the shopping cart."""

    def __init__(self, product: Product, quantity: int = 1):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal(self) -> float:
        return self.product.price * self.quantity

    def __repr__(self) -> str:
        return f"{self.product.name} x{self.quantity} = ${self.subtotal:.2f}"
