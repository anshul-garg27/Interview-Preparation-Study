"""
SOLID Principles Demo in Python
================================
Each principle is shown with a BEFORE (violation) and AFTER (correct) section.
Run this file to see all demonstrations.

Usage: python solid_demo.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol


def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


# ============================================================
# 1. SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# ============================================================
# "A class should have only one reason to change."

section("1. SRP - Single Responsibility Principle")

# --- BEFORE: SRP Violation ---
print("--- BEFORE (Violation) ---")
print("User class does EVERYTHING: validation, persistence, email")


class UserBad:
    """VIOLATION: This class has THREE reasons to change.
    1. User data changes
    2. Database logic changes
    3. Email logic changes
    """

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def validate(self) -> bool:
        # Reason to change: validation rules
        return "@" in self.email and len(self.name) > 0

    def save_to_db(self):
        # Reason to change: database technology
        print(f"  [BAD] INSERT INTO users VALUES ('{self.name}', '{self.email}')")

    def send_welcome_email(self):
        # Reason to change: email template/service
        print(f"  [BAD] Sending email to {self.email}")


bad_user = UserBad("Alice", "alice@example.com")
bad_user.validate()
bad_user.save_to_db()
bad_user.send_welcome_email()

# --- AFTER: SRP Fixed ---
print("\n--- AFTER (Fixed) ---")
print("Each class has ONE reason to change")


class User:
    """Only responsible for user data."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def __repr__(self):
        return f"User({self.name}, {self.email})"


class UserValidator:
    """Only responsible for validation rules."""

    def validate(self, user: User) -> bool:
        is_valid = "@" in user.email and len(user.name) > 0
        print(f"  [GOOD] Validated {user}: {is_valid}")
        return is_valid


class UserRepository:
    """Only responsible for persistence."""

    def save(self, user: User):
        print(f"  [GOOD] Saving {user} to database")


class EmailService:
    """Only responsible for sending emails."""

    def send_welcome(self, user: User):
        print(f"  [GOOD] Sending welcome email to {user.email}")


user = User("Alice", "alice@example.com")
UserValidator().validate(user)
UserRepository().save(user)
EmailService().send_welcome(user)

print("\n  Benefit: Changing email service doesn't affect User or Repository")


# ============================================================
# 2. OPEN/CLOSED PRINCIPLE (OCP)
# ============================================================
# "Open for extension, closed for modification."

section("2. OCP - Open/Closed Principle")

# --- BEFORE: OCP Violation ---
print("--- BEFORE (Violation) ---")
print("Adding a new shape requires modifying AreaCalculator")


class AreaCalculatorBad:
    """VIOLATION: Must modify this class for every new shape."""

    def calculate(self, shape) -> float:
        if shape["type"] == "circle":
            return 3.14159 * shape["radius"] ** 2
        elif shape["type"] == "rectangle":
            return shape["width"] * shape["height"]
        elif shape["type"] == "triangle":
            return 0.5 * shape["base"] * shape["height"]
        # Every new shape = modify this method!
        else:
            raise ValueError(f"Unknown shape: {shape['type']}")


calc_bad = AreaCalculatorBad()
print(f"  Circle area: {calc_bad.calculate({'type': 'circle', 'radius': 5}):.2f}")
print(f"  Rectangle area: {calc_bad.calculate({'type': 'rectangle', 'width': 4, 'height': 6}):.2f}")
print("  Problem: Adding 'triangle' means modifying AreaCalculator!")

# --- AFTER: OCP Fixed ---
print("\n--- AFTER (Fixed) ---")
print("New shapes are added by creating new classes, not modifying existing code")


class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return 3.14159 * self.radius ** 2


class RectangleShape(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class Triangle(Shape):
    """NEW shape - no existing code modified!"""

    def __init__(self, base: float, height: float):
        self.base = base
        self.height = height

    def area(self) -> float:
        return 0.5 * self.base * self.height


class AreaCalculator:
    """NEVER needs to change when new shapes are added."""

    def total_area(self, shapes: list[Shape]) -> float:
        return sum(s.area() for s in shapes)


shapes = [Circle(5), RectangleShape(4, 6), Triangle(3, 8)]
calculator = AreaCalculator()
for s in shapes:
    print(f"  {s.__class__.__name__} area: {s.area():.2f}")
print(f"  Total area: {calculator.total_area(shapes):.2f}")

print("\n  Benefit: Adding Pentagon just needs class Pentagon(Shape) - zero changes elsewhere")


# ============================================================
# 3. LISKOV SUBSTITUTION PRINCIPLE (LSP)
# ============================================================
# "Subtypes must be substitutable for their base types."

section("3. LSP - Liskov Substitution Principle")

# --- BEFORE: LSP Violation ---
print("--- BEFORE (Violation) ---")
print("Square breaks Rectangle's contract")


class RectangleBad:
    def __init__(self, width: float, height: float):
        self._width = width
        self._height = height

    @property
    def width(self) -> float:
        return self._width

    @width.setter
    def width(self, value: float):
        self._width = value

    @property
    def height(self) -> float:
        return self._height

    @height.setter
    def height(self, value: float):
        self._height = value

    def area(self) -> float:
        return self._width * self._height


class SquareBad(RectangleBad):
    """VIOLATION: Overrides setters to maintain square invariant.
    This breaks the contract: setting width shouldn't change height.
    """

    def __init__(self, side: float):
        super().__init__(side, side)

    @RectangleBad.width.setter
    def width(self, value: float):
        self._width = value
        self._height = value  # Surprise! Height changes too!

    @RectangleBad.height.setter
    def height(self, value: float):
        self._width = value  # Surprise! Width changes too!
        self._height = value


def test_rectangle(rect: RectangleBad):
    """This function expects Rectangle behavior."""
    rect.width = 5
    rect.height = 10
    expected = 50  # 5 * 10
    actual = rect.area()
    result = "PASS" if actual == expected else "FAIL"
    print(f"  {rect.__class__.__name__}: expected={expected}, actual={actual} [{result}]")


print("Testing with Rectangle:")
test_rectangle(RectangleBad(0, 0))
print("Testing with Square (substituted for Rectangle):")
test_rectangle(SquareBad(0))  # FAILS! Square is NOT substitutable

# --- AFTER: LSP Fixed ---
print("\n--- AFTER (Fixed) ---")
print("Both Rectangle and Square implement Shape independently")


class ShapeLSP(ABC):
    @abstractmethod
    def area(self) -> float:
        pass


class RectangleGood(ShapeLSP):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


class SquareGood(ShapeLSP):
    """Square is NOT a subtype of Rectangle. Both implement Shape."""

    def __init__(self, side: float):
        self.side = side

    def area(self) -> float:
        return self.side ** 2


def print_area(shape: ShapeLSP):
    print(f"  {shape.__class__.__name__} area: {shape.area():.2f}")


print_area(RectangleGood(5, 10))
print_area(SquareGood(7))
print("\n  Benefit: No surprises - each class fulfills its own contract")


# ============================================================
# 4. INTERFACE SEGREGATION PRINCIPLE (ISP)
# ============================================================
# "Clients should not depend on interfaces they don't use."

section("4. ISP - Interface Segregation Principle")

# --- BEFORE: ISP Violation ---
print("--- BEFORE (Violation) ---")
print("Robot is forced to implement eat() and sleep()")


class WorkerBad(ABC):
    """VIOLATION: Fat interface - forces all methods on all implementors."""

    @abstractmethod
    def work(self): pass

    @abstractmethod
    def eat(self): pass

    @abstractmethod
    def sleep(self): pass


class HumanWorkerBad(WorkerBad):
    def work(self):
        print("  Human working")

    def eat(self):
        print("  Human eating")

    def sleep(self):
        print("  Human sleeping")


class RobotWorkerBad(WorkerBad):
    def work(self):
        print("  Robot working")

    def eat(self):
        # VIOLATION: Robot doesn't eat!
        raise NotImplementedError("Robots don't eat!")

    def sleep(self):
        # VIOLATION: Robot doesn't sleep!
        raise NotImplementedError("Robots don't sleep!")


print("Human worker:")
human_bad = HumanWorkerBad()
human_bad.work()
human_bad.eat()

print("Robot worker:")
robot_bad = RobotWorkerBad()
robot_bad.work()
try:
    robot_bad.eat()
except NotImplementedError as e:
    print(f"  ERROR: {e}")

# --- AFTER: ISP Fixed ---
print("\n--- AFTER (Fixed) ---")
print("Small, focused interfaces - implement only what you need")


class Workable(ABC):
    @abstractmethod
    def work(self): pass


class Eatable(ABC):
    @abstractmethod
    def eat(self): pass


class Sleepable(ABC):
    @abstractmethod
    def sleep(self): pass


class HumanWorker(Workable, Eatable, Sleepable):
    """Human implements all three interfaces."""

    def work(self):
        print("  Human working")

    def eat(self):
        print("  Human eating")

    def sleep(self):
        print("  Human sleeping")


class RobotWorker(Workable):
    """Robot only implements Workable - no forced empty methods!"""

    def work(self):
        print("  Robot working")


class SuperRobot(Workable):
    """Another robot - also only Workable."""

    def work(self):
        print("  Super Robot working at 10x speed")


print("Human:")
human = HumanWorker()
human.work()
human.eat()

print("Robot:")
robot = RobotWorker()
robot.work()
# robot.eat()  # This method doesn't even exist - no violation possible!

print("\n  Benefit: Robot is not forced to implement eat() or sleep()")
print("  Benefit: Can add Chargeable interface for robots without affecting humans")


# ============================================================
# 5. DEPENDENCY INVERSION PRINCIPLE (DIP)
# ============================================================
# "Depend on abstractions, not concretions."

section("5. DIP - Dependency Inversion Principle")

# --- BEFORE: DIP Violation ---
print("--- BEFORE (Violation) ---")
print("NotificationService depends directly on concrete classes")


class SMSSenderBad:
    def send(self, message: str, phone: str):
        print(f"  [BAD] SMS to {phone}: {message}")


class EmailSenderBad:
    def send_email(self, message: str, email: str):
        print(f"  [BAD] Email to {email}: {message}")


class NotificationServiceBad:
    """VIOLATION: Depends on CONCRETE classes, not abstractions.
    Adding PushNotification requires modifying this class.
    """

    def __init__(self):
        self.sms = SMSSenderBad()         # Tight coupling!
        self.email = EmailSenderBad()     # Tight coupling!

    def notify(self, message: str, method: str, recipient: str):
        if method == "sms":
            self.sms.send(message, recipient)
        elif method == "email":
            self.email.send_email(message, recipient)
        # Adding push notification means modifying this class!


bad_service = NotificationServiceBad()
bad_service.notify("Hello!", "sms", "+1234567890")
bad_service.notify("Hello!", "email", "user@example.com")
print("  Problem: Adding PushNotification modifies NotificationService!")

# --- AFTER: DIP Fixed ---
print("\n--- AFTER (Fixed) ---")
print("NotificationService depends on abstraction (NotificationSender)")


class NotificationSender(ABC):
    """Abstraction - both high and low level modules depend on this."""

    @abstractmethod
    def send(self, message: str, recipient: str):
        pass


class SMSSender(NotificationSender):
    def send(self, message: str, recipient: str):
        print(f"  [GOOD] SMS to {recipient}: {message}")


class EmailSender(NotificationSender):
    def send(self, message: str, recipient: str):
        print(f"  [GOOD] Email to {recipient}: {message}")


class PushNotificationSender(NotificationSender):
    """NEW sender - no existing code modified!"""

    def send(self, message: str, recipient: str):
        print(f"  [GOOD] Push to {recipient}: {message}")


class SlackSender(NotificationSender):
    """Another new sender - still no changes needed!"""

    def send(self, message: str, recipient: str):
        print(f"  [GOOD] Slack to #{recipient}: {message}")


class NotificationService:
    """Depends on ABSTRACTION (NotificationSender), not concrete classes.
    New senders are injected - this class never changes.
    """

    def __init__(self, senders: list[NotificationSender]):
        self._senders = senders  # Dependency Injection!

    def notify_all(self, message: str, recipient: str):
        for sender in self._senders:
            sender.send(message, recipient)

    def add_sender(self, sender: NotificationSender):
        self._senders.append(sender)


# Inject dependencies from outside
service = NotificationService([
    SMSSender(),
    EmailSender(),
    PushNotificationSender(),
])
service.notify_all("System alert!", "user123")

# Add Slack at runtime - no code changes!
service.add_sender(SlackSender())
print("\nAfter adding Slack sender:")
service.notify_all("Updated alert!", "user123")

print("\n  Benefit: NotificationService is CLOSED for modification, OPEN for extension")
print("  Benefit: Easy to mock senders for testing")


# ============================================================
# BONUS: Using Python's Protocol (Structural Typing)
# ============================================================

section("BONUS: Protocol-based DIP (Python Structural Typing)")


class MessageSender(Protocol):
    """Protocol: any class with send(str, str) is compatible.
    No inheritance required!
    """

    def send(self, message: str, recipient: str) -> None: ...


class WebhookSender:
    """Does NOT inherit from any ABC - but still works!"""

    def send(self, message: str, recipient: str) -> None:
        print(f"  Webhook to {recipient}: {message}")


class ConsoleSender:
    """Also no inheritance - duck typing via Protocol."""

    def send(self, message: str, recipient: str) -> None:
        print(f"  Console [{recipient}]: {message}")


def send_via(sender: MessageSender, msg: str, to: str):
    """Accepts any object with a send(str, str) method."""
    sender.send(msg, to)


print("Protocol-based (structural typing):")
send_via(WebhookSender(), "Test", "https://hooks.example.com")
send_via(ConsoleSender(), "Test", "admin")
print("\n  No inheritance needed! Just match the method signature.")


# ============================================================
# SUMMARY
# ============================================================

section("SUMMARY: SOLID Principles")

principles = [
    ("SRP", "Single Responsibility", "One class, one reason to change",
     "Split User into User + Validator + Repository + EmailService"),
    ("OCP", "Open/Closed", "Open for extension, closed for modification",
     "Shape ABC + subclasses instead of if/else in calculator"),
    ("LSP", "Liskov Substitution", "Subtypes must be substitutable",
     "Square and Rectangle both implement Shape, not Square extends Rectangle"),
    ("ISP", "Interface Segregation", "Don't depend on unused interfaces",
     "Workable + Eatable + Sleepable instead of one fat Worker interface"),
    ("DIP", "Dependency Inversion", "Depend on abstractions, not concretions",
     "NotificationService depends on NotificationSender ABC, not SMS/Email"),
]

for acronym, name, rule, example in principles:
    print(f"  {acronym}: {name}")
    print(f"    Rule: {rule}")
    print(f"    Fix:  {example}")
    print()

print("Key insight: SOLID principles work TOGETHER.")
print("  OCP needs polymorphism (which needs proper LSP).")
print("  DIP enables OCP (depend on abstractions to extend).")
print("  ISP keeps interfaces small (so DIP is practical).")
print("  SRP ensures each class has focused responsibility.")
