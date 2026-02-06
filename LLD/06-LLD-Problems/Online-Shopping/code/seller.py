"""Seller class extending User with product management."""

from user import User


class Seller(User):
    """A seller who lists products in the catalog."""

    def __init__(self, user_id: str, name: str, email: str,
                 store_name: str, address: str = ""):
        super().__init__(user_id, name, email, address)
        self.store_name = store_name
        self.products = []

    def __repr__(self) -> str:
        return f"Seller({self.store_name}, Products={len(self.products)})"
