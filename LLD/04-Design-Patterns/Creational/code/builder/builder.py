"""Abstract HouseBuilder interface."""

from abc import ABC, abstractmethod
from house import House


class HouseBuilder(ABC):
    """Defines all building steps."""

    def __init__(self):
        self._house = House()

    @abstractmethod
    def build_foundation(self): pass

    @abstractmethod
    def build_walls(self): pass

    @abstractmethod
    def build_roof(self): pass

    @abstractmethod
    def build_rooms(self, count: int): pass

    def get_result(self) -> House:
        house = self._house
        self._house = House()  # Reset for next build
        return house
