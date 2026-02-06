"""Abstract Coffee component."""

from abc import ABC, abstractmethod


class Coffee(ABC):
    """Base interface for all coffees and decorators."""

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_cost(self) -> float:
        pass

    def __repr__(self):
        return f"{self.get_description()} = ${self.get_cost():.2f}"
