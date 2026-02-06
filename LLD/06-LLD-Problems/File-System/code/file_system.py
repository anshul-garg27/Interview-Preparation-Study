"""
In-Memory File System - Low Level Design
Run: python file_system.py

Patterns: Composite (file/directory tree), Visitor (operations), Iterator (traversal)
Key: Composite pattern showcase - files and directories treated uniformly
"""
from abc import ABC, abstractmethod
from datetime import datetime
from collections import deque


# ─── Permission Model ────────────────────────────────────────────────
class Permission:
    def __init__(self, read=True, write=True, execute=False):
        self.read = read
        self.write = write
        self.execute = execute

    def __repr__(self):
        r = "r" if self.read else "-"
        w = "w" if self.write else "-"
        x = "x" if self.execute else "-"
        return f"{r}{w}{x}"


# ─── Composite Pattern: FileSystemNode ───────────────────────────────
class FileSystemNode(ABC):
    def __init__(self, name: str, permissions: Permission = None):
        self.name = name
        self.permissions = permissions or Permission()
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.parent: "Directory | None" = None

    def get_path(self) -> str:
        parts = []
        node = self
        while node is not None:
            parts.append(node.name)
            node = node.parent
        return "/" + "/".join(reversed(parts[:-1]))  # skip root name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def is_directory(self) -> bool:
        pass

    @abstractmethod
    def accept(self, visitor: "FileSystemVisitor"):
        pass


class File(FileSystemNode):
    def __init__(self, name: str, size: int = 0, content: str = ""):
        super().__init__(name)
        self.size = size
        self.content = content
        self.extension = name.rsplit(".", 1)[-1] if "." in name else ""

    def get_size(self) -> int:
        return self.size

    def is_directory(self) -> bool:
        return False

    def accept(self, visitor: "FileSystemVisitor"):
        visitor.visit_file(self)

    def __repr__(self):
        return f"File({self.name}, {self.size}B)"


class Directory(FileSystemNode):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: dict[str, FileSystemNode] = {}

    def add(self, node: FileSystemNode):
        if not self.permissions.write:
            raise PermissionError(f"No write permission on {self.name}")
        if node.name in self.children:
            raise FileExistsError(f"'{node.name}' already exists in {self.name}")
        node.parent = self
        self.children[node.name] = node
        self.modified_at = datetime.now()

    def remove(self, name: str):
        if not self.permissions.write:
            raise PermissionError(f"No write permission on {self.name}")
        if name not in self.children:
            raise FileNotFoundError(f"'{name}' not found in {self.name}")
        removed = self.children.pop(name)
        removed.parent = None
        self.modified_at = datetime.now()
        return removed

    def get_child(self, name: str) -> FileSystemNode:
        if name not in self.children:
            raise FileNotFoundError(f"'{name}' not found in {self.name}")
        return self.children[name]

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children.values())

    def is_directory(self) -> bool:
        return True

    def accept(self, visitor: "FileSystemVisitor"):
        visitor.visit_directory(self)

    def __repr__(self):
        return f"Dir({self.name}/, {len(self.children)} items)"


# ─── Visitor Pattern: Operations on the tree ─────────────────────────
class FileSystemVisitor(ABC):
    @abstractmethod
    def visit_file(self, file: File):
        pass

    @abstractmethod
    def visit_directory(self, directory: Directory):
        pass


class TreeDisplayVisitor(FileSystemVisitor):
    """Display tree structure like the `tree` command."""
    def __init__(self):
        self.output_lines: list[str] = []
        self._depth = 0

    def visit_file(self, file: File):
        prefix = "    " * self._depth + "|-- "
        self.output_lines.append(f"{prefix}{file.name} ({file.size}B) [{file.permissions}]")

    def visit_directory(self, directory: Directory):
        if self._depth == 0:
            self.output_lines.append(f"{directory.name}/")
        else:
            prefix = "    " * self._depth + "|-- "
            self.output_lines.append(f"{prefix}{directory.name}/")
        self._depth += 1
        for child in sorted(directory.children.values(),
                            key=lambda c: (not c.is_directory(), c.name)):
            child.accept(self)
        self._depth -= 1

    def get_output(self) -> str:
        return "\n".join(self.output_lines)


class SearchVisitor(FileSystemVisitor):
    """Search files by name, extension, or minimum size."""
    def __init__(self, name: str = None, extension: str = None,
                 min_size: int = None):
        self.name = name
        self.extension = extension
        self.min_size = min_size
        self.results: list[FileSystemNode] = []

    def _matches(self, node: FileSystemNode) -> bool:
        if self.name and self.name.lower() not in node.name.lower():
            return False
        if self.extension and isinstance(node, File):
            if node.extension.lower() != self.extension.lower():
                return False
        if self.min_size and node.get_size() < self.min_size:
            return False
        return True

    def visit_file(self, file: File):
        if self._matches(file):
            self.results.append(file)

    def visit_directory(self, directory: Directory):
        if self.name and not self.extension and self._matches(directory):
            self.results.append(directory)
        for child in directory.children.values():
            child.accept(self)


class SizeCalculatorVisitor(FileSystemVisitor):
    """Calculate total size of a subtree."""
    def __init__(self):
        self.total_size = 0

    def visit_file(self, file: File):
        self.total_size += file.size

    def visit_directory(self, directory: Directory):
        for child in directory.children.values():
            child.accept(self)


# ─── Iterator: BFS Traversal ────────────────────────────────────────
class BFSIterator:
    """Breadth-first iterator over file system nodes."""
    def __init__(self, root: FileSystemNode):
        self._queue = deque([root])

    def __iter__(self):
        return self

    def __next__(self) -> FileSystemNode:
        if not self._queue:
            raise StopIteration
        node = self._queue.popleft()
        if isinstance(node, Directory):
            self._queue.extend(node.children.values())
        return node


# ─── Facade: FileSystem ─────────────────────────────────────────────
class FileSystem:
    def __init__(self):
        self.root = Directory("root")

    def _resolve_path(self, path: str) -> FileSystemNode:
        if path == "/":
            return self.root
        parts = [p for p in path.strip("/").split("/") if p]
        current = self.root
        for part in parts:
            if not isinstance(current, Directory):
                raise NotADirectoryError(f"'{current.name}' is not a directory")
            current = current.get_child(part)
        return current

    def create_file(self, dir_path: str, name: str, size: int = 0) -> File:
        parent = self._resolve_path(dir_path)
        if not isinstance(parent, Directory):
            raise NotADirectoryError(f"'{dir_path}' is not a directory")
        f = File(name, size)
        parent.add(f)
        return f

    def create_directory(self, dir_path: str, name: str) -> Directory:
        parent = self._resolve_path(dir_path)
        if not isinstance(parent, Directory):
            raise NotADirectoryError(f"'{dir_path}' is not a directory")
        d = Directory(name)
        parent.add(d)
        return d

    def delete(self, path: str):
        node = self._resolve_path(path)
        if node == self.root:
            raise PermissionError("Cannot delete root directory")
        node.parent.remove(node.name)

    def move(self, src_path: str, dest_dir_path: str):
        node = self._resolve_path(src_path)
        dest = self._resolve_path(dest_dir_path)
        if not isinstance(dest, Directory):
            raise NotADirectoryError(f"Destination is not a directory")
        # Prevent moving directory into itself
        check = dest
        while check is not None:
            if check == node:
                raise ValueError("Cannot move directory into its own subtree")
            check = check.parent
        node.parent.remove(node.name)
        dest.add(node)

    def search(self, **kwargs) -> list[FileSystemNode]:
        visitor = SearchVisitor(**kwargs)
        self.root.accept(visitor)
        return visitor.results

    def display_tree(self) -> str:
        visitor = TreeDisplayVisitor()
        self.root.accept(visitor)
        return visitor.get_output()

    def get_size(self, path: str = "/") -> int:
        node = self._resolve_path(path)
        visitor = SizeCalculatorVisitor()
        node.accept(visitor)
        return visitor.total_size


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    fs = FileSystem()

    # Build a file tree
    print("=" * 60)
    print("BUILDING FILE SYSTEM")
    print("=" * 60)

    fs.create_directory("/", "home")
    fs.create_directory("/home", "alice")
    fs.create_directory("/home", "bob")
    fs.create_directory("/home/alice", "documents")
    fs.create_directory("/home/alice", "photos")
    fs.create_file("/home/alice/documents", "report.txt", 1024)
    fs.create_file("/home/alice/documents", "budget.xlsx", 2048)
    fs.create_file("/home/alice/photos", "vacation.jpg", 5120)
    fs.create_file("/home/bob", "notes.txt", 512)
    fs.create_directory("/", "etc")
    fs.create_file("/etc", "config.yml", 256)

    # Display tree
    print("\n" + "=" * 60)
    print("TREE DISPLAY")
    print("=" * 60)
    print(fs.display_tree())

    # Size calculation
    print("\n" + "=" * 60)
    print("SIZE CALCULATIONS")
    print("=" * 60)
    print(f"  Total system size: {fs.get_size('/')} bytes")
    print(f"  /home size: {fs.get_size('/home')} bytes")
    print(f"  /home/alice size: {fs.get_size('/home/alice')} bytes")
    print(f"  Single file: {fs.get_size('/home/alice/documents/report.txt')} bytes")

    # Search
    print("\n" + "=" * 60)
    print("SEARCH")
    print("=" * 60)
    results = fs.search(extension="txt")
    print(f"  .txt files: {[f'{r.name} ({r.get_path()})' for r in results]}")
    results = fs.search(min_size=2000)
    print(f"  Files > 2KB: {[f'{r.name} ({r.get_size()}B)' for r in results]}")
    results = fs.search(name="alice")
    print(f"  Name contains 'alice': {[r.get_path() for r in results]}")

    # Move operation
    print("\n" + "=" * 60)
    print("MOVE: /home/bob/notes.txt -> /home/alice/documents/")
    print("=" * 60)
    fs.move("/home/bob/notes.txt", "/home/alice/documents")
    print(fs.display_tree())

    # Delete operation
    print("\n" + "=" * 60)
    print("DELETE: /home/alice/photos (recursive)")
    print("=" * 60)
    fs.delete("/home/alice/photos")
    print(fs.display_tree())

    # BFS Iterator
    print("\n" + "=" * 60)
    print("BFS TRAVERSAL")
    print("=" * 60)
    for node in BFSIterator(fs.root):
        kind = "DIR " if node.is_directory() else "FILE"
        print(f"  [{kind}] {node.get_path() or '/'} ({node.get_size()}B)")

    # Edge cases
    print("\n" + "=" * 60)
    print("EDGE CASES")
    print("=" * 60)
    try:
        fs.create_file("/home/alice/documents", "report.txt", 100)
    except FileExistsError as e:
        print(f"  Duplicate: {e}")
    try:
        fs.delete("/")
    except PermissionError as e:
        print(f"  Root delete: {e}")
    try:
        fs.move("/home", "/home/alice")
    except ValueError as e:
        print(f"  Cycle: {e}")


if __name__ == "__main__":
    main()
