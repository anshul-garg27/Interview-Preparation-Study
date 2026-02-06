"""
Composite Pattern - Composes objects into tree structures to represent
part-whole hierarchies. Lets clients treat individual objects and
compositions uniformly.

Examples:
1. File System: File and Directory hierarchy
2. Organization: Employee -> Manager -> Department
"""
from abc import ABC, abstractmethod


# --- File System ---
class FileSystemItem(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def get_size(self) -> int:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass


class File(FileSystemItem):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size

    def get_size(self) -> int:
        return self.size

    def display(self, indent: int = 0) -> str:
        return f"{'  ' * indent}|- {self.name} ({self.size} KB)"


class Directory(FileSystemItem):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem):
        self.children.append(item)
        return self

    def remove(self, item: FileSystemItem):
        self.children.remove(item)

    def get_size(self) -> int:
        return sum(child.get_size() for child in self.children)

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}[+] {self.name}/ ({self.get_size()} KB)"]
        for child in self.children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)


# --- Organization Hierarchy ---
class Employee(ABC):
    def __init__(self, name: str, role: str, salary: float):
        self.name = name
        self.role = role
        self.salary = salary

    @abstractmethod
    def get_total_salary(self) -> float:
        pass

    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass


class Developer(Employee):
    def get_total_salary(self) -> float:
        return self.salary

    def display(self, indent: int = 0) -> str:
        return f"{'  ' * indent}|- {self.name} ({self.role}) ${self.salary:,.0f}"


class Manager(Employee):
    def __init__(self, name: str, role: str, salary: float):
        super().__init__(name, role, salary)
        self.reports: list[Employee] = []

    def add(self, emp: Employee):
        self.reports.append(emp)
        return self

    def get_total_salary(self) -> float:
        return self.salary + sum(r.get_total_salary() for r in self.reports)

    def display(self, indent: int = 0) -> str:
        lines = [f"{'  ' * indent}[M] {self.name} ({self.role}) "
                 f"${self.salary:,.0f} [Team: ${self.get_total_salary():,.0f}]"]
        for r in self.reports:
            lines.append(r.display(indent + 1))
        return "\n".join(lines)


if __name__ == "__main__":
    print("=" * 60)
    print("COMPOSITE PATTERN DEMO")
    print("=" * 60)

    # File System
    print("\n--- File System ---")
    root = Directory("project")
    src = Directory("src")
    src.add(File("main.py", 15)).add(File("utils.py", 8))

    tests = Directory("tests")
    tests.add(File("test_main.py", 10))

    assets = Directory("assets")
    assets.add(File("logo.png", 250)).add(File("style.css", 5))

    root.add(src).add(tests).add(assets).add(File("README.md", 3))
    print(root.display())
    print(f"\n  Total project size: {root.get_size()} KB")

    # Organization
    print("\n--- Organization Hierarchy ---")
    cto = Manager("Alice", "CTO", 200000)
    eng_mgr = Manager("Bob", "Eng Manager", 150000)
    eng_mgr.add(Developer("Charlie", "Senior Dev", 120000))
    eng_mgr.add(Developer("Diana", "Junior Dev", 80000))
    eng_mgr.add(Developer("Eve", "Junior Dev", 80000))

    design_mgr = Manager("Frank", "Design Lead", 130000)
    design_mgr.add(Developer("Grace", "UI Designer", 100000))

    cto.add(eng_mgr).add(design_mgr)
    print(cto.display())
    print(f"\n  Total department cost: ${cto.get_total_salary():,.0f}")
