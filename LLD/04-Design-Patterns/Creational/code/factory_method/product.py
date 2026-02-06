"""Abstract Product interface for documents."""

from abc import ABC, abstractmethod


class Document(ABC):
    """Abstract document that all concrete documents must implement."""

    @abstractmethod
    def create(self) -> str:
        pass

    @abstractmethod
    def save(self, filename: str) -> str:
        pass

    @abstractmethod
    def get_extension(self) -> str:
        pass
