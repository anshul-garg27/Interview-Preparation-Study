"""Abstract Observer interface."""

from abc import ABC, abstractmethod


class Observer(ABC):
    """Objects that want to be notified of changes."""

    @abstractmethod
    def update(self, symbol: str, price: float):
        pass
