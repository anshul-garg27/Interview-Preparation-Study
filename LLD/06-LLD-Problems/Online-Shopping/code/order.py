"""Order class with state machine for order lifecycle."""

import threading
from datetime import datetime
from enums import OrderStatus, PaymentMethod


class Order:
    """An order with state-machine based status transitions."""

    _counter = 0
    _lock = threading.Lock()

    TRANSITIONS = {
        OrderStatus.PLACED: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.SHIPPED, OrderStatus.CANCELLED],
        OrderStatus.SHIPPED: [OrderStatus.OUT_FOR_DELIVERY],
        OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED],
        OrderStatus.DELIVERED: [OrderStatus.RETURNED],
        OrderStatus.CANCELLED: [],
        OrderStatus.RETURNED: [],
    }

    def __init__(self, customer, items: list, payment_method: PaymentMethod):
        with Order._lock:
            Order._counter += 1
            self.order_id = f"ORD-{Order._counter:04d}"
        self.customer = customer
        self.items = items
        self.status = OrderStatus.PLACED
        self.payment_method = payment_method
        self.total = sum(i.subtotal for i in items)
        self.created_at = datetime.now()
        self.observers = []
        self.status_history = [(OrderStatus.PLACED, datetime.now())]

    def add_observer(self, observer) -> None:
        self.observers.append(observer)

    def update_status(self, new_status: OrderStatus) -> bool:
        """Transition to a new status if valid."""
        if new_status not in self.TRANSITIONS.get(self.status, []):
            print(f"    [Order Error] Cannot transition "
                  f"{self.status.value} -> {new_status.value}")
            return False
        old_status = self.status
        self.status = new_status
        self.status_history.append((new_status, datetime.now()))
        for obs in self.observers:
            obs.on_status_change(self, old_status, new_status)
        return True

    def display_tracking(self) -> None:
        """Print order tracking timeline."""
        print(f"\n    Order Tracking: {self.order_id}")
        print(f"    {'─'*40}")
        all_statuses = [OrderStatus.PLACED, OrderStatus.CONFIRMED,
                        OrderStatus.SHIPPED, OrderStatus.OUT_FOR_DELIVERY,
                        OrderStatus.DELIVERED]
        reached = {s for s, _ in self.status_history}
        for s in all_statuses:
            marker = "[x]" if s in reached else "[ ]"
            print(f"      {marker} {s.value}")
        if self.status == OrderStatus.CANCELLED:
            print(f"      [!] CANCELLED")
        if self.status == OrderStatus.RETURNED:
            print(f"      [!] RETURNED")

    def __repr__(self) -> str:
        name = self.customer.name if hasattr(self.customer, 'name') else str(self.customer)
        return f"Order({self.order_id}, {name}, ${self.total:.2f}, {self.status.value})"
