# One-Page LLD Problems Revision

> 15 LLD problems summarized — key classes, patterns, tricky parts.

---

## Problem 1: Parking Lot

**Key Classes:** `ParkingLot`, `ParkingFloor`, `ParkingSpot`, `Vehicle`, `Ticket`, `PaymentProcessor`

**Patterns:** Strategy (pricing), Factory (vehicle/spot), Observer (availability), Singleton (ParkingLot)

**Tricky Parts:**
- Multiple spot types (compact, large, handicapped) — use enum + Factory
- Pricing strategies (hourly, flat, dynamic) — use Strategy
- Concurrency on spot assignment — use locking
- Finding nearest available spot — use Strategy for allocation

**Core Design:**
```python
class ParkingLot:          # Singleton, has floors
class ParkingSpot:         # has vehicle, spot_type
class Vehicle(ABC):        # Car, Truck, Motorcycle subclasses
class PricingStrategy(ABC): # HourlyPricing, FlatPricing
```

---

## Problem 2: Elevator System

**Key Classes:** `ElevatorSystem`, `Elevator`, `Floor`, `Request`, `Dispatcher`, `Door`

**Patterns:** State (elevator states), Strategy (dispatching), Observer (floor requests), Command (requests)

**Tricky Parts:**
- Elevator state machine: Idle -> Moving Up/Down -> Stopped -> Door Open
- Dispatching algorithm: nearest elevator, SCAN, LOOK
- Multiple elevators coordination
- Direction optimization

**Core Design:**
```python
class Elevator:            # has state, current_floor, direction
class ElevatorState(ABC):  # Idle, MovingUp, MovingDown, DoorOpen
class Dispatcher:          # Strategy for selecting best elevator
class Request:             # floor, direction, type (internal/external)
```

---

## Problem 3: LRU Cache

**Key Classes:** `LRUCache`, `Node`, `DoublyLinkedList`

**Patterns:** Strategy (eviction policy), Proxy (cache layer)

**Tricky Parts:**
- O(1) get and put — requires HashMap + Doubly Linked List
- Eviction — remove least recently used (tail of list)
- Thread safety — lock around get/put
- Capacity management

**Core Design:**
```python
class LRUCache:
    def __init__(self, capacity):
        self.cache = {}               # key -> Node
        self.dll = DoublyLinkedList()  # MRU at head, LRU at tail
    def get(self, key):    # Move to head, return value
    def put(self, key, v): # Add to head, evict tail if full
```

---

## Problem 4: Chess

**Key Classes:** `Game`, `Board`, `Piece`, `Player`, `Move`, `Square`

**Patterns:** Factory (piece creation), Strategy (move validation), Command (moves for undo), Observer (check detection)

**Tricky Parts:**
- Each piece type has unique movement rules — Strategy or polymorphism
- Check, checkmate, stalemate detection
- Special moves: castling, en passant, pawn promotion
- Move validation: can't move into check

**Core Design:**
```python
class Piece(ABC):          # has color, position; abstract move_rules()
class King(Piece): ...     # Each piece overrides move validation
class Board:               # 8x8 grid of Square, validates moves
class Game:                # Manages turns, checks game-over conditions
```

---

## Problem 5: BookMyShow (Movie Ticket Booking)

**Key Classes:** `Theater`, `Screen`, `Show`, `Seat`, `Booking`, `Movie`, `Payment`, `User`

**Patterns:** Observer (seat availability), Strategy (pricing), Factory (seat types), Singleton (BookingSystem)

**Tricky Parts:**
- Seat locking during booking — temporary hold with timeout
- Concurrent seat selection — optimistic locking or DB locks
- Pricing by seat type, time, demand
- Search and filter movies by city, genre, language

**Core Design:**
```python
class Theater:     # has screens, location
class Show:        # has movie, screen, time, available_seats
class Booking:     # has user, show, seats, payment_status
class Seat:        # has row, number, type, price
```

---

## Problem 6: Library Management

**Key Classes:** `Library`, `Book`, `BookItem`, `Member`, `Librarian`, `Loan`, `Fine`, `Reservation`

**Patterns:** Observer (book available notification), Strategy (fine calculation), Factory (member types)

**Tricky Parts:**
- Book vs BookItem (catalog entry vs physical copy)
- Reservation queue when book unavailable
- Fine calculation based on overdue days
- Renewal limits and policies

**Core Design:**
```python
class Book:        # ISBN, title, author (catalog)
class BookItem:    # physical copy, barcode, status
class Loan:        # member, book_item, due_date
class Member:      # has active loans, reservations
```

---

## Problem 7: Vending Machine

**Key Classes:** `VendingMachine`, `Product`, `Inventory`, `Coin`, `State`

**Patterns:** State (machine states), Strategy (payment), Factory (products)

**Tricky Parts:**
- State machine: Idle -> HasMoney -> Dispensing -> ReturnChange
- Change calculation — greedy algorithm
- Inventory management
- Handling insufficient funds / out of stock

**Core Design:**
```python
class VendingMachine:      # has state, balance, inventory
class State(ABC):          # IdleState, HasMoneyState, DispensingState
class Product:             # name, price, code
class Inventory:           # product -> count mapping
```

---

## Problem 8: Cab Booking (Uber/Ola)

**Key Classes:** `RideService`, `Rider`, `Driver`, `Ride`, `Location`, `Payment`, `Rating`

**Patterns:** Strategy (pricing, matching), Observer (ride status), State (ride lifecycle), Factory (ride types)

**Tricky Parts:**
- Driver matching — nearest available, rating-based
- Surge pricing — Strategy pattern
- Ride state machine: Requested -> Matched -> InProgress -> Completed
- Real-time location tracking
- Concurrent ride requests

**Core Design:**
```python
class Ride:                # rider, driver, pickup, dropoff, status
class RideState(ABC):      # Requested, Matched, InProgress, Completed
class PricingStrategy(ABC): # BasePricing, SurgePricing
class DriverMatcher:       # Strategy for matching drivers to riders
```

---

## Problem 9: Snake and Ladder

**Key Classes:** `Game`, `Board`, `Player`, `Dice`, `Snake`, `Ladder`, `Cell`

**Patterns:** Strategy (dice), Factory (board elements), State (game state)

**Tricky Parts:**
- Board generation with random snakes/ladders (no overlap, no cycles)
- Multiple players, turn management
- Win condition: reach or exceed cell 100
- Snake head > tail; Ladder bottom < top

**Core Design:**
```python
class Board:       # cells with optional snake/ladder
class Game:        # players, board, current_turn, is_over
class Dice:        # roll() -> 1-6
class Snake:       # head position, tail position
class Ladder:      # bottom position, top position
```

---

## Problem 10: Online Shopping (Amazon)

**Key Classes:** `Product`, `Cart`, `Order`, `User`, `Payment`, `Catalog`, `Review`, `Address`, `Shipment`

**Patterns:** Strategy (payment, shipping), Observer (order status), Decorator (product variants), Factory (payment)

**Tricky Parts:**
- Cart management with inventory checks
- Payment processing with multiple methods
- Order lifecycle: Placed -> Confirmed -> Shipped -> Delivered
- Search and filter products — Strategy for sorting/filtering
- Discount/coupon system — Decorator or Strategy

**Core Design:**
```python
class Cart:        # has items, calculates total
class Order:       # has items, status, payment, shipping_address
class Product:     # name, price, category, inventory
class Catalog:     # search, filter products
```

---

## Problem 11: ATM Machine

**Key Classes:** `ATM`, `Account`, `Card`, `Transaction`, `CashDispenser`, `Screen`

**Patterns:** State (ATM states), Chain of Responsibility (cash dispensing), Strategy (transaction types)

**Tricky Parts:**
- State machine: Idle -> CardInserted -> Authenticated -> TransactionSelected -> Processing
- Cash dispensing: give fewest bills (Chain of Responsibility: 500 -> 200 -> 100)
- Daily withdrawal limit, insufficient funds handling
- Card retention after 3 failed attempts

---

## Problem 12: Hotel Booking

**Key Classes:** `Hotel`, `Room`, `Reservation`, `Guest`, `Payment`, `RoomType`

**Patterns:** Strategy (pricing), Observer (availability), Factory (room types)

**Tricky Parts:**
- Date-range based availability (not just boolean)
- Overbooking policies
- Cancellation and refund rules
- Room type matching and upgrades

---

## Problem 13: Tic-Tac-Toe

**Key Classes:** `Game`, `Board`, `Player`, `Cell`, `Move`

**Patterns:** Strategy (player strategy: human vs AI), Factory (player types)

**Tricky Parts:**
- Win detection: rows, columns, diagonals — O(1) possible with row/col sums
- Draw detection
- Extensible to N x N board
- AI player: minimax algorithm

---

## Problem 14: File System

**Key Classes:** `FileSystem`, `File`, `Directory`, `Path`

**Patterns:** Composite (file/directory tree), Iterator (traversal), Visitor (operations)

**Tricky Parts:**
- Recursive directory structure — Composite pattern
- Path resolution (absolute vs relative)
- Permissions and access control
- Search across directory tree

---

## Problem 15: Social Media Feed (Twitter/Instagram)

**Key Classes:** `User`, `Post`, `Feed`, `Comment`, `Like`, `Follow`, `Notification`

**Patterns:** Observer (follow/notify), Strategy (feed ranking), Decorator (post types), Iterator (feed pagination)

**Tricky Parts:**
- Feed generation: pull vs push model
- Feed ranking algorithm — chronological vs engagement-based
- Infinite scroll / pagination
- Privacy settings affecting visibility

---

## Pattern Frequency Across Problems

| Pattern           | Count | Problems                                          |
|-------------------|-------|---------------------------------------------------|
| Strategy          | 15/15 | Every problem uses it somewhere                   |
| Factory           | 12/15 | Object creation in most problems                  |
| Observer          | 11/15 | Notifications and event handling                  |
| State             | 8/15  | Elevator, Vending, Cab, ATM, Booking systems      |
| Command           | 4/15  | Chess, Elevator, Text Editor                      |
| Decorator         | 3/15  | Shopping, Coffee pricing, Feed                    |
| Composite         | 2/15  | File System, Menu systems                         |
| Singleton         | 4/15  | Parking Lot, Booking System, Cache                |
| Chain of Resp.    | 2/15  | ATM cash dispensing, middleware                   |

---

*One-page revision | 2026-02-06*
