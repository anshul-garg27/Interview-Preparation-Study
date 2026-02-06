"""Inventory management for the vending machine."""

from product import Product


class Inventory:
    """Tracks products and their quantities."""

    def __init__(self):
        self.products: dict[str, Product] = {}
        self.quantities: dict[str, int] = {}

    def add_product(self, product: Product, quantity: int) -> None:
        """Add or restock a product."""
        self.products[product.code] = product
        self.quantities[product.code] = (
            self.quantities.get(product.code, 0) + quantity
        )

    def remove_product(self, code: str) -> None:
        """Remove a product from inventory entirely."""
        self.products.pop(code, None)
        self.quantities.pop(code, None)

    def get_product(self, code: str) -> Product | None:
        """Get product by code."""
        return self.products.get(code)

    def is_available(self, code: str) -> bool:
        """Check if product is in stock."""
        return code in self.quantities and self.quantities[code] > 0

    def dispense(self, code: str) -> None:
        """Decrement quantity after dispensing."""
        if self.is_available(code):
            self.quantities[code] -= 1

    def display(self) -> None:
        """Print inventory table."""
        print("\n    +------+--------------------+--------+-----+")
        print("    | Code | Product            | Price  | Qty |")
        print("    +------+--------------------+--------+-----+")
        for code, product in self.products.items():
            qty = self.quantities.get(code, 0)
            status = f"{qty:3d}" if qty > 0 else "OUT"
            print(f"    | {code:4s} | {product.name:18s} "
                  f"| ${product.price:5.2f} | {status} |")
        print("    +------+--------------------+--------+-----+")
