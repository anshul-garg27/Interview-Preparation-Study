"""Real-World Interfaces - Drawable, Serializable, Comparable."""

from abc import ABC, abstractmethod
import json


class Drawable(ABC):
    @abstractmethod
    def draw(self) -> str:
        pass


class Serializable(ABC):
    @abstractmethod
    def to_json(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data: str) -> "Serializable":
        pass


class Comparable(ABC):
    @abstractmethod
    def compare_to(self, other: "Comparable") -> int:
        """Returns -1, 0, or 1."""
        pass


# A class can implement MULTIPLE interfaces
class Shape(Drawable, Serializable, Comparable):
    pass


class Circle(Shape):
    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self) -> str:
        return f"Drawing circle at ({self.x},{self.y}) r={self.radius}"

    def to_json(self) -> str:
        return json.dumps({"type": "circle", "x": self.x, "y": self.y, "r": self.radius})

    @classmethod
    def from_json(cls, data: str) -> "Circle":
        d = json.loads(data)
        return cls(d["x"], d["y"], d["r"])

    def compare_to(self, other: "Comparable") -> int:
        if not isinstance(other, Circle):
            return NotImplemented
        if self.radius < other.radius:
            return -1
        elif self.radius > other.radius:
            return 1
        return 0

    @property
    def area(self) -> float:
        return 3.14159 * self.radius ** 2


if __name__ == "__main__":
    print("=== Real-World Interfaces ===\n")

    c1 = Circle(0, 0, 5)
    c2 = Circle(10, 10, 3)

    # Drawable interface
    print("--- Drawable ---")
    shapes: list[Drawable] = [c1, c2]
    for s in shapes:
        print(f"  {s.draw()}")

    # Serializable interface
    print("\n--- Serializable ---")
    json_str = c1.to_json()
    print(f"  Serialized:   {json_str}")
    restored = Circle.from_json(json_str)
    print(f"  Deserialized: {restored.draw()}")

    # Comparable interface
    print("\n--- Comparable ---")
    result = c1.compare_to(c2)
    comparison = "larger" if result > 0 else "smaller" if result < 0 else "equal"
    print(f"  Circle(r=5) is {comparison} than Circle(r=3)")

    # Sorting using compare_to
    circles = [Circle(0, 0, 7), Circle(0, 0, 2), Circle(0, 0, 5)]
    from functools import cmp_to_key
    sorted_circles = sorted(circles, key=cmp_to_key(lambda a, b: a.compare_to(b)))
    print(f"  Sorted radii: {[c.radius for c in sorted_circles]}")
