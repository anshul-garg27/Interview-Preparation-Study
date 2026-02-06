"""Product class for the Online Shopping System."""

from enums import ProductCategory


class Product:
    """A product listed in the catalog."""

    def __init__(self, product_id: str, name: str, price: float,
                 category: ProductCategory, seller: str, stock: int = 10):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.category = category
        self.seller = seller
        self.stock = stock
        self.rating = 0.0
        self.review_count = 0

    def add_review(self, rating: float) -> None:
        """Add a rating and update the running average."""
        total = self.rating * self.review_count + rating
        self.review_count += 1
        self.rating = total / self.review_count

    def is_in_stock(self, quantity: int = 1) -> bool:
        return self.stock >= quantity

    def __repr__(self) -> str:
        stars = f"{self.rating:.1f}*" if self.review_count > 0 else "N/A"
        return (f"{self.name} (${self.price:.2f}, {self.category.value}, "
                f"{self.seller}, Stock:{self.stock}, Rating:{stars})")
