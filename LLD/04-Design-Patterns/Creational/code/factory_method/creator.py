"""Abstract Creator with the factory method."""

from abc import ABC, abstractmethod
from product import Document


class DocumentCreator(ABC):
    """Declares the factory method that returns a Document."""

    @abstractmethod
    def factory_method(self) -> Document:
        pass

    def create_document(self) -> str:
        """Template method that uses the factory method."""
        doc = self.factory_method()
        result = doc.create()
        return result
