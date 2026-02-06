"""OrderService - manages order lifecycle from checkout to delivery."""

from enums import PaymentMethod, OrderStatus
from order import Order
from payment import PaymentFactory
from notification import CustomerNotification, SellerNotification


class OrderService:
    """Orchestrates checkout, payment, and order status transitions."""

    def __init__(self):
        self.all_orders = []

    def checkout(self, customer, payment_method: PaymentMethod):
        """Validate stock, process payment, create order."""
        if not customer.cart.items:
            print(f"    [Checkout] Cart is empty!")
            return None

        print(f"\n    [Checkout] {customer.name} checking out...")
        customer.cart.display()

        # Validate stock
        for item in customer.cart.items.values():
            if not item.product.is_in_stock(item.quantity):
                print(f"    [Checkout FAILED] '{item.product.name}' insufficient stock")
                return None

        # Process payment
        processor = PaymentFactory.create(payment_method)
        if not processor.process(customer.cart.get_total(), customer.name):
            print(f"    [Checkout FAILED] Payment failed")
            return None

        # Create order
        order_items = list(customer.cart.items.values())
        order = Order(customer, order_items, payment_method)
        order.add_observer(CustomerNotification())
        order.add_observer(SellerNotification())

        # Deduct stock
        for item in order_items:
            item.product.stock -= item.quantity

        customer.order_history.append(order)
        self.all_orders.append(order)
        customer.cart.clear()
        print(f"    [Order Created] {order}")
        return order

    def process_order(self, order: Order) -> None:
        """Simulate order through full delivery lifecycle."""
        print(f"\n    Processing {order.order_id}...")
        for status in [OrderStatus.CONFIRMED, OrderStatus.SHIPPED,
                       OrderStatus.OUT_FOR_DELIVERY, OrderStatus.DELIVERED]:
            order.update_status(status)
