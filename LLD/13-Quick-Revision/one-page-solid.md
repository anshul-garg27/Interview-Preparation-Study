# One-Page SOLID Revision

> All 5 SOLID principles with mini code examples on one page.

---

## S — Single Responsibility

> "One class, one reason to change."

```python
# BAD: Employee handles pay, report, DB
class Employee:
    def calculate_pay(self): ...
    def generate_report(self): ...
    def save(self): ...

# GOOD: Separate responsibilities
class PayCalculator:      def calculate(self, emp): ...
class ReportGen:          def generate(self, emp): ...
class EmployeeRepo:       def save(self, emp): ...
```
**Detect:** Class has 200+ lines? Multiple stakeholders change it? Violates SRP.

---

## O — Open/Closed

> "Open for extension, closed for modification."

```python
# BAD: Modify for every new type
def discount(type, amt):
    if type == "regular": return amt * 0.1
    elif type == "vip":   return amt * 0.3  # Edit here each time

# GOOD: Extend without modifying
class Discount(ABC):
    @abstractmethod
    def calc(self, amt): ...

class VIPDiscount(Discount):        # Just add new class
    def calc(self, amt): return amt * 0.3
```
**Detect:** Long if/elif chain by type? Must edit existing code for new feature? Violates OCP.

---

## L — Liskov Substitution

> "Child must work wherever parent works."

```python
# BAD: Square breaks Rectangle contract
class Rectangle:
    def set_width(self, w):  self.w = w
    def set_height(self, h): self.h = h

class Square(Rectangle):
    def set_width(self, w):  self.w = self.h = w  # BREAKS!

# GOOD: Separate hierarchies
class Shape(ABC):
    @abstractmethod
    def area(self): ...

class Rectangle(Shape): ...  # Independent
class Square(Shape): ...     # Independent
```
**Detect:** Subclass throws NotImplementedError? isinstance() checks before calling? Violates LSP.

---

## I — Interface Segregation

> "Don't force clients to depend on unused methods."

```python
# BAD: Robot forced to implement eat()
class Worker(ABC):
    @abstractmethod
    def work(self): ...
    @abstractmethod
    def eat(self): ...   # Robot can't eat!

# GOOD: Split interfaces
class Workable(ABC):
    @abstractmethod
    def work(self): ...
class Eatable(ABC):
    @abstractmethod
    def eat(self): ...

class Robot(Workable):        # Only what it needs
    def work(self): ...
```
**Detect:** Empty method bodies? Interface has 10+ methods? Violates ISP.

---

## D — Dependency Inversion

> "Depend on abstractions, not concretions."

```python
# BAD: Direct dependency on MySQL
class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Concrete!

# GOOD: Inject abstraction
class UserService:
    def __init__(self, db: Database):  # Abstract!
        self.db = db

# Usage: UserService(MySQLDatabase())
# Test:  UserService(MockDatabase())
```
**Detect:** `self.x = ConcreteClass()` in constructor? Can't unit test without real DB? Violates DIP.

---

## Quick Violation Detector

| #  | Question                                              | Violation |
|----|-------------------------------------------------------|-----------|
| 1  | Class has multiple reasons to change?                 | SRP       |
| 2  | Adding feature requires editing existing code?        | OCP       |
| 3  | Subclass can't replace parent safely?                 | LSP       |
| 4  | Implementor has stub/empty methods?                   | ISP       |
| 5  | High-level module creates low-level objects directly? | DIP       |

---

## How They Connect

```
SRP → small classes → easier to extend (OCP)
OCP → relies on safe substitution (LSP)
ISP → small interfaces → supports SRP
DIP → abstractions → enables OCP
```

---

## Mnemonics

| Principle | Remember                                 |
|-----------|------------------------------------------|
| SRP       | "A chef shouldn't also be the waiter"    |
| OCP       | "Add plugins, don't rewrite the app"     |
| LSP       | "If it looks like a duck but needs batteries, it's wrong" |
| ISP       | "Buffet menu, not fixed course"          |
| DIP       | "Program to the interface, not the class"|

---

*One-page revision | 2026-02-06*
