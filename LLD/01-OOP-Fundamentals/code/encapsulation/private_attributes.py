"""Encapsulation - Private attributes, name mangling, and @property."""


class Employee:
    """Demonstrates Python's access control conventions."""

    def __init__(self, name: str, salary: float):
        self.name = name          # Public - anyone can access
        self._department = "TBD"  # Protected (convention) - internal use
        self.__salary = salary    # Private (name-mangled) - truly hidden

    # Property: controlled access to private data
    @property
    def salary(self) -> float:
        return self.__salary

    @salary.setter
    def salary(self, value: float):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self.__salary = value

    @property
    def department(self) -> str:
        return self._department

    @department.setter
    def department(self, value: str):
        allowed = ["Engineering", "Sales", "HR", "TBD"]
        if value not in allowed:
            raise ValueError(f"Department must be one of {allowed}")
        self._department = value

    def get_info(self) -> str:
        return f"{self.name} | {self._department} | ${self.__salary:,.0f}"


if __name__ == "__main__":
    print("=== Encapsulation: Private Attributes ===\n")

    emp = Employee("Alice", 85000)

    # Public: direct access
    print(f"Name (public): {emp.name}")

    # Protected: works but signals "internal use"
    print(f"Dept (protected): {emp._department}")

    # Private: name-mangled to _Employee__salary
    try:
        print(emp.__salary)  # type: ignore
    except AttributeError:
        print("Cannot access __salary directly (name-mangled)")

    # Access via property (controlled)
    print(f"Salary (property): ${emp.salary:,.0f}")

    # Setter with validation
    emp.salary = 95000
    print(f"Updated salary: ${emp.salary:,.0f}")

    try:
        emp.salary = -1000
    except ValueError as e:
        print(f"Validation caught: {e}")

    # Name mangling: still accessible but NEVER do this
    print(f"\nName-mangled access: ${emp._Employee__salary:,.0f}")
    print("(Above is possible but violates encapsulation!)")

    # Department validation
    emp.department = "Engineering"
    print(f"\n{emp.get_info()}")
