"""Hierarchical Inheritance - One parent, multiple children (Shape example)."""

import math
from abc import ABC, abstractmethod


class Shape(ABC):
    """Common parent for all shapes."""

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> str:
        return (f"{self.__class__.__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c


if __name__ == "__main__":
    print("=== Hierarchical Inheritance ===\n")
    print("Shape -> Circle, Rectangle, Triangle\n")

    shapes: list[Shape] = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5),
    ]

    total_area = 0.0
    for shape in shapes:
        print(f"  {shape.describe()}")
        total_area += shape.area()

    print(f"\nTotal area: {total_area:.2f}")
