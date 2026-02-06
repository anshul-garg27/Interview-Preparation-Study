"""LSP Fixed - Proper hierarchy where subtypes are truly substitutable."""

from abc import ABC, abstractmethod


class Shape(ABC):
    """Common interface - no mutable width/height coupling issues."""

    @abstractmethod
    def area(self) -> float:
        pass

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.1f}"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Square(Shape):
    """Square is NOT a subclass of Rectangle - it's a separate Shape."""

    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side ** 2


def print_areas(shapes: list[Shape]) -> None:
    """Works correctly with ANY Shape - true substitutability."""
    for shape in shapes:
        print(f"  {shape.describe()}")


if __name__ == "__main__":
    print("GOOD DESIGN: Liskov Substitution Principle\n")

    shapes: list[Shape] = [
        Rectangle(5, 10),
        Square(7),
        Rectangle(3, 4),
        Square(5),
    ]

    print_areas(shapes)

    print("\nBENEFITS:")
    print("  1. Rectangle and Square are siblings, not parent-child")
    print("  2. No broken contracts - each type honors Shape interface")
    print("  3. Any Shape can replace any other Shape safely")
    print("  4. No surprising side effects from setters")
