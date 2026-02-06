"""Dataclasses - Less boilerplate for data-holding classes."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Point:
    """Simple dataclass - auto-generates __init__, __repr__, __eq__."""
    x: float
    y: float

    def distance_from_origin(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** 0.5


@dataclass(frozen=True)
class Color:
    """Frozen dataclass - immutable (can be used as dict key / in sets)."""
    r: int
    g: int
    b: int


@dataclass(order=True)
class Student:
    """Ordered dataclass - auto-generates comparison methods.
    sort_index controls sorting; name is excluded from ordering."""
    sort_index: float = field(init=False, repr=False)
    name: str = ""
    gpa: float = 0.0

    def __post_init__(self):
        self.sort_index = self.gpa


@dataclass
class Team:
    """Dataclass with mutable default (use field(default_factory=...))."""
    name: str
    members: List[str] = field(default_factory=list)

    def add(self, member: str):
        self.members.append(member)


if __name__ == "__main__":
    print("=== Dataclasses ===\n")

    # Basic dataclass
    p1 = Point(3, 4)
    p2 = Point(3, 4)
    print(f"Point: {p1}")
    print(f"Equal: {p1 == p2}")
    print(f"Distance: {p1.distance_from_origin()}")

    # Frozen (immutable)
    print("\n--- Frozen ---")
    red = Color(255, 0, 0)
    print(f"Color: {red}")
    try:
        red.r = 100  # type: ignore
    except AttributeError as e:
        print(f"Cannot mutate frozen: {e}")

    # Ordered (sortable)
    print("\n--- Ordered ---")
    students = [
        Student("Alice", 3.8),
        Student("Bob", 3.5),
        Student("Charlie", 3.9),
    ]
    for s in sorted(students, reverse=True):
        print(f"  {s.name}: {s.gpa}")

    # Mutable default with field()
    print("\n--- Mutable Defaults ---")
    t1 = Team("Backend")
    t1.add("Alice")
    t1.add("Bob")
    t2 = Team("Frontend")
    t2.add("Charlie")
    print(f"{t1}")
    print(f"{t2}")  # Separate list - no shared state bug
