"""Abstract Image interface (Subject)."""

from abc import ABC, abstractmethod


class Image(ABC):
    """Common interface for real images and proxies."""

    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def get_filename(self) -> str:
        pass
