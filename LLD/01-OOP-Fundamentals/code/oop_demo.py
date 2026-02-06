"""
Complete OOP Concepts Demo in Python
=====================================
Run this file to see ALL OOP concepts demonstrated with clear output.

Usage: python oop_demo.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import total_ordering


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ============================================================
# 1. CLASS DEFINITION: __init__, __str__, __repr__
# ============================================================

section("1. Class Definition: __init__, __str__, __repr__")


class Book:
    """A simple class demonstrating __init__, __str__, and __repr__."""

    def __init__(self, title: str, author: str, pages: int):
        self.title = title
        self.author = author
        self.pages = pages

    def __str__(self) -> str:
        """Human-readable string (for print(), str())."""
        return f"'{self.title}' by {self.author}"

    def __repr__(self) -> str:
        """Developer-readable string (for debugging, repr())."""
        return f"Book(title={self.title!r}, author={self.author!r}, pages={self.pages})"


book = Book("Clean Code", "Robert Martin", 464)
print(f"str(book):  {str(book)}")       # Calls __str__
print(f"repr(book): {repr(book)}")      # Calls __repr__
print(f"print(book): {book}")           # Calls __str__
print(f"In list: {[book]}")             # Uses __repr__ inside containers


# ============================================================
# 2. ENCAPSULATION: @property, private attributes
# ============================================================

section("2. Encapsulation: @property and Private Attributes")


class BankAccount:
    """Demonstrates encapsulation with @property."""

    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner            # Protected (convention)
        self.__balance = initial_balance  # Name-mangled (private)

    @property
    def owner(self) -> str:
        """Read-only property."""
        return self._owner

    @property
    def balance(self) -> float:
        """Read-only balance with controlled access."""
        return self.__balance

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.__balance += amount
        print(f"  Deposited ${amount:.2f}. New balance: ${self.__balance:.2f}")

    def withdraw(self, amount: float):
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        self.__balance -= amount
        print(f"  Withdrew ${amount:.2f}. New balance: ${self.__balance:.2f}")


account = BankAccount("Alice", 100.0)
print(f"Owner: {account.owner}")
print(f"Balance: ${account.balance:.2f}")
account.deposit(50)
account.withdraw(30)

# Trying to set read-only property:
try:
    account.owner = "Bob"
except AttributeError as e:
    print(f"  Cannot set owner: {e}")

# Trying to access private attribute directly:
try:
    print(account.__balance)
except AttributeError:
    print("  Cannot access __balance directly (name mangling)")
    print(f"  But can via name mangling: account._BankAccount__balance = {account._BankAccount__balance}")


# ============================================================
# 3. INHERITANCE: Single, Multi-level, Method Overriding
# ============================================================

section("3. Inheritance: Single, Multi-level, Method Overriding")


# --- Single Inheritance ---
class Animal:
    def __init__(self, name: str):
        self.name = name

    def speak(self) -> str:
        return "..."

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


class Cat(Animal):
    def speak(self) -> str:
        return "Meow!"


dog = Dog("Rex")
cat = Cat("Whiskers")
print(f"{dog} says: {dog.speak()}")
print(f"{cat} says: {cat.speak()}")


# --- Multi-level Inheritance ---
class Puppy(Dog):
    """Puppy inherits from Dog which inherits from Animal."""
    def speak(self) -> str:
        return "Yip!"

    def parent_speak(self) -> str:
        """Call parent's method using super()."""
        return super().speak()


puppy = Puppy("Tiny")
print(f"{puppy} says: {puppy.speak()}")
print(f"{puppy}'s parent says: {puppy.parent_speak()}")
print(f"MRO for Puppy: {[c.__name__ for c in Puppy.__mro__]}")


# --- Method Overriding with super() ---
class GuideDog(Dog):
    def __init__(self, name: str, handler: str):
        super().__init__(name)  # Call parent's __init__
        self.handler = handler

    def speak(self) -> str:
        base = super().speak()
        return f"{base} (Trained guide dog for {self.handler})"


guide = GuideDog("Buddy", "John")
print(f"{guide} says: {guide.speak()}")


# ============================================================
# 4. POLYMORPHISM: Duck Typing and ABC
# ============================================================

section("4. Polymorphism: Duck Typing and ABC")


# --- Duck Typing ---
class Duck:
    def quack(self):
        return "Quack!"

    def swim(self):
        return "Swimming..."


class Person:
    def quack(self):
        return "I'm quacking like a duck!"

    def swim(self):
        return "I'm swimming like a duck!"


def make_it_quack(thing):
    """Doesn't care about type - just needs a quack() method."""
    print(f"  {thing.__class__.__name__}: {thing.quack()}")


print("Duck typing - any object with quack() works:")
make_it_quack(Duck())
make_it_quack(Person())


# --- Polymorphism through ABC ---
class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def perimeter(self) -> float:
        pass

    def describe(self) -> str:
        return (f"{self.__class__.__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


print("\nPolymorphism through ABC:")
shapes: list[Shape] = [Circle(5), Rectangle(4, 6)]
for shape in shapes:
    print(f"  {shape.describe()}")

# Cannot instantiate abstract class:
try:
    s = Shape()
except TypeError as e:
    print(f"\n  Cannot instantiate ABC: {e}")


# ============================================================
# 5. COMPOSITION vs INHERITANCE
# ============================================================

section("5. Composition vs Inheritance")


# --- BAD: Inheritance for code reuse (IS-A misuse) ---
class InheritanceEngine:
    def start(self):
        return "Engine started"


class InheritanceCar(InheritanceEngine):
    """BAD: Car IS-A Engine? No! Car HAS-A Engine."""
    pass


# --- GOOD: Composition (HAS-A) ---
class Engine:
    def __init__(self, horsepower: int):
        self.horsepower = horsepower

    def start(self) -> str:
        return f"Engine ({self.horsepower}hp) started"

    def stop(self) -> str:
        return "Engine stopped"


class Transmission:
    def __init__(self, gear_type: str):
        self.gear_type = gear_type

    def shift(self, gear: int) -> str:
        return f"{self.gear_type} shifted to gear {gear}"


class Car:
    """GOOD: Car HAS-A Engine and HAS-A Transmission."""

    def __init__(self, model: str, engine: Engine, transmission: Transmission):
        self.model = model
        self._engine = engine           # Composition
        self._transmission = transmission  # Composition

    def drive(self) -> str:
        return (f"{self.model}: {self._engine.start()}, "
                f"{self._transmission.shift(1)}")


car = Car("Tesla Model 3",
          Engine(450),
          Transmission("Automatic"))
print(f"Composition: {car.drive()}")
print("\nWhy composition wins:")
print("  - Can swap engine at runtime (dependency injection)")
print("  - Car and Engine can evolve independently")
print("  - Engine can be reused in Boat, Airplane, etc.")


# ============================================================
# 6. ABSTRACT CLASS with ABC
# ============================================================

section("6. Abstract Class with ABC")


class PaymentProcessor(ABC):
    """Abstract class with both abstract and concrete methods."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        """Must be implemented by subclasses."""
        pass

    @abstractmethod
    def refund(self, transaction_id: str) -> bool:
        """Must be implemented by subclasses."""
        pass

    def log_transaction(self, amount: float, status: str):
        """Concrete method - shared by all subclasses."""
        print(f"  [{self.name}] Transaction: ${amount:.2f} - {status}")


class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        self.log_transaction(amount, "APPROVED")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"  [{self.name}] Refund for {transaction_id}: PROCESSED")
        return True


class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> bool:
        self.log_transaction(amount, "APPROVED via PayPal")
        return True

    def refund(self, transaction_id: str) -> bool:
        print(f"  [{self.name}] PayPal refund {transaction_id}: PROCESSED")
        return True


processors: list[PaymentProcessor] = [
    CreditCardProcessor("Visa"),
    PayPalProcessor("PayPal"),
]

for proc in processors:
    proc.process_payment(99.99)
    proc.refund("TXN-001")


# ============================================================
# 7. MIXIN CLASSES
# ============================================================

section("7. Mixin Classes")


class JsonMixin:
    """Mixin: adds JSON serialization to any class."""

    def to_json(self) -> str:
        import json
        return json.dumps(self.__dict__, default=str)


class LogMixin:
    """Mixin: adds logging capability to any class."""

    def log(self, message: str):
        print(f"  LOG [{self.__class__.__name__}]: {message}")


class User(JsonMixin, LogMixin):
    """User class gains JSON + Logging via mixins."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class Product(JsonMixin, LogMixin):
    """Product class gains the same capabilities."""

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price


user = User("Alice", "alice@example.com")
product = Product("Laptop", 999.99)

print(f"User JSON: {user.to_json()}")
print(f"Product JSON: {product.to_json()}")
user.log("User created")
product.log("Product listed")

print(f"\nMRO for User: {[c.__name__ for c in User.__mro__]}")


# ============================================================
# 8. MAGIC METHODS: __eq__, __hash__, __lt__
# ============================================================

section("8. Magic Methods: __eq__, __hash__, __lt__")


@total_ordering  # Generates __le__, __gt__, __ge__ from __lt__ and __eq__
class Money:
    """Demonstrates comparison and hashing magic methods."""

    def __init__(self, amount: float, currency: str = "USD"):
        self.amount = amount
        self.currency = currency

    def __eq__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError(f"Cannot compare {self.currency} with {other.currency}")
        return self.amount < other.amount

    def __hash__(self) -> int:
        """Required for use in sets and as dict keys."""
        return hash((self.amount, self.currency))

    def __add__(self, other) -> 'Money':
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)

    def __repr__(self) -> str:
        return f"Money({self.amount}, '{self.currency}')"


a = Money(10.00)
b = Money(20.00)
c = Money(10.00)

print(f"a = {a}, b = {b}, c = {c}")
print(f"a == c: {a == c}")      # __eq__
print(f"a == b: {a == b}")
print(f"a < b:  {a < b}")       # __lt__
print(f"a > b:  {a > b}")       # Generated by @total_ordering
print(f"a + b:  {a + b}")       # __add__

# __hash__ enables use in sets and dicts
money_set = {a, b, c}  # c is duplicate of a
print(f"\nSet: {money_set}")
print(f"Set has {len(money_set)} items (duplicates removed via __hash__ + __eq__)")

money_dict = {a: "ten bucks", b: "twenty bucks"}
print(f"Dict lookup: money_dict[Money(10.00)] = '{money_dict[Money(10.00)]}'")


# ============================================================
# 9. DATACLASSES
# ============================================================

section("9. Dataclasses")


@dataclass
class Point:
    """Dataclass auto-generates __init__, __repr__, __eq__."""
    x: float
    y: float

    def distance_to(self, other: 'Point') -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


@dataclass(frozen=True)  # Immutable - also makes it hashable
class Color:
    r: int
    g: int
    b: int


@dataclass
class Player:
    name: str
    score: int = 0
    achievements: list[str] = field(default_factory=list)  # Mutable default

    def add_achievement(self, achievement: str):
        self.achievements.append(achievement)
        self.score += 10


p1 = Point(3, 4)
p2 = Point(0, 0)
print(f"Point: {p1}")                          # Auto __repr__
print(f"Distance: {p1.distance_to(p2):.2f}")
print(f"p1 == Point(3, 4): {p1 == Point(3, 4)}")  # Auto __eq__

red = Color(255, 0, 0)
print(f"\nFrozen Color: {red}")
try:
    red.r = 100
except Exception as e:
    print(f"Cannot modify frozen: {e}")

print(f"Color hashable (usable in sets): {hash(red)}")

player = Player("Alice")
player.add_achievement("First Kill")
player.add_achievement("Level Up")
print(f"\nPlayer: {player}")


# ============================================================
# SUMMARY
# ============================================================

section("SUMMARY: OOP Concepts Covered")

concepts = [
    ("__init__, __str__, __repr__", "Object creation and string representation"),
    ("Encapsulation (@property)", "Controlled access to internal state"),
    ("Inheritance", "Single, multi-level, method overriding with super()"),
    ("Polymorphism", "Duck typing + ABC abstract methods"),
    ("Composition vs Inheritance", "HAS-A vs IS-A relationships"),
    ("Abstract Base Classes", "ABC with abstract + concrete methods"),
    ("Mixin Classes", "Reusable behavior via multiple inheritance"),
    ("Magic Methods", "__eq__, __hash__, __lt__, __add__"),
    ("Dataclasses", "Auto-generated __init__, __repr__, __eq__, frozen"),
]

for concept, description in concepts:
    print(f"  {concept:<35} -> {description}")

print(f"\nTotal concepts demonstrated: {len(concepts)}")
print("All demos are runnable - execute this file to see output!")
