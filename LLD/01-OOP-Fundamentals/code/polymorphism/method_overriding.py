"""Runtime Polymorphism - Same method name, different behavior per type."""

from abc import ABC, abstractmethod


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def draw(self) -> str:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def draw(self) -> str:
        return f"Drawing Circle (r={self.radius})"


class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

    def area(self) -> float:
        return self.w * self.h

    def draw(self) -> str:
        return f"Drawing Rectangle ({self.w}x{self.h})"


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height

    def draw(self) -> str:
        return f"Drawing Triangle (b={self.base}, h={self.height})"


def render_canvas(shapes: list[Shape]) -> None:
    """Client code treats all shapes uniformly - polymorphism in action."""
    print("Rendering canvas:")
    total = 0.0
    for shape in shapes:
        print(f"  {shape.draw()} | area = {shape.area():.2f}")
        total += shape.area()
    print(f"  Total area: {total:.2f}")


if __name__ == "__main__":
    print("=== Runtime Polymorphism (Method Overriding) ===\n")

    # Same function works with any Shape - no if/elif needed
    shapes: list[Shape] = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 8),
    ]
    render_canvas(shapes)

    # Adding new shapes requires ZERO changes to render_canvas
    print("\nKey insight: render_canvas never checks the type.")
    print("It just calls .draw() and .area() - the object decides what to do.")
