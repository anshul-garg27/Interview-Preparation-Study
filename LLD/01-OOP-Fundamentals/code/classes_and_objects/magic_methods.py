"""Magic (Dunder) Methods - __str__, __repr__, __eq__, __hash__, __lt__, __len__."""


class Product:
    """Demonstrates common magic methods on a Product class."""

    def __init__(self, name: str, price: float, quantity: int = 0):
        self.name = name
        self.price = price
        self.quantity = quantity

    # Human-readable string (for print, str())
    def __str__(self) -> str:
        return f"{self.name} - ${self.price:.2f}"

    # Developer-friendly string (for debugging, repr())
    def __repr__(self) -> str:
        return f"Product({self.name!r}, {self.price}, qty={self.quantity})"

    # Equality comparison
    def __eq__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.name == other.name and self.price == other.price

    # Required when __eq__ is defined (for use in sets/dict keys)
    def __hash__(self) -> int:
        return hash((self.name, self.price))

    # Less-than (enables sorting)
    def __lt__(self, other) -> bool:
        if not isinstance(other, Product):
            return NotImplemented
        return self.price < other.price

    # Length (inventory count)
    def __len__(self) -> int:
        return self.quantity

    # Boolean truth value
    def __bool__(self) -> bool:
        return self.quantity > 0


if __name__ == "__main__":
    print("=== Magic Methods ===\n")

    p1 = Product("Laptop", 999.99, 5)
    p2 = Product("Mouse", 29.99, 10)
    p3 = Product("Laptop", 999.99, 3)  # Same name+price as p1
    p4 = Product("Keyboard", 79.99, 0)

    # __str__ vs __repr__
    print(f"str:  {str(p1)}")        # Laptop - $999.99
    print(f"repr: {repr(p1)}")       # Product('Laptop', 999.99, qty=5)

    # __eq__ and __hash__
    print(f"\np1 == p3: {p1 == p3}")          # True (same name+price)
    print(f"p1 == p2: {p1 == p2}")            # False
    print(f"In set: {len({p1, p2, p3})}")     # 2 (p1 and p3 are equal)

    # __lt__ (sorting)
    products = [p1, p2, p4]
    print(f"\nSorted: {[str(p) for p in sorted(products)]}")

    # __len__
    print(f"\nlen(p1): {len(p1)}")   # 5
    print(f"len(p2): {len(p2)}")     # 10

    # __bool__
    print(f"\nbool(p1): {bool(p1)}")   # True (qty=5)
    print(f"bool(p4): {bool(p4)}")     # False (qty=0)
