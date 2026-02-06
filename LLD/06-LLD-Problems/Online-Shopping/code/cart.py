"""ShoppingCart class for managing cart items."""

from product import Product
from cart_item import CartItem


class ShoppingCart:
    """Manages items in a user's shopping cart."""

    def __init__(self):
        self.items = {}  # product_id -> CartItem

    def add_item(self, product: Product, quantity: int = 1) -> bool:
        """Add product to cart if in stock."""
        if not product.is_in_stock(quantity):
            print(f"    [Cart] '{product.name}' out of stock!")
            return False
        if product.product_id in self.items:
            self.items[product.product_id].quantity += quantity
        else:
            self.items[product.product_id] = CartItem(product, quantity)
        print(f"    [Cart +] {product.name} x{quantity} added")
        return True

    def remove_item(self, product_id: str) -> None:
        """Remove an item from the cart."""
        if product_id in self.items:
            item = self.items.pop(product_id)
            print(f"    [Cart -] {item.product.name} removed")

    def get_total(self) -> float:
        return sum(item.subtotal for item in self.items.values())

    def clear(self) -> None:
        self.items.clear()

    def display(self) -> None:
        """Print cart contents."""
        if not self.items:
            print("    [Cart] Empty")
            return
        print(f"\n    {'─'*45}")
        print(f"    Shopping Cart:")
        for item in self.items.values():
            print(f"      {item}")
        print(f"    {'─'*45}")
        print(f"    Total: ${self.get_total():.2f}")
        print(f"    {'─'*45}")
