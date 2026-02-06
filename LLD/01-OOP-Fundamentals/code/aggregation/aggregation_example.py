"""Aggregation - Department HAS Employees (weak ownership)."""


class Employee:
    """Employee exists independently of any department."""

    def __init__(self, name: str, skill: str):
        self.name = name
        self.skill = skill

    def __repr__(self) -> str:
        return f"Employee({self.name}, {self.skill})"


class Department:
    """Department contains employees but doesn't own their lifecycle.
    Employees are created outside and passed in (weak ownership)."""

    def __init__(self, name: str):
        self.name = name
        self._members: list[Employee] = []

    def add(self, employee: Employee) -> None:
        self._members.append(employee)
        print(f"  {employee.name} joined {self.name}")

    def remove(self, employee: Employee) -> None:
        self._members.remove(employee)
        print(f"  {employee.name} left {self.name}")

    def list_members(self) -> None:
        print(f"  {self.name}: {[e.name for e in self._members]}")

    @property
    def size(self) -> int:
        return len(self._members)


if __name__ == "__main__":
    print("=== Aggregation (Weak Ownership) ===\n")

    # Employees exist independently
    alice = Employee("Alice", "Python")
    bob = Employee("Bob", "Java")
    charlie = Employee("Charlie", "Go")

    # Departments aggregate employees
    engineering = Department("Engineering")
    research = Department("Research")

    engineering.add(alice)
    engineering.add(bob)
    research.add(charlie)

    print("\nTeams:")
    engineering.list_members()
    research.list_members()

    # Key difference from composition:
    # Employee can move between departments
    print("\n--- Alice moves from Engineering to Research ---")
    engineering.remove(alice)
    research.add(alice)

    print("\nUpdated teams:")
    engineering.list_members()
    research.list_members()

    # Delete department - employees still exist!
    print(f"\n--- Delete Engineering department ---")
    del engineering
    print(f"Alice still exists: {alice}")
    print(f"Bob still exists:   {bob}")
    print("Employees survive department deletion (weak ownership).")
