"""Concrete prototypes: shapes that can be cloned."""

import copy
from prototype import Prototype


class Circle(Prototype):
    def __init__(self, radius: float, color: str):
        self.radius = radius
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def __repr__(self):
        return f"Circle(r={self.radius}, color={self.color}, id={id(self)})"


class Rectangle(Prototype):
    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color = color

    def clone(self):
        return copy.deepcopy(self)

    def area(self) -> float:
        return self.width * self.height

    def __repr__(self):
        return (
            f"Rectangle(w={self.width}, h={self.height}, "
            f"color={self.color}, id={id(self)})"
        )
