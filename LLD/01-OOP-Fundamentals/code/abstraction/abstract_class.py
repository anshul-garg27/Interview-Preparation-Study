"""Abstraction - Abstract Base Classes and @abstractmethod."""

from abc import ABC, abstractmethod


class Shape(ABC):
    """Abstract class - cannot be instantiated directly."""

    @abstractmethod
    def area(self) -> float:
        """Subclasses MUST implement this."""
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    # Concrete method - shared by all subclasses
    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


# Abstract property example
class Vehicle(ABC):
    @property
    @abstractmethod
    def fuel_type(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.__class__.__name__} uses {self.fuel_type}"


class ElectricCar(Vehicle):
    @property
    def fuel_type(self) -> str:
        return "electricity"


if __name__ == "__main__":
    print("=== Abstract Classes ===\n")

    # Cannot instantiate abstract class
    try:
        s = Shape()  # type: ignore
    except TypeError as e:
        print(f"Cannot instantiate: {e}")

    # Concrete subclasses work fine
    shapes: list[Shape] = [Circle(5), Rectangle(4, 6)]
    for shape in shapes:
        print(shape.describe())

    # Abstract property
    print(f"\n{ElectricCar().describe()}")
