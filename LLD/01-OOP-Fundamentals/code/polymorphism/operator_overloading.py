"""Operator Overloading - __add__, __mul__, __eq__ for a Vector class."""


class Vector:
    """2D Vector with overloaded operators."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    # Addition: v1 + v2
    def __add__(self, other: "Vector") -> "Vector":
        return Vector(self.x + other.x, self.y + other.y)

    # Subtraction: v1 - v2
    def __sub__(self, other: "Vector") -> "Vector":
        return Vector(self.x - other.x, self.y - other.y)

    # Scalar multiplication: v * 3
    def __mul__(self, scalar: float) -> "Vector":
        return Vector(self.x * scalar, self.y * scalar)

    # Reverse multiplication: 3 * v
    def __rmul__(self, scalar: float) -> "Vector":
        return self.__mul__(scalar)

    # Equality: v1 == v2
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    # Absolute value (magnitude): abs(v)
    def __abs__(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5

    # Negation: -v
    def __neg__(self) -> "Vector":
        return Vector(-self.x, -self.y)

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"


if __name__ == "__main__":
    print("=== Operator Overloading ===\n")

    v1 = Vector(3, 4)
    v2 = Vector(1, 2)

    # Arithmetic operators
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")         # Vector(4, 6)
    print(f"v1 - v2 = {v1 - v2}")         # Vector(2, 2)
    print(f"v1 * 3  = {v1 * 3}")          # Vector(9, 12)
    print(f"3 * v1  = {3 * v1}")          # Vector(9, 12) via __rmul__

    # Comparison
    print(f"\nv1 == v2:              {v1 == v2}")           # False
    print(f"v1 == Vector(3, 4):    {v1 == Vector(3, 4)}")  # True

    # Unary operators
    print(f"\nabs(v1) = {abs(v1):.2f}")  # 5.0 (magnitude)
    print(f"-v1     = {-v1}")            # Vector(-3, -4)

    # Chaining operations
    result = (v1 + v2) * 2
    print(f"\n(v1 + v2) * 2 = {result}")  # Vector(8, 12)
