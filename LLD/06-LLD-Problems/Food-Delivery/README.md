# Food Delivery System (Swiggy/DoorDash) - Low Level Design

## Problem Statement
Design a food delivery system where customers can browse restaurants, place orders, and get food delivered. The system must handle restaurant management, order lifecycle, delivery agent assignment, real-time tracking, ratings, and payment processing.

---

## Functional Requirements
1. **Restaurant Management** - Register restaurants with menus and prices
2. **Customer Ordering** - Browse, add to cart, place order
3. **Delivery Assignment** - Assign nearest available delivery agent
4. **Order Tracking** - Real-time order status updates (lifecycle)
5. **Estimated Delivery Time** - Calculate based on distance and prep time
6. **Rating System** - Rate restaurants and delivery agents
7. **Payment Processing** - Multiple payment methods

## Non-Functional Requirements
- Real-time order status updates
- Fair delivery agent assignment
- Handle concurrent orders
- Accurate ETA calculation

---

## Design Patterns Used

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **State** | Order lifecycle (Placed → Preparing → PickedUp → Delivered) | Clean state transitions with validation |
| **Strategy** | Delivery assignment algorithm, pricing strategy | Swap algorithms without changing core logic |
| **Observer** | Order status notifications to customer, restaurant, agent | Decouple notification from state changes |
| **Factory** | Payment method creation | Encapsulate payment object creation |

### State Pattern -- Order Lifecycle
The order progresses through well-defined states. Each state knows which transitions are valid and what actions to perform on entry/exit. This prevents invalid transitions like "Delivered → Placed".

### Strategy -- Delivery Assignment
Different algorithms for matching delivery agents:
- **Nearest First**: Assign closest available agent
- **Load Balanced**: Assign agent with fewest active orders
- **Rating Based**: Prefer highest-rated agents

---

## Class Diagram

```mermaid
classDiagram
    class User {
        -String id
        -String name
        -String phone
        -Address address
    }

    class Customer {
        -List~Order~ order_history
        +place_order(restaurant, items) Order
        +rate_order(order, rating)
    }

    class Restaurant {
        -String id
        -String name
        -Address address
        -Menu menu
        -float rating
        -int total_ratings
        -bool is_open
        +add_menu_item(item)
        +update_rating(new_rating)
        +get_menu() Menu
    }

    class MenuItem {
        -String id
        -String name
        -float price
        -String category
        -bool available
    }

    class Menu {
        -List~MenuItem~ items
        +get_items_by_category(cat) List
        +get_item(id) MenuItem
    }

    class DeliveryAgent {
        -String id
        -String name
        -Location current_location
        -bool is_available
        -float rating
        -Order current_order
        +accept_order(order)
        +update_location(location)
        +mark_available()
    }

    class Order {
        -String id
        -Customer customer
        -Restaurant restaurant
        -List~OrderItem~ items
        -float total_amount
        -OrderState state
        -DeliveryAgent agent
        -datetime created_at
        -datetime estimated_delivery
        +get_total() float
        +transition_to(state)
    }

    class OrderState {
        <<interface>>
        +handle(order)
        +next(order)
        +cancel(order)
        +get_status() String
    }

    class PlacedState {
        +handle(order)
        +next(order)
    }

    class PreparingState {
        +handle(order)
        +next(order)
    }

    class ReadyState {
        +handle(order)
        +next(order)
    }

    class PickedUpState {
        +handle(order)
        +next(order)
    }

    class DeliveredState {
        +handle(order)
    }

    class CancelledState {
        +handle(order)
    }

    class DeliveryAssignmentStrategy {
        <<interface>>
        +assign(order, agents) DeliveryAgent
    }

    class NearestFirstStrategy {
        +assign(order, agents) DeliveryAgent
    }

    class OrderObserver {
        <<interface>>
        +on_status_change(order, old, new)
    }

    class CustomerNotifier {
        +on_status_change(order, old, new)
    }

    class RestaurantNotifier {
        +on_status_change(order, old, new)
    }

    class FoodDeliveryService {
        -Map~String, Restaurant~ restaurants
        -Map~String, DeliveryAgent~ agents
        -Map~String, Order~ orders
        -DeliveryAssignmentStrategy assignment_strategy
        -List~OrderObserver~ observers
        +register_restaurant(restaurant)
        +place_order(customer, restaurant_id, items) Order
        +update_order_status(order_id)
        +assign_delivery(order_id)
        +rate_restaurant(restaurant_id, rating)
        +rate_agent(agent_id, rating)
    }

    User <|-- Customer
    User <|-- DeliveryAgent
    OrderState <|.. PlacedState
    OrderState <|.. PreparingState
    OrderState <|.. ReadyState
    OrderState <|.. PickedUpState
    OrderState <|.. DeliveredState
    OrderState <|.. CancelledState
    DeliveryAssignmentStrategy <|.. NearestFirstStrategy
    OrderObserver <|.. CustomerNotifier
    OrderObserver <|.. RestaurantNotifier
    Restaurant --> Menu
    Menu --> MenuItem
    Order --> OrderState
    Order --> Customer
    Order --> Restaurant
    Order --> DeliveryAgent
    FoodDeliveryService --> Restaurant
    FoodDeliveryService --> DeliveryAgent
    FoodDeliveryService --> Order
    FoodDeliveryService --> DeliveryAssignmentStrategy
    FoodDeliveryService --> OrderObserver
```

---

## Sequence Diagram - Placing an Order

```mermaid
sequenceDiagram
    participant C as Customer
    participant S as FoodDeliveryService
    participant R as Restaurant
    participant O as Order
    participant DA as DeliveryAssignment
    participant A as DeliveryAgent
    participant N as Observer/Notifier

    C->>S: place_order(restaurant_id, items)
    S->>R: validate items available
    R-->>S: items validated
    S->>O: create Order(customer, restaurant, items)
    O->>O: set state = PlacedState
    S->>N: notify(order, PLACED)
    N-->>R: "New order received!"
    S-->>C: Order created (id=ORD-123)

    Note over S: Restaurant starts preparing
    S->>O: next() → PreparingState
    S->>N: notify(order, PREPARING)
    N-->>C: "Your order is being prepared"

    Note over S: Food ready
    S->>O: next() → ReadyState
    S->>DA: assign(order, available_agents)
    DA->>DA: Find nearest available agent
    DA-->>S: Agent found
    S->>A: accept_order(order)
    A-->>S: accepted
    S->>N: notify(order, READY)
    N-->>C: "Agent on the way to restaurant"

    S->>O: next() → PickedUpState
    N-->>C: "Order picked up! ETA: 15 min"

    S->>O: next() → DeliveredState
    S->>A: mark_available()
    N-->>C: "Order delivered! Please rate"
```

## Sequence Diagram - Order State Machine

```mermaid
stateDiagram-v2
    [*] --> Placed
    Placed --> Preparing : restaurant accepts
    Placed --> Cancelled : customer cancels
    Preparing --> Ready : food prepared
    Preparing --> Cancelled : restaurant cancels
    Ready --> PickedUp : agent picks up
    PickedUp --> Delivered : agent delivers
    Delivered --> [*]
    Cancelled --> [*]
```

---

## Edge Cases
1. **No available agents** - Queue the order, retry with backoff
2. **Agent cancels after accepting** - Reassign to next nearest agent
3. **Restaurant is closed** - Reject order at placement time
4. **Item out of stock** - Reject order or suggest alternatives
5. **Payment failure** - Retry or cancel order
6. **Delivery address unreachable** - Contact customer, timeout policy
7. **Concurrent orders to same restaurant** - Queue if restaurant is at capacity
8. **Agent location update failure** - Use last known location, mark stale

## Extensions
- Surge pricing during peak hours
- Scheduled orders (order for later)
- Promo codes and discounts
- Split payment between customers
- Restaurant search with filters (cuisine, rating, distance)
- Live order tracking on map
- Chat between customer and delivery agent
- Subscription plans (free delivery)

---

## Interview Tips

1. **Lead with the State pattern** - Draw the state machine diagram first
2. **Discuss delivery assignment** - Show the Strategy pattern with distance calculation
3. **Observer for notifications** - Clean decoupling between order changes and notifications
4. **Mention ETA calculation** - Prep time + travel distance / speed
5. **Rating with weighted average** - `new_avg = (old_avg * count + new_rating) / (count + 1)`
6. **Common follow-up**: "How to handle peak load?" - Queue orders, rate limit, async processing
7. **Common follow-up**: "How to optimize delivery?" - Batching nearby orders for same agent
