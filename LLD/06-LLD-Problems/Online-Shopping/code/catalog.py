"""ProductCatalog (Singleton) - search and filter products."""

import threading
from typing import Optional, List
from enums import ProductCategory
from product import Product


class ProductCatalog:
    """Singleton catalog with search and filter capabilities."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.products = {}  # product_id -> Product
        self._initialized = True

    def add_product(self, product: Product) -> None:
        self.products[product.product_id] = product

    def search(self, keyword: str = None, category: ProductCategory = None,
               min_price: float = None, max_price: float = None,
               brand: str = None) -> List[Product]:
        """Search products with multiple filters."""
        results = list(self.products.values())
        if keyword:
            kw = keyword.lower()
            results = [p for p in results if kw in p.name.lower() or kw in p.seller.lower()]
        if category:
            results = [p for p in results if p.category == category]
        if min_price is not None:
            results = [p for p in results if p.price >= min_price]
        if max_price is not None:
            results = [p for p in results if p.price <= max_price]
        if brand:
            results = [p for p in results if brand.lower() in p.seller.lower()]
        return results

    def display(self) -> None:
        print(f"\n    {'='*70}")
        print(f"    Product Catalog ({len(self.products)} items)")
        print(f"    {'='*70}")
        for p in self.products.values():
            print(f"      [{p.product_id}] {p}")
        print(f"    {'='*70}")
