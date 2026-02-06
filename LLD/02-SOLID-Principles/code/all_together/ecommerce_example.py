"""All 5 SOLID Principles Together - E-Commerce Order System.

S - Each class has ONE responsibility
O - Add new payment/notification methods without changing existing code
L - All PaymentProcessors are substitutable
I - Small interfaces: PaymentProcessor, NotificationSender, OrderRepository
D - OrderService depends on abstractions, not concrete implementations
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


# ─── Domain Model (SRP: only holds data) ─────────────────────────

@dataclass
class OrderItem:
    name: str
    price: float
    quantity: int = 1

    @property
    def total(self) -> float:
        return self.price * self.quantity


@dataclass
class Order:
    customer_email: str
    items: List[OrderItem] = field(default_factory=list)
    status: str = "pending"

    @property
    def total(self) -> float:
        return sum(item.total for item in self.items)


# ─── Small Interfaces (ISP: segregated, focused) ─────────────────

class PaymentProcessor(ABC):
    """Interface: process payments."""
    @abstractmethod
    def charge(self, amount: float) -> str:
        pass


class NotificationSender(ABC):
    """Interface: send notifications."""
    @abstractmethod
    def send(self, to: str, message: str) -> str:
        pass


class OrderRepository(ABC):
    """Interface: persist orders."""
    @abstractmethod
    def save(self, order: Order) -> str:
        pass


# ─── Concrete Implementations (OCP: extend by adding new classes) ─

class StripePayment(PaymentProcessor):
    def charge(self, amount: float) -> str:
        return f"Stripe charged ${amount:.2f}"


class PayPalPayment(PaymentProcessor):
    def charge(self, amount: float) -> str:
        return f"PayPal charged ${amount:.2f}"


class EmailNotifier(NotificationSender):
    def send(self, to: str, message: str) -> str:
        return f"Email to {to}: {message}"


class SMSNotifier(NotificationSender):
    def send(self, to: str, message: str) -> str:
        return f"SMS to {to}: {message}"


class InMemoryOrderRepo(OrderRepository):
    def __init__(self):
        self.orders: list[Order] = []

    def save(self, order: Order) -> str:
        self.orders.append(order)
        return f"Order saved (total: {len(self.orders)})"


# ─── High-Level Service (DIP: depends on abstractions) ───────────

class OrderService:
    """Orchestrates order placement.
    - SRP: only coordinates, doesn't do payment/notification/persistence
    - DIP: depends on abstract interfaces, not concrete classes
    - LSP: any PaymentProcessor/NotificationSender works here
    """

    def __init__(
        self,
        payment: PaymentProcessor,
        notifier: NotificationSender,
        repo: OrderRepository,
    ):
        self._payment = payment
        self._notifier = notifier
        self._repo = repo

    def place_order(self, order: Order) -> None:
        print(f"\n  Processing order for {order.customer_email}...")
        print(f"  Items: {[f'{i.name} x{i.quantity}' for i in order.items]}")

        # Charge payment
        result = self._payment.charge(order.total)
        print(f"  {result}")

        # Save order
        order.status = "confirmed"
        save_result = self._repo.save(order)
        print(f"  {save_result}")

        # Notify customer
        msg = f"Order confirmed! Total: ${order.total:.2f}"
        notify_result = self._notifier.send(order.customer_email, msg)
        print(f"  {notify_result}")


if __name__ == "__main__":
    print("=== SOLID E-Commerce Example ===")

    # Setup with Stripe + Email
    service = OrderService(
        payment=StripePayment(),
        notifier=EmailNotifier(),
        repo=InMemoryOrderRepo(),
    )

    order = Order(
        customer_email="alice@example.com",
        items=[OrderItem("Laptop", 999.99), OrderItem("Mouse", 29.99, 2)],
    )
    service.place_order(order)

    # Switch to PayPal + SMS - ZERO changes to OrderService (OCP + DIP)
    print("\n--- Switching to PayPal + SMS ---")
    service2 = OrderService(
        payment=PayPalPayment(),
        notifier=SMSNotifier(),
        repo=InMemoryOrderRepo(),
    )
    order2 = Order(
        customer_email="bob@example.com",
        items=[OrderItem("Keyboard", 79.99)],
    )
    service2.place_order(order2)

    print("\n--- SOLID Principles Applied ---")
    print("  S: OrderService, PaymentProcessor, Notifier - each has one job")
    print("  O: Add CryptoPayment without modifying existing code")
    print("  L: StripePayment and PayPalPayment are interchangeable")
    print("  I: Small interfaces: PaymentProcessor, NotificationSender, OrderRepo")
    print("  D: OrderService depends on abstractions, not Gmail/Stripe directly")
