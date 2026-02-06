"""File - leaf node in the composite tree."""

from component import FileSystemComponent


class File(FileSystemComponent):
    """A file with a fixed size (leaf node)."""

    def __init__(self, name: str, size: int):
        super().__init__(name)
        self._size = size

    def get_size(self) -> int:
        return self._size

    def display(self, indent: int = 0):
        print(f"{'  ' * indent}- {self.name} ({self._size} bytes)")
