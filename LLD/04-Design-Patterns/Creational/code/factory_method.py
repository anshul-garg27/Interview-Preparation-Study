"""
Factory Method Pattern - Defines an interface for creating objects,
letting subclasses decide which class to instantiate.

Examples:
1. Shape Factory: Circle, Rectangle, Triangle with area/perimeter
2. Logistics Factory: Truck and Ship transport
"""
from abc import ABC, abstractmethod
import math


# --- Shape Factory ---
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    @abstractmethod
    def draw(self) -> str:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * math.pi * self.radius

    def draw(self) -> str:
        return f"Drawing Circle(radius={self.radius})"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width, self.height = width, height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

    def draw(self) -> str:
        return f"Drawing Rectangle({self.width}x{self.height})"


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c

    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def perimeter(self) -> float:
        return self.a + self.b + self.c

    def draw(self) -> str:
        return f"Drawing Triangle(sides={self.a},{self.b},{self.c})"


class ShapeFactory:
    @staticmethod
    def create(shape_type: str, **kwargs) -> Shape:
        factories = {
            "circle": lambda: Circle(kwargs["radius"]),
            "rectangle": lambda: Rectangle(kwargs["width"], kwargs["height"]),
            "triangle": lambda: Triangle(kwargs["a"], kwargs["b"], kwargs["c"]),
        }
        if shape_type not in factories:
            raise ValueError(f"Unknown shape: {shape_type}")
        return factories[shape_type]()


# --- Logistics Factory ---
class Transport(ABC):
    @abstractmethod
    def deliver(self) -> str:
        pass

    @abstractmethod
    def cost_per_km(self) -> float:
        pass


class Truck(Transport):
    def deliver(self) -> str:
        return "Delivering by road in a truck"

    def cost_per_km(self) -> float:
        return 1.5


class Ship(Transport):
    def deliver(self) -> str:
        return "Delivering by sea in a cargo ship"

    def cost_per_km(self) -> float:
        return 0.8


class Logistics(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        pass

    def plan_delivery(self, distance: float) -> str:
        transport = self.create_transport()
        cost = transport.cost_per_km() * distance
        return f"  {transport.deliver()} | Distance: {distance}km | Cost: ${cost:.2f}"


class RoadLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Truck()


class SeaLogistics(Logistics):
    def create_transport(self) -> Transport:
        return Ship()


if __name__ == "__main__":
    print("=" * 60)
    print("FACTORY METHOD PATTERN DEMO")
    print("=" * 60)

    # Shape Factory
    print("\n--- Shape Factory ---")
    shapes = [
        ShapeFactory.create("circle", radius=5),
        ShapeFactory.create("rectangle", width=4, height=6),
        ShapeFactory.create("triangle", a=3, b=4, c=5),
    ]
    for shape in shapes:
        print(f"  {shape.draw()}")
        print(f"    Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")

    # Logistics Factory
    print("\n--- Logistics Factory ---")
    for logistics in [RoadLogistics(), SeaLogistics()]:
        print(logistics.plan_delivery(500))
