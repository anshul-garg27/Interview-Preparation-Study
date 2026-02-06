"""Customer class extending User with cart and order history."""

from user import User
from cart import ShoppingCart


class Customer(User):
    """A customer who can browse, add to cart, and place orders."""

    def __init__(self, user_id: str, name: str, email: str, address: str = ""):
        super().__init__(user_id, name, email, address)
        self.cart = ShoppingCart()
        self.order_history = []

    def __repr__(self) -> str:
        return f"Customer({self.name}, Orders={len(self.order_history)})"
