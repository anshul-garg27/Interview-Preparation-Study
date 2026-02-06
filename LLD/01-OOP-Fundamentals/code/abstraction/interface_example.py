"""Abstraction - Python Protocols (structural subtyping / duck typing interfaces)."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Drawable(Protocol):
    """Interface via Protocol - any class with draw() method satisfies this."""
    def draw(self) -> str: ...


@runtime_checkable
class Resizable(Protocol):
    def resize(self, factor: float) -> None: ...


# These classes DON'T explicitly inherit Drawable - they just implement draw()
class Circle:
    def __init__(self, radius: float):
        self.radius = radius

    def draw(self) -> str:
        return f"Drawing circle with radius {self.radius}"

    def resize(self, factor: float) -> None:
        self.radius *= factor


class Square:
    def __init__(self, side: float):
        self.side = side

    def draw(self) -> str:
        return f"Drawing square with side {self.side}"


class Text:
    """Not a shape, but still Drawable!"""
    def __init__(self, content: str):
        self.content = content

    def draw(self) -> str:
        return f"Rendering text: '{self.content}'"


def render_all(items: list[Drawable]) -> None:
    """Works with ANY object that has a draw() method."""
    for item in items:
        print(f"  {item.draw()}")


if __name__ == "__main__":
    print("=== Protocols (Structural Subtyping) ===\n")

    items: list[Drawable] = [Circle(5), Square(3), Text("Hello")]
    render_all(items)

    # Runtime check with @runtime_checkable
    print(f"\nCircle is Drawable? {isinstance(Circle(1), Drawable)}")
    print(f"Square is Drawable? {isinstance(Square(1), Drawable)}")
    print(f"str is Drawable?    {isinstance('hello', Drawable)}")

    # Circle is also Resizable, Square is not
    print(f"\nCircle is Resizable? {isinstance(Circle(1), Resizable)}")
    print(f"Square is Resizable? {isinstance(Square(1), Resizable)}")
