"""Directory - composite node containing files and sub-directories."""

from component import FileSystemComponent


class Directory(FileSystemComponent):
    """A directory that can contain files and other directories."""

    def __init__(self, name: str):
        super().__init__(name)
        self._children: list[FileSystemComponent] = []

    def add(self, component: FileSystemComponent):
        self._children.append(component)

    def remove(self, component: FileSystemComponent):
        self._children.remove(component)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self._children)

    def display(self, indent: int = 0):
        print(f"{'  ' * indent}+ {self.name}/ ({self.get_size()} bytes)")
        for child in self._children:
            child.display(indent + 1)
