"""LSP Violation - Square breaks Rectangle's area contract."""


class Rectangle:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value

    def area(self) -> float:
        return self._width * self._height


class Square(Rectangle):
    """BAD: Square forces width == height, breaking Rectangle's contract."""

    def __init__(self, side: float):
        super().__init__(side, side)

    @Rectangle.width.setter
    def width(self, value: float) -> None:
        # Must keep width == height, so change BOTH
        self._width = value
        self._height = value

    @Rectangle.height.setter
    def height(self, value: float) -> None:
        self._width = value
        self._height = value


def calculate_expected_area(rect: Rectangle) -> None:
    """This function assumes Rectangle behavior: set width and height independently."""
    rect.width = 5
    rect.height = 10
    expected = 50  # 5 * 10
    actual = rect.area()
    status = "PASS" if actual == expected else "FAIL"
    print(f"  {rect.__class__.__name__}: expected={expected}, actual={actual} [{status}]")


if __name__ == "__main__":
    print("BAD DESIGN: Liskov Substitution Violation\n")

    print("Setting width=5, height=10, expecting area=50:")
    calculate_expected_area(Rectangle(1, 1))  # PASS: 50
    calculate_expected_area(Square(1))         # FAIL: 100 (both became 10)

    print("\nPROBLEM:")
    print("  Square cannot replace Rectangle without breaking behavior.")
    print("  Setting height to 10 also changed width to 10!")
    print("  This violates LSP: subtypes must be substitutable for base types.")
