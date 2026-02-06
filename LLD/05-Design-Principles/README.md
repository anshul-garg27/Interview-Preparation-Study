# Design Principles - Beyond SOLID

## Table of Contents
- [Introduction](#introduction)
- [1. DRY (Don't Repeat Yourself)](#1-dry-dont-repeat-yourself)
- [2. KISS (Keep It Simple, Stupid)](#2-kiss-keep-it-simple-stupid)
- [3. YAGNI (You Aren't Gonna Need It)](#3-yagni-you-arent-gonna-need-it)
- [4. Composition over Inheritance](#4-composition-over-inheritance)
- [5. Law of Demeter](#5-law-of-demeter-principle-of-least-knowledge)
- [6. Tell, Don't Ask](#6-tell-dont-ask)
- [7. Program to an Interface](#7-program-to-an-interface-not-implementation)
- [8. Favor Immutability](#8-favor-immutability)
- [9. GRASP Patterns](#9-grasp-patterns)
- [10. Code Smells](#10-code-smells)

---

## Introduction

SOLID principles are foundational, but experienced engineers follow additional design principles that lead to cleaner, more maintainable code. These principles complement SOLID and are frequently tested in LLD interviews through code design decisions.

---

## 1. DRY (Don't Repeat Yourself)

**"Every piece of knowledge must have a single, unambiguous, authoritative representation within a system."**

DRY is NOT just about duplicated code. It is about duplicated **knowledge**. Two identical-looking code blocks that change for different reasons are NOT a DRY violation.

### Violation: Duplicated Validation Logic

```python
# BAD: Validation logic duplicated across methods
class UserService:
    def register_user(self, email: str, password: str):
        # Email validation duplicated
        if not email or "@" not in email or "." not in email.split("@")[1]:
            raise ValueError("Invalid email")
        # Password validation duplicated
        if len(password) < 8 or not any(c.isupper() for c in password):
            raise ValueError("Weak password")
        # ... register logic

    def update_email(self, user_id: str, new_email: str):
        # Same email validation copy-pasted
        if not new_email or "@" not in new_email or "." not in new_email.split("@")[1]:
            raise ValueError("Invalid email")
        # ... update logic

    def reset_password(self, user_id: str, new_password: str):
        # Same password validation copy-pasted
        if len(new_password) < 8 or not any(c.isupper() for c in new_password):
            raise ValueError("Weak password")
        # ... reset logic
```

### Fix: Single Source of Truth

```python
# GOOD: Validation logic centralized
class EmailValidator:
    @staticmethod
    def validate(email: str) -> None:
        if not email or "@" not in email:
            raise ValueError("Invalid email")
        if "." not in email.split("@")[1]:
            raise ValueError("Invalid email domain")


class PasswordValidator:
    MIN_LENGTH = 8

    @staticmethod
    def validate(password: str) -> None:
        if len(password) < PasswordValidator.MIN_LENGTH:
            raise ValueError(f"Password must be at least {PasswordValidator.MIN_LENGTH} chars")
        if not any(c.isupper() for c in password):
            raise ValueError("Password must contain an uppercase letter")


class UserService:
    def register_user(self, email: str, password: str):
        EmailValidator.validate(email)
        PasswordValidator.validate(password)
        # ... register logic

    def update_email(self, user_id: str, new_email: str):
        EmailValidator.validate(new_email)
        # ... update logic

    def reset_password(self, user_id: str, new_password: str):
        PasswordValidator.validate(new_password)
        # ... reset logic
```

### When NOT to Apply DRY

Two pieces of code that look identical but represent **different domain concepts** should remain separate. Premature DRY extraction couples unrelated concerns.

```python
# These look similar but change for different reasons - keep them separate
def calculate_employee_tax(salary: float) -> float:
    return salary * 0.30  # Tax policy

def calculate_vendor_commission(revenue: float) -> float:
    return revenue * 0.30  # Business rule
```

---

## 2. KISS (Keep It Simple, Stupid)

**"The simplest solution that works is usually the best."**

Over-engineering is one of the most common sins in software design. If a simple approach solves the problem, do not introduce unnecessary complexity.

### Violation: Over-Engineered Solution

```python
# BAD: Over-engineered for a simple task
from abc import ABC, abstractmethod

class FilterStrategy(ABC):
    @abstractmethod
    def apply(self, items: list, predicate) -> list:
        pass

class ListFilterStrategy(FilterStrategy):
    def apply(self, items: list, predicate) -> list:
        return [item for item in items if predicate(item)]

class FilterContext:
    def __init__(self, strategy: FilterStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: FilterStrategy):
        self._strategy = strategy

    def execute(self, items: list, predicate) -> list:
        return self._strategy.apply(items, predicate)

# Usage for a simple filter operation
context = FilterContext(ListFilterStrategy())
adults = context.execute(users, lambda u: u.age >= 18)
```

### Fix: Simple and Direct

```python
# GOOD: Simple, readable, Pythonic
adults = [user for user in users if user.age >= 18]
```

### Another Example: Simple Status Check

```python
# BAD: Unnecessary abstraction
class StatusChecker:
    _handlers = {}

    @classmethod
    def register(cls, status, handler):
        cls._handlers[status] = handler

    @classmethod
    def check(cls, order):
        handler = cls._handlers.get(order.status)
        if handler:
            return handler(order)
        raise ValueError(f"Unknown status: {order.status}")

# GOOD: Direct and readable
def is_order_complete(order) -> bool:
    return order.status in ("DELIVERED", "COMPLETED")
```

**Rule of thumb**: If your abstraction is harder to understand than the problem it solves, it is too complex.

---

## 3. YAGNI (You Aren't Gonna Need It)

**"Always implement things when you actually need them, never when you just foresee that you need them."**

YAGNI fights premature abstraction. Do not build features, extension points, or configurations for hypothetical future requirements.

### Violation: Premature Abstraction

```python
# BAD: Building for a future that may never come
class NotificationService:
    """Supports email, SMS, push, carrier pigeon, and smoke signals.
    Currently only email is used."""

    def __init__(self):
        self._channels: dict[str, NotificationChannel] = {}
        self._retry_policy = RetryPolicy()
        self._rate_limiter = RateLimiter()
        self._template_engine = TemplateEngine()
        self._channel_priority_queue = PriorityQueue()
        self._fallback_chain = FallbackChain()
        self._delivery_tracker = DeliveryTracker()

    def register_channel(self, name: str, channel: NotificationChannel):
        self._channels[name] = channel

    def send(self, message: str, channels: list[str] = None,
             priority: int = 0, retry: bool = True,
             template: str = None, fallback: bool = True):
        # 200 lines of "flexible" code...
        pass
```

### Fix: Build What You Need Now

```python
# GOOD: Solve today's problem
class EmailNotifier:
    def __init__(self, smtp_client):
        self._smtp = smtp_client

    def send(self, to: str, subject: str, body: str) -> None:
        self._smtp.send_mail(to=to, subject=subject, body=body)
```

When you actually need SMS support, refactor then. The refactoring cost is almost always lower than the cost of maintaining unused abstractions.

### Signs You Are Violating YAGNI

- "We might need this later"
- "What if we want to support X in the future?"
- Configuration options nobody uses
- Abstract base classes with only one implementation
- Plugin systems with no plugins

---

## 4. Composition over Inheritance

**"Favor object composition over class inheritance."** -- Gang of Four

Inheritance creates tight coupling and rigid hierarchies. Composition gives flexibility, testability, and avoids the fragile base class problem.

### The Problem with Deep Inheritance

```python
# BAD: Inheritance hierarchy becomes a trap
class Animal:
    def eat(self): print("Eating")
    def sleep(self): print("Sleeping")

class Bird(Animal):
    def fly(self): print("Flying")

class Penguin(Bird):  # Problem! Penguins can't fly
    def fly(self):
        raise NotImplementedError("Penguins can't fly")  # LSP violation

class FlyingFish(Animal):  # Can fly but isn't a bird...
    def fly(self): print("Flying")  # Duplicated from Bird
    def swim(self): print("Swimming")
```

### Fix: Composition with Behaviors

```python
# GOOD: Compose behaviors
from abc import ABC, abstractmethod

class MovementBehavior(ABC):
    @abstractmethod
    def move(self) -> str:
        pass

class FlyBehavior(MovementBehavior):
    def move(self) -> str:
        return "Flying through the air"

class SwimBehavior(MovementBehavior):
    def move(self) -> str:
        return "Swimming in water"

class WalkBehavior(MovementBehavior):
    def move(self) -> str:
        return "Walking on land"

class NoMoveBehavior(MovementBehavior):
    def move(self) -> str:
        return "Cannot move"


class Animal:
    def __init__(self, name: str, movements: list[MovementBehavior]):
        self.name = name
        self._movements = movements

    def perform_movements(self) -> list[str]:
        return [m.move() for m in self._movements]


# Flexible composition - no hierarchy problems
eagle = Animal("Eagle", [FlyBehavior(), WalkBehavior()])
penguin = Animal("Penguin", [SwimBehavior(), WalkBehavior()])
flying_fish = Animal("FlyingFish", [FlyBehavior(), SwimBehavior()])
```

### When Inheritance IS Appropriate

- True "is-a" relationships that won't change (e.g., `IOException extends Exception`)
- Template Method pattern where you control the base class
- Shallow hierarchies (1-2 levels max)
- When the language/framework requires it

### Comparison

| Aspect | Inheritance | Composition |
|--------|-------------|-------------|
| Coupling | Tight (white-box reuse) | Loose (black-box reuse) |
| Flexibility | Static (compile-time) | Dynamic (runtime) |
| Testability | Harder (need base class) | Easier (mock components) |
| Code reuse | Via class hierarchy | Via delegation |
| Hierarchy depth | Can grow deep | Flat |

---

## 5. Law of Demeter (Principle of Least Knowledge)

**"Only talk to your immediate friends. Don't talk to strangers."**

A method should only call methods on:
1. Its own object (`self`)
2. Objects passed as parameters
3. Objects it creates
4. Its direct component objects

### Violation: Train Wreck Code

```python
# BAD: Reaching deep into object chains
class OrderProcessor:
    def process(self, order):
        # Chaining through multiple objects - fragile!
        city = order.get_customer().get_address().get_city()
        tax_rate = self.tax_service.get_rate_for(city)

        # What if customer has no address? What if address format changes?
        zip_code = order.get_customer().get_address().get_zip_code()

        # Tight coupling to the entire object graph
        card_last_four = order.get_customer().get_wallet().get_default_card().get_last_four()
```

### Fix: Tell, Don't Ask (Delegate)

```python
# GOOD: Each object exposes only what's needed
class Customer:
    def __init__(self, name: str, address: "Address", wallet: "Wallet"):
        self._name = name
        self._address = address
        self._wallet = wallet

    def get_city(self) -> str:
        return self._address.city

    def get_zip_code(self) -> str:
        return self._address.zip_code

    def get_payment_display(self) -> str:
        return self._wallet.get_default_card_display()


class Order:
    def __init__(self, customer: Customer):
        self._customer = customer

    def get_shipping_city(self) -> str:
        return self._customer.get_city()


class OrderProcessor:
    def process(self, order: Order):
        city = order.get_shipping_city()  # Only one dot!
        tax_rate = self.tax_service.get_rate_for(city)
```

### Quick Test

Count the dots. More than one dot in a chain (excluding fluent builders) is a Law of Demeter violation.

```python
# Violations (multiple dots reaching into structure):
order.customer.address.city
user.get_profile().get_settings().get_theme()

# OK (fluent API / builder pattern - same object returned):
QueryBuilder().select("*").from_table("users").where("age > 18").build()
```

---

## 6. Tell, Don't Ask

**"Tell objects what to do, don't ask them for data and then act on it."**

Procedural code gets data then makes decisions. Object-oriented code tells objects to do things.

### Violation: Procedural Style (Ask, Then Act)

```python
# BAD: Asking for data, then making decisions externally
class BankAccount:
    def __init__(self):
        self.balance = 0.0
        self.overdraft_limit = -500.0
        self.is_frozen = False

def transfer(source: BankAccount, target: BankAccount, amount: float):
    # Asking for internal state and making decisions externally
    if source.is_frozen:
        raise ValueError("Account frozen")
    if source.balance - amount < source.overdraft_limit:
        raise ValueError("Insufficient funds")

    source.balance -= amount
    target.balance += amount
```

### Fix: OO Style (Tell)

```python
# GOOD: Tell the object what to do; it handles its own logic
class BankAccount:
    def __init__(self, balance: float = 0.0, overdraft_limit: float = -500.0):
        self._balance = balance
        self._overdraft_limit = overdraft_limit
        self._is_frozen = False

    def withdraw(self, amount: float) -> None:
        if self._is_frozen:
            raise ValueError("Account is frozen")
        if self._balance - amount < self._overdraft_limit:
            raise ValueError("Insufficient funds")
        self._balance -= amount

    def deposit(self, amount: float) -> None:
        if self._is_frozen:
            raise ValueError("Account is frozen")
        self._balance += amount

    def transfer_to(self, target: "BankAccount", amount: float) -> None:
        self.withdraw(amount)  # Tell self to withdraw
        target.deposit(amount)  # Tell target to deposit
```

### Key Difference

| Aspect | Ask (Procedural) | Tell (OO) |
|--------|-------------------|-----------|
| Data exposure | Public fields / getters | Private, encapsulated |
| Logic location | External to the object | Inside the object |
| Coupling | High (caller knows internals) | Low (caller knows interface) |
| Maintainability | Change one rule = change many callers | Change one rule = change one class |

---

## 7. Program to an Interface, Not Implementation

**"Depend on abstractions, not concretions."**

Code should depend on abstract contracts (interfaces/protocols), not specific implementations. This enables flexibility, testability, and adherence to the Dependency Inversion Principle.

### Violation: Coupled to Implementation

```python
# BAD: Tightly coupled to specific implementations
class OrderService:
    def __init__(self):
        self._db = MySQLDatabase()  # Hardcoded to MySQL
        self._mailer = SmtpEmailSender()  # Hardcoded to SMTP
        self._logger = FileLogger()  # Hardcoded to file

    def place_order(self, order):
        self._db.insert("orders", order.to_dict())
        self._mailer.send_smtp_email(order.customer_email, "Order placed")
        self._logger.write_to_file(f"Order {order.id} placed")
```

### Fix: Depend on Abstractions (Dependency Injection)

```python
# GOOD: Depend on interfaces, inject implementations
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, table: str, data: dict) -> None:
        pass

class Notifier(ABC):
    @abstractmethod
    def notify(self, recipient: str, message: str) -> None:
        pass

class Logger(ABC):
    @abstractmethod
    def log(self, message: str) -> None:
        pass


# Concrete implementations
class MySQLDatabase(Database):
    def save(self, table: str, data: dict) -> None:
        # MySQL-specific logic
        pass

class PostgresDatabase(Database):
    def save(self, table: str, data: dict) -> None:
        # Postgres-specific logic
        pass

class EmailNotifier(Notifier):
    def notify(self, recipient: str, message: str) -> None:
        # Send email
        pass

class SmsNotifier(Notifier):
    def notify(self, recipient: str, message: str) -> None:
        # Send SMS
        pass


# Service depends only on abstractions
class OrderService:
    def __init__(self, db: Database, notifier: Notifier, logger: Logger):
        self._db = db
        self._notifier = notifier
        self._logger = logger

    def place_order(self, order):
        self._db.save("orders", order.to_dict())
        self._notifier.notify(order.customer_email, "Order placed")
        self._logger.log(f"Order {order.id} placed")


# Easy to swap implementations
service = OrderService(
    db=PostgresDatabase(),
    notifier=SmsNotifier(),
    logger=ConsoleLogger()
)
```

### Benefits

1. **Testability**: Inject mock implementations for unit tests
2. **Flexibility**: Swap implementations without changing business logic
3. **Decoupling**: Classes don't know or care about implementation details
4. **Open/Closed**: Add new implementations without modifying existing code

---

## 8. Favor Immutability

**"Immutable objects are simpler, safer, and easier to reason about."**

An immutable object cannot be modified after creation. Any "change" produces a new object.

### Why Immutability Matters

1. **Thread safety**: No synchronization needed -- immutable objects can be freely shared
2. **Predictability**: No surprising mutations from other code
3. **Hashability**: Immutable objects can be used as dict keys and set members
4. **Debugging**: State at creation = state forever, easier to trace bugs

### Mutable (Risky)

```python
# BAD: Mutable objects lead to subtle bugs
class Money:
    def __init__(self, amount: float, currency: str):
        self.amount = amount
        self.currency = currency

    def add(self, other: "Money") -> "Money":
        self.amount += other.amount  # Mutates in place!
        return self

price = Money(100, "USD")
tax = Money(10, "USD")

total = price.add(tax)
print(price.amount)  # 110 -- price was mutated! Bug.
print(total.amount)  # 110
print(price is total)  # True -- same object!
```

### Immutable (Safe)

```python
# GOOD: Immutable Money class
from dataclasses import dataclass

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)  # New object

    def subtract(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount - other.amount, self.currency)


price = Money(100, "USD")
tax = Money(10, "USD")

total = price.add(tax)
print(price.amount)   # 100 -- unchanged
print(total.amount)   # 110 -- new object
print(price is total)  # False
```

### Python Tools for Immutability

```python
# 1. frozen dataclass
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# 2. NamedTuple
from typing import NamedTuple

class Color(NamedTuple):
    r: int
    g: int
    b: int

# 3. Using __slots__ and property (manual approach)
class Temperature:
    __slots__ = ("_value", "_unit")

    def __init__(self, value: float, unit: str):
        object.__setattr__(self, "_value", value)
        object.__setattr__(self, "_unit", unit)

    def __setattr__(self, name, value):
        raise AttributeError("Temperature is immutable")

    @property
    def value(self) -> float:
        return self._value

    @property
    def unit(self) -> str:
        return self._unit
```

### When Mutability Is Acceptable

- Builder pattern during construction
- Performance-critical inner loops
- Objects with inherently mutable state (e.g., connection pools)

---

## 9. GRASP Patterns

**GRASP** (General Responsibility Assignment Software Patterns) provide guidelines for assigning responsibilities to classes. These are not design patterns -- they are principles for deciding **which class should do what**.

### 9.1 Information Expert

**Assign responsibility to the class that has the information needed to fulfill it.**

```python
# BAD: External class calculates order total
class OrderCalculator:
    def calculate_total(self, order):
        total = 0
        for item in order.items:  # Reaching into order's data
            total += item.price * item.quantity
        return total

# GOOD: Order calculates its own total (it has the data)
class Order:
    def __init__(self):
        self._items: list[OrderItem] = []

    def get_total(self) -> float:
        return sum(item.get_subtotal() for item in self._items)

class OrderItem:
    def __init__(self, price: float, quantity: int):
        self._price = price
        self._quantity = quantity

    def get_subtotal(self) -> float:
        return self._price * self._quantity
```

### 9.2 Creator

**Class B should create instances of class A if B contains/aggregates A, B closely uses A, or B has the data to initialize A.**

```python
# GOOD: Order creates OrderItems (it aggregates them)
class Order:
    def __init__(self):
        self._items: list[OrderItem] = []

    def add_item(self, product: Product, quantity: int) -> None:
        item = OrderItem(product.price, quantity, product.name)  # Order creates OrderItem
        self._items.append(item)
```

### 9.3 Controller

**Assign system event handling to a non-UI class that represents the overall system or a use case scenario.**

```python
# BAD: UI directly manipulates domain objects
class CheckoutButton:
    def on_click(self):
        order = Order()
        order.add_items(cart.items)
        payment = PaymentGateway()
        payment.charge(order.total)
        inventory.reduce_stock(order.items)
        emailer.send_confirmation(order)

# GOOD: Controller coordinates the use case
class CheckoutController:
    def __init__(self, payment_service, inventory_service, notification_service):
        self._payment = payment_service
        self._inventory = inventory_service
        self._notification = notification_service

    def checkout(self, cart: Cart, customer: Customer) -> Order:
        order = Order.from_cart(cart, customer)
        self._payment.process(order)
        self._inventory.reserve(order.items)
        self._notification.send_confirmation(order)
        return order
```

### 9.4 Low Coupling

**Minimize dependencies between classes.** A class with low coupling is not dependent on too many other classes.

```python
# BAD: High coupling - OrderService depends on everything
class OrderService:
    def __init__(self):
        self.mysql_db = MySQLDatabase()
        self.stripe_payment = StripePayment()
        self.sendgrid_email = SendGridEmail()
        self.twilio_sms = TwilioSMS()
        self.redis_cache = RedisCache()

# GOOD: Low coupling via abstractions
class OrderService:
    def __init__(self, db: Database, payment: PaymentGateway, notifier: Notifier):
        self._db = db
        self._payment = payment
        self._notifier = notifier
```

### 9.5 High Cohesion

**Keep related responsibilities together in a single class.** A highly cohesive class does one thing well.

```python
# BAD: Low cohesion - class does too many unrelated things
class UserManager:
    def create_user(self, data): pass
    def send_email(self, to, body): pass
    def generate_report(self): pass
    def backup_database(self): pass
    def resize_image(self, path): pass

# GOOD: High cohesion - each class has focused responsibilities
class UserService:
    def create_user(self, data): pass
    def update_user(self, user_id, data): pass
    def deactivate_user(self, user_id): pass

class EmailService:
    def send_email(self, to, body): pass

class ReportService:
    def generate_report(self): pass
```

### GRASP Quick Reference

| Pattern | Question It Answers |
|---------|-------------------|
| Information Expert | "Which class should have this method?" |
| Creator | "Which class should create this object?" |
| Controller | "Which class should handle this system event?" |
| Low Coupling | "How do I minimize dependencies?" |
| High Cohesion | "How do I keep classes focused?" |

---

## 10. Code Smells

Code smells are symptoms of deeper design problems. They indicate that a refactoring may be needed.

### 10.1 God Class (Blob)

A class that knows too much or does too much. It centralizes the intelligence of the system.

```python
# SMELL: God class
class Application:
    def __init__(self):
        self.users = []
        self.orders = []
        self.products = []
        self.payments = []

    def register_user(self, data): pass
    def authenticate_user(self, credentials): pass
    def create_order(self, user_id, items): pass
    def process_payment(self, order_id, card): pass
    def send_notification(self, user_id, message): pass
    def generate_invoice(self, order_id): pass
    def calculate_tax(self, order_id): pass
    def update_inventory(self, product_id, qty): pass
    def generate_report(self, report_type): pass
    # ... 50 more methods
```

**Fix**: Break into focused classes (UserService, OrderService, PaymentService, etc.)

### 10.2 Feature Envy

A method that uses more features of another class than its own. It "envies" another class's data.

```python
# SMELL: Feature envy - method uses order's data extensively
class InvoiceGenerator:
    def generate(self, order):
        customer_name = order.customer.name
        customer_address = order.customer.address
        items = order.items
        subtotal = sum(item.price * item.qty for item in items)
        tax = subtotal * order.tax_rate
        shipping = order.shipping_cost
        total = subtotal + tax + shipping
        # ... format invoice

# FIX: Move the logic to where the data lives
class Order:
    def get_subtotal(self) -> float:
        return sum(item.get_total() for item in self._items)

    def get_tax(self) -> float:
        return self.get_subtotal() * self._tax_rate

    def get_total(self) -> float:
        return self.get_subtotal() + self.get_tax() + self._shipping_cost

    def get_invoice_data(self) -> dict:
        return {
            "customer": self._customer.get_display_info(),
            "items": [item.to_dict() for item in self._items],
            "subtotal": self.get_subtotal(),
            "tax": self.get_tax(),
            "total": self.get_total(),
        }
```

### 10.3 Shotgun Surgery

A single change requires modifications in many different classes. The opposite of high cohesion.

```python
# SMELL: Adding a new user field requires changes everywhere
# 1. User model
# 2. UserService
# 3. UserValidator
# 4. UserSerializer
# 5. UserView
# 6. UserTest
# 7. UserMigration
# 8. UserDTO

# FIX: Consolidate related logic. Use patterns like:
# - Value objects to group related fields
# - Single class responsible for a concept
# - Events/observers for cross-cutting concerns
```

### 10.4 Primitive Obsession

Using primitives (str, int, float) instead of small domain objects.

```python
# SMELL: Primitives everywhere
def create_order(
    customer_email: str,       # Should be Email value object
    phone: str,                # Should be PhoneNumber value object
    amount: float,             # Should be Money value object
    currency: str,             # Part of Money
    address_line1: str,        # Should be Address value object
    address_line2: str,
    city: str,
    state: str,
    zip_code: str,
    country: str
):
    pass

# FIX: Use value objects
@dataclass(frozen=True)
class Email:
    value: str
    def __post_init__(self):
        if "@" not in self.value:
            raise ValueError(f"Invalid email: {self.value}")

@dataclass(frozen=True)
class Money:
    amount: float
    currency: str

@dataclass(frozen=True)
class Address:
    line1: str
    line2: str
    city: str
    state: str
    zip_code: str
    country: str

def create_order(email: Email, phone: PhoneNumber, total: Money, address: Address):
    pass  # Much cleaner
```

### 10.5 Long Parameter List

A method with too many parameters is hard to call, read, and maintain.

```python
# SMELL: Too many parameters
def create_user(first_name, last_name, email, phone, street, city,
                state, zip_code, country, dob, gender, role, department):
    pass

# FIX Option 1: Parameter object
@dataclass
class CreateUserRequest:
    name: FullName
    email: Email
    phone: PhoneNumber
    address: Address
    dob: date
    gender: str
    role: str
    department: str

def create_user(request: CreateUserRequest):
    pass

# FIX Option 2: Builder pattern (for optional params)
user = UserBuilder("John", "Doe") \
    .with_email("john@example.com") \
    .with_phone("555-1234") \
    .with_address(address) \
    .build()
```

### 10.6 Other Common Smells

| Smell | Description | Fix |
|-------|-------------|-----|
| **Dead Code** | Unused classes, methods, variables | Delete it |
| **Speculative Generality** | "What if we need..." abstractions | Apply YAGNI, remove |
| **Data Class** | Class with only fields and getters/setters | Move behavior into the class |
| **Refused Bequest** | Subclass doesn't use inherited methods | Use composition instead |
| **Parallel Inheritance** | Adding subclass in one hierarchy requires adding in another | Merge hierarchies or use composition |
| **Message Chains** | `a.getB().getC().getD()` | Apply Law of Demeter |
| **Middle Man** | Class that only delegates to another | Remove or inline |
| **Inappropriate Intimacy** | Two classes access each other's private details | Reduce coupling, introduce interfaces |

---

## Interview Tips: Design Principles

1. **Don't name-drop without understanding** -- Saying "DRY" without explaining why is worse than not mentioning it
2. **Trade-offs matter** -- Every principle has cases where it shouldn't apply. Discuss trade-offs.
3. **Show, don't tell** -- Demonstrate principles through your code, not by lecturing about them
4. **SOLID + these principles** -- Together they form a complete design toolkit
5. **Refactoring vocabulary** -- Knowing code smells shows maturity as an engineer

---

## Quick Reference Card

```
CORE PRINCIPLES:
  DRY    → One source of truth for each piece of knowledge
  KISS   → Simplest solution that works
  YAGNI  → Build only what you need now

DESIGN GUIDELINES:
  Composition > Inheritance     → Favor "has-a" over "is-a"
  Law of Demeter               → Talk only to immediate friends
  Tell, Don't Ask              → Tell objects what to do
  Program to Interface         → Depend on abstractions
  Favor Immutability           → Safer, simpler, thread-safe

GRASP (Responsibility Assignment):
  Information Expert  → Give method to class with the data
  Creator            → B creates A if B contains/uses A
  Controller         → Non-UI class handles system events
  Low Coupling       → Minimize dependencies
  High Cohesion      → Keep related things together

CODE SMELLS (Red Flags):
  God Class          → Class does everything
  Feature Envy       → Method uses another class's data
  Shotgun Surgery    → One change = many files touched
  Primitive Obsession → Using str/int instead of value objects
  Long Parameter List → Too many method parameters
```

---

*Next: [LLD Problems](../06-LLD-Problems/README.md) | Back to [Design Patterns](../04-Design-Patterns/README.md)*
