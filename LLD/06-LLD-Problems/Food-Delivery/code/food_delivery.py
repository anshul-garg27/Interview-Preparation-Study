"""
Food Delivery System (Swiggy/DoorDash) - Low Level Design
Run: python food_delivery.py

Patterns: State (order lifecycle), Strategy (delivery assignment),
          Observer (notifications), Factory (payment)
Key: Order state machine, delivery agent matching algorithm
"""
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from enum import Enum
import math
import uuid


# ─── Location ────────────────────────────────────────────────────────
class Location:
    def __init__(self, lat: float, lng: float):
        self.lat = lat
        self.lng = lng

    def distance_to(self, other: "Location") -> float:
        """Simple Euclidean distance (scaled to km-like units)."""
        return math.sqrt((self.lat - other.lat)**2 +
                         (self.lng - other.lng)**2) * 111  # ~km

    def __repr__(self):
        return f"({self.lat:.2f}, {self.lng:.2f})"


# ─── Models ──────────────────────────────────────────────────────────
class MenuItem:
    def __init__(self, name: str, price: float, category: str = "Main"):
        self.id = str(uuid.uuid4())[:6]
        self.name = name
        self.price = price
        self.category = category
        self.available = True


class Restaurant:
    def __init__(self, name: str, location: Location):
        self.id = str(uuid.uuid4())[:6]
        self.name = name
        self.location = location
        self.menu: list[MenuItem] = []
        self.rating = 0.0
        self.total_ratings = 0
        self.is_open = True

    def add_item(self, name: str, price: float, category: str = "Main") -> MenuItem:
        item = MenuItem(name, price, category)
        self.menu.append(item)
        return item

    def update_rating(self, new_rating: float):
        self.rating = ((self.rating * self.total_ratings + new_rating)
                       / (self.total_ratings + 1))
        self.total_ratings += 1


class Customer:
    def __init__(self, name: str, location: Location):
        self.id = str(uuid.uuid4())[:6]
        self.name = name
        self.location = location
        self.orders: list["Order"] = []


class DeliveryAgent:
    def __init__(self, name: str, location: Location):
        self.id = str(uuid.uuid4())[:6]
        self.name = name
        self.location = location
        self.is_available = True
        self.rating = 5.0
        self.total_ratings = 0
        self.current_order: "Order | None" = None

    def accept_order(self, order: "Order"):
        self.is_available = False
        self.current_order = order

    def complete_delivery(self):
        self.is_available = True
        self.current_order = None

    def update_rating(self, new_rating: float):
        self.rating = ((self.rating * self.total_ratings + new_rating)
                       / (self.total_ratings + 1))
        self.total_ratings += 1


# ─── State Pattern: Order States ─────────────────────────────────────
class OrderStatus(Enum):
    PLACED = "Placed"
    PREPARING = "Preparing"
    READY = "Ready for Pickup"
    PICKED_UP = "Picked Up"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"


class OrderState(ABC):
    @abstractmethod
    def get_status(self) -> OrderStatus:
        pass

    @abstractmethod
    def next(self, order: "Order") -> "OrderState":
        pass

    def cancel(self, order: "Order") -> "OrderState":
        raise ValueError(f"Cannot cancel from {self.get_status().value}")


class PlacedState(OrderState):
    def get_status(self): return OrderStatus.PLACED
    def next(self, order): return PreparingState()
    def cancel(self, order): return CancelledState()


class PreparingState(OrderState):
    def get_status(self): return OrderStatus.PREPARING
    def next(self, order): return ReadyState()
    def cancel(self, order): return CancelledState()


class ReadyState(OrderState):
    def get_status(self): return OrderStatus.READY
    def next(self, order): return PickedUpState()


class PickedUpState(OrderState):
    def get_status(self): return OrderStatus.PICKED_UP
    def next(self, order): return DeliveredState()


class DeliveredState(OrderState):
    def get_status(self): return OrderStatus.DELIVERED
    def next(self, order):
        raise ValueError("Order already delivered")


class CancelledState(OrderState):
    def get_status(self): return OrderStatus.CANCELLED
    def next(self, order):
        raise ValueError("Order is cancelled")


class Order:
    def __init__(self, customer: Customer, restaurant: Restaurant,
                 items: list[tuple[MenuItem, int]]):
        self.id = "ORD-" + str(uuid.uuid4())[:6]
        self.customer = customer
        self.restaurant = restaurant
        self.items = items  # [(MenuItem, quantity)]
        self.state: OrderState = PlacedState()
        self.agent: DeliveryAgent | None = None
        self.created_at = datetime.now()
        self.estimated_delivery: datetime | None = None

    @property
    def status(self) -> OrderStatus:
        return self.state.get_status()

    @property
    def total(self) -> float:
        return sum(item.price * qty for item, qty in self.items)

    def advance(self):
        old = self.state.get_status()
        self.state = self.state.next(self)
        return old, self.state.get_status()

    def cancel(self):
        old = self.state.get_status()
        self.state = self.state.cancel(self)
        return old, self.state.get_status()


# ─── Observer: Notifications ─────────────────────────────────────────
class OrderObserver(ABC):
    @abstractmethod
    def on_status_change(self, order: Order, old: OrderStatus,
                         new: OrderStatus):
        pass


class CustomerNotifier(OrderObserver):
    def on_status_change(self, order, old, new):
        msgs = {
            OrderStatus.PREPARING: "Your order is being prepared!",
            OrderStatus.READY: "Food is ready, agent heading to restaurant",
            OrderStatus.PICKED_UP: f"Order picked up! ETA: {order.estimated_delivery.strftime('%H:%M') if order.estimated_delivery else 'TBD'}",
            OrderStatus.DELIVERED: "Order delivered! Please rate your experience",
            OrderStatus.CANCELLED: "Your order has been cancelled",
        }
        msg = msgs.get(new, f"Order status: {new.value}")
        print(f"    [SMS to {order.customer.name}] {msg}")


class RestaurantNotifier(OrderObserver):
    def on_status_change(self, order, old, new):
        if new == OrderStatus.PLACED:
            print(f"    [Alert to {order.restaurant.name}] New order {order.id}!")


# ─── Strategy: Delivery Assignment ───────────────────────────────────
class AssignmentStrategy(ABC):
    @abstractmethod
    def assign(self, order: Order,
               agents: list[DeliveryAgent]) -> DeliveryAgent | None:
        pass


class NearestFirstStrategy(AssignmentStrategy):
    def assign(self, order, agents):
        available = [a for a in agents if a.is_available]
        if not available:
            return None
        return min(available,
                   key=lambda a: a.location.distance_to(order.restaurant.location))


# ─── Service ─────────────────────────────────────────────────────────
class FoodDeliveryService:
    def __init__(self, assignment_strategy: AssignmentStrategy = None):
        self.restaurants: dict[str, Restaurant] = {}
        self.agents: dict[str, DeliveryAgent] = {}
        self.orders: dict[str, Order] = {}
        self.observers: list[OrderObserver] = []
        self.strategy = assignment_strategy or NearestFirstStrategy()

    def add_observer(self, obs: OrderObserver):
        self.observers.append(obs)

    def register_restaurant(self, restaurant: Restaurant):
        self.restaurants[restaurant.id] = restaurant

    def register_agent(self, agent: DeliveryAgent):
        self.agents[agent.id] = agent

    def place_order(self, customer: Customer, restaurant: Restaurant,
                    items: list[tuple[MenuItem, int]]) -> Order:
        if not restaurant.is_open:
            raise ValueError(f"{restaurant.name} is closed")
        order = Order(customer, restaurant, items)
        self.orders[order.id] = order
        customer.orders.append(order)
        self._notify(order, None, OrderStatus.PLACED)
        return order

    def advance_order(self, order_id: str):
        order = self.orders[order_id]
        old, new = order.advance()
        self._notify(order, old, new)

        # Auto-assign agent when food is ready
        if new == OrderStatus.READY:
            self._assign_agent(order)

        # Free agent when delivered
        if new == OrderStatus.DELIVERED and order.agent:
            order.agent.complete_delivery()

    def cancel_order(self, order_id: str):
        order = self.orders[order_id]
        old, new = order.cancel()
        if order.agent:
            order.agent.complete_delivery()
        self._notify(order, old, new)

    def _assign_agent(self, order: Order):
        agent = self.strategy.assign(order, list(self.agents.values()))
        if agent:
            agent.accept_order(order)
            order.agent = agent
            dist = agent.location.distance_to(order.restaurant.location)
            cust_dist = order.restaurant.location.distance_to(order.customer.location)
            total_dist = dist + cust_dist
            eta_minutes = int(total_dist / 0.5) + 10  # 0.5 km/min + 10 min buffer
            order.estimated_delivery = datetime.now() + timedelta(minutes=eta_minutes)
            print(f"    [Assigned] {agent.name} "
                  f"(dist={dist:.1f}km, ETA={eta_minutes}min)")
        else:
            print("    [Warning] No agents available!")

    def _notify(self, order, old, new):
        for obs in self.observers:
            obs.on_status_change(order, old, new)


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    service = FoodDeliveryService()
    service.add_observer(CustomerNotifier())
    service.add_observer(RestaurantNotifier())

    # Setup restaurants
    pizza_place = Restaurant("Mario's Pizza", Location(12.97, 77.59))
    pizza_place.add_item("Margherita", 12.99, "Pizza")
    pizza_place.add_item("Pepperoni", 14.99, "Pizza")
    pizza_place.add_item("Garlic Bread", 5.99, "Sides")
    pizza_place.add_item("Coke", 2.99, "Drinks")
    service.register_restaurant(pizza_place)

    biryani_place = Restaurant("Hyderabad House", Location(12.95, 77.60))
    biryani_place.add_item("Chicken Biryani", 10.99)
    biryani_place.add_item("Raita", 2.99)
    service.register_restaurant(biryani_place)

    # Setup agents
    agents = [
        DeliveryAgent("Ravi", Location(12.96, 77.58)),
        DeliveryAgent("Priya", Location(12.98, 77.61)),
        DeliveryAgent("Amit", Location(13.00, 77.57)),
    ]
    for a in agents:
        service.register_agent(a)

    # Customer
    customer = Customer("Alice", Location(12.99, 77.62))

    # ── Place Order ──
    print("=" * 60)
    print("ORDER LIFECYCLE")
    print("=" * 60)
    items = [(pizza_place.menu[0], 2), (pizza_place.menu[2], 1)]
    order = service.place_order(customer, pizza_place, items)
    print(f"  Order {order.id}: {order.total:.2f} | Status: {order.status.value}")
    for item, qty in order.items:
        print(f"    {qty}x {item.name} @ ${item.price}")

    # Progress through states
    for step in ["Preparing", "Ready (+ assign agent)", "Picked Up", "Delivered"]:
        print(f"\n  --- {step} ---")
        service.advance_order(order.id)
        print(f"  Status: {order.status.value}")

    # ── Ratings ──
    print(f"\n{'=' * 60}")
    print("RATINGS")
    print("=" * 60)
    pizza_place.update_rating(4.5)
    pizza_place.update_rating(4.0)
    pizza_place.update_rating(5.0)
    print(f"  {pizza_place.name}: {pizza_place.rating:.2f} "
          f"({pizza_place.total_ratings} ratings)")

    if order.agent:
        order.agent.update_rating(4.8)
        print(f"  {order.agent.name}: {order.agent.rating:.2f}")

    # ── Cancel Order ──
    print(f"\n{'=' * 60}")
    print("ORDER CANCELLATION")
    print("=" * 60)
    order2 = service.place_order(customer, biryani_place,
                                  [(biryani_place.menu[0], 1)])
    print(f"  Order {order2.id}: {order2.status.value}")
    service.cancel_order(order2.id)
    print(f"  After cancel: {order2.status.value}")

    # ── Invalid Transition ──
    print(f"\n{'=' * 60}")
    print("INVALID STATE TRANSITION")
    print("=" * 60)
    try:
        service.advance_order(order.id)  # already delivered
    except ValueError as e:
        print(f"  Caught: {e}")

    try:
        service.cancel_order(order.id)  # can't cancel delivered
    except ValueError as e:
        print(f"  Caught: {e}")

    # ── Agent Availability ──
    print(f"\n{'=' * 60}")
    print("AGENT STATUS")
    print("=" * 60)
    for a in agents:
        print(f"  {a.name}: {'Available' if a.is_available else 'Busy'} "
              f"| Rating: {a.rating:.1f}")


if __name__ == "__main__":
    main()
