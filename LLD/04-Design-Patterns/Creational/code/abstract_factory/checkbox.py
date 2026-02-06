"""Abstract Checkbox interface."""

from abc import ABC, abstractmethod


class Checkbox(ABC):
    """All platform checkboxes must implement this."""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def toggle(self) -> str:
        pass
