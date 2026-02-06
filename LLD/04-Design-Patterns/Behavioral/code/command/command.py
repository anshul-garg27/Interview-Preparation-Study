"""Abstract Command interface."""

from abc import ABC, abstractmethod


class Command(ABC):
    """All commands must implement execute and undo."""

    @abstractmethod
    def execute(self) -> str:
        pass

    @abstractmethod
    def undo(self) -> str:
        pass
