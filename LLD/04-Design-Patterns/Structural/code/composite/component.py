"""Abstract FileSystemComponent."""

from abc import ABC, abstractmethod


class FileSystemComponent(ABC):
    """Common interface for files and directories."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0):
        pass
