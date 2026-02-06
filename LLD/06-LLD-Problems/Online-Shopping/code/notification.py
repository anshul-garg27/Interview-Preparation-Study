"""Observer Pattern: Order status notifications."""

from abc import ABC, abstractmethod
from enums import OrderStatus


class OrderObserver(ABC):
    """Observer interface for order status changes."""

    @abstractmethod
    def on_status_change(self, order, old_status: OrderStatus,
                         new_status: OrderStatus) -> None:
        pass


class CustomerNotification(OrderObserver):
    """Notifies the customer on every status change."""

    def on_status_change(self, order, old_status, new_status) -> None:
        print(f"      [Notify -> {order.customer.name}] "
              f"Order {order.order_id}: {old_status.value} -> {new_status.value}")


class SellerNotification(OrderObserver):
    """Notifies the seller on key status changes."""

    def on_status_change(self, order, old_status, new_status) -> None:
        if new_status in (OrderStatus.PLACED, OrderStatus.CANCELLED, OrderStatus.RETURNED):
            print(f"      [Notify -> Seller] "
                  f"Order {order.order_id}: {new_status.value}")
