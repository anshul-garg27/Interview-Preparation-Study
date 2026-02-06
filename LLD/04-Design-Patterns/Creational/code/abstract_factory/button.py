"""Abstract Button interface."""

from abc import ABC, abstractmethod


class Button(ABC):
    """All platform buttons must implement this."""

    @abstractmethod
    def render(self) -> str:
        pass

    @abstractmethod
    def on_click(self, callback: str) -> str:
        pass
