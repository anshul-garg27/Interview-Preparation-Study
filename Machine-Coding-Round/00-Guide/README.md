# Complete Guide to Machine Coding Rounds

## Table of Contents
1. [What is a Machine Coding Round?](#what-is-a-machine-coding-round)
2. [How It Differs from LLD and DSA](#how-it-differs-from-lld-and-dsa)
3. [Companies That Use It](#companies-that-use-it)
4. [Format Breakdown](#format-breakdown)
5. [What Interviewers Evaluate](#what-interviewers-evaluate)
6. [The 90-Minute Framework](#the-90-minute-framework)
7. [Golden Rules](#golden-rules)
8. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
9. [Template: How to Structure ANY Solution](#template-how-to-structure-any-solution)
10. [10 Machine Coding Topics You MUST Know](#10-machine-coding-topics-you-must-know)
11. [Language-Specific Tips](#language-specific-tips)
12. [Real Interview Examples](#real-interview-examples)
13. [Pre-Round Checklist](#pre-round-checklist)
14. [Post-Round: How to Demo](#post-round-how-to-demo)

---

## What is a Machine Coding Round?

### Definition
A Machine Coding Round is a **timed coding exercise** (typically 90-120 minutes) where you are
given a **real-world problem statement** and expected to write **fully functional, executable code**
that implements a mini-system from scratch.

Unlike whiteboard interviews or take-home assignments, this round happens **live** (in-person or
on a shared screen), and the output must be a **running program** that handles the given
requirements and produces correct output.

### The Core Expectation
```
Input:  A problem statement (1-2 pages) with requirements and sample I/O
Output: A RUNNABLE codebase with clean OOP, proper structure, and working demo
Time:   90-120 minutes (varies by company)
```

### What "Working Code" Means
- The code **compiles/runs without errors**
- A main/driver function demonstrates all features
- Sample inputs produce expected outputs
- Edge cases are handled gracefully (not crashes)
- Code is organized into multiple classes/files

### Key Characteristics
| Aspect | Machine Coding Round |
|--------|---------------------|
| Time | 90-120 minutes |
| Output | Fully executable code |
| Storage | In-memory (HashMaps, Lists) |
| UI | Console I/O or method calls |
| Testing | Demo with sample inputs |
| Language | Your choice (Java/Python/C++) |
| IDE | Your own laptop or online IDE |
| Internet | Usually allowed (no copy-paste of solutions) |

---

## How It Differs from LLD and DSA

### Machine Coding vs Low-Level Design (LLD)

| Aspect | LLD Interview | Machine Coding |
|--------|--------------|----------------|
| **Focus** | Design & architecture | Working implementation |
| **Output** | Class diagrams, API design | Executable code |
| **Depth** | Broad system design | Deep implementation of subset |
| **Code** | Skeleton/pseudocode OK | Must compile and run |
| **Time** | 45-60 minutes | 90-120 minutes |
| **Evaluation** | Design quality | Code quality + correctness |
| **Storage** | Can discuss DB schemas | Must use in-memory storage |

**Key Insight**: In LLD, saying "I'll use the Observer pattern here" is sufficient.
In Machine Coding, you must **implement** the Observer pattern with working code.

### Machine Coding vs DSA

| Aspect | DSA Round | Machine Coding |
|--------|-----------|----------------|
| **Focus** | Algorithm efficiency | System implementation |
| **Problem size** | Single function/algorithm | Multiple classes working together |
| **Evaluation** | Time/space complexity | OOP, modularity, extensibility |
| **Patterns** | Two pointers, DP, graphs | Strategy, Factory, Observer |
| **Input** | Well-defined, small | Multiple commands, real-world |
| **Error handling** | Usually not needed | Critical |

**Key Insight**: DSA asks "Can you solve this efficiently?" Machine Coding asks
"Can you build a system that works, is clean, and can grow?"

### The Spectrum
```
DSA ──────────── Machine Coding ──────────── System Design
(Algorithm)      (Implementation)              (Architecture)
Single function  Multiple classes              Multiple services
O(n) analysis    OOP + Patterns                Scalability
30-45 min        90-120 min                    45-60 min
```

---

## Companies That Use It

### Tier 1 (Machine Coding is a MUST)
| Company | Format | Time | Notes |
|---------|--------|------|-------|
| **Flipkart** | On-laptop, in-office | 90 min | Most famous for this round |
| **Uber** | On-laptop | 90-120 min | Focus on extensibility |
| **Swiggy** | On-laptop | 90 min | Real-world delivery problems |
| **Cred** | On-laptop | 90 min | Clean code emphasis |
| **Razorpay** | On-laptop | 90-120 min | Payment-related problems |
| **PhonePe** | On-laptop | 90 min | Similar to Flipkart style |

### Tier 2 (Frequently Used)
| Company | Format | Time | Notes |
|---------|--------|------|-------|
| **Gojek** | On-laptop | 120 min | Very thorough evaluation |
| **Udaan** | On-laptop | 90 min | Supply chain problems |
| **Groww** | On-laptop | 90 min | Trading/finance problems |
| **BrowserStack** | On-laptop | 90 min | Testing-related problems |
| **Atlassian** | On-laptop | 90-120 min | Collaboration tool problems |
| **Tekion** | On-laptop | 90 min | Automotive domain |

### Tier 3 (Sometimes Used)
| Company | Notes |
|---------|-------|
| **Google** | Occasionally for certain roles |
| **Amazon** | Bar raiser rounds sometimes include this |
| **Microsoft** | Some teams use machine coding |
| **Intuit** | For senior engineer roles |
| **Walmart** | Backend engineering roles |

---

## Format Breakdown

### Flipkart-Style Format (Most Common)

```
Total Time: ~120 minutes

Phase 1: Pre-Coding (15 minutes)
├── Read the problem statement carefully
├── Ask clarifying questions to the interviewer
├── Identify entities, relationships, and key operations
├── Sketch class diagram on paper/whiteboard
└── Decide on design patterns to use

Phase 2: Coding (90 minutes)
├── 0-5 min:   Set up project structure, create files
├── 5-15 min:  Write enums, constants, data models
├── 15-40 min: Implement core business logic (Service layer)
├── 40-60 min: Implement remaining features
├── 60-75 min: Add input parsing / demo flow
├── 75-85 min: Test with sample inputs
└── 85-90 min: Fix bugs, clean up code

Phase 3: Post-Coding (15 minutes)
├── Run the demo for the interviewer
├── Walk through your design decisions
├── Discuss what you would add with more time
├── Answer questions about extensibility
└── Discuss trade-offs you made
```

### Uber-Style Format
```
- Receive problem via email/doc 30 minutes before
- 90 minutes to code (screen shared or on-site)
- 15 minutes for code review and discussion
- Emphasis: Can you extend this design with new features?
```

### Cred/Gojek-Style Format
```
- Receive problem at the start of the round
- 120 minutes to code (more generous timing)
- Detailed code review session afterward
- Emphasis: Code cleanliness, naming, separation of concerns
```

### Online/Remote Format
```
- Problem shared via HackerEarth, CoderPad, or Google Doc
- Screen share on Zoom/Google Meet
- Interviewer observes but doesn't interrupt
- Post-coding: Walk through the code
```

---

## What Interviewers Evaluate

### Scoring Rubric (Typical Breakdown)

```
Total: 100 points

1. Executable Code          [30 points]
   ├── Does it compile/run?           (10)
   ├── Does it produce correct output? (10)
   └── Does the demo work end-to-end?  (10)

2. Clean & Modular Code     [25 points]
   ├── Proper OOP (classes, encapsulation)  (8)
   ├── Single Responsibility Principle      (5)
   ├── Meaningful naming                     (4)
   ├── Separation of concerns               (4)
   └── No code duplication                   (4)

3. Extensibility            [15 points]
   ├── Can add new features without rewriting? (5)
   ├── Open/Closed Principle followed?          (5)
   └── Interfaces/abstractions used properly?   (5)

4. Edge Case Handling       [15 points]
   ├── Null/empty input handling        (5)
   ├── Boundary conditions              (5)
   └── Meaningful error messages        (5)

5. Design Patterns          [10 points]
   ├── Appropriate pattern usage        (5)
   └── Not over-engineered              (5)

6. Bonus: Concurrency       [5 points]
   ├── Thread safety where needed       (3)
   └── Proper synchronization           (2)
```

### What Gets You REJECTED
- Code doesn't run / compile errors
- Single God class with everything
- No separation of data and logic
- Hardcoded values everywhere (no enums)
- No error handling at all
- Spending 90 minutes on design, no code

### What Gets You SELECTED
- Clean, running code that handles all requirements
- Well-structured with multiple classes
- Easy to explain and extend
- Good naming conventions
- Handles edge cases gracefully
- Clear demo with formatted output

### Evaluation Red Flags vs Green Flags

```
RED FLAGS                              GREEN FLAGS
--------------------                   --------------------
Everything in main()                   Separate classes per entity
if/else chains for types               Enums + Strategy pattern
System.out.println everywhere          Dedicated output formatter
new ConcreteClass() in logic           Factory pattern / DI
Global mutable state                   Encapsulated state in objects
No input validation                    Graceful error messages
Magic numbers/strings                  Named constants / enums
Copy-pasted code blocks                Shared utility methods
Comments explaining obvious code       Self-documenting names
Unused code left in                    Clean, minimal code
```

---

## The 90-Minute Framework

### Minute-by-Minute Breakdown

```
PHASE 1: UNDERSTAND (0-10 min)
┌─────────────────────────────────────────────┐
│ Read the problem statement TWICE             │
│ Underline key requirements                   │
│ List entities (nouns = classes)               │
│ List operations (verbs = methods)             │
│ Ask clarifying questions:                     │
│   - "Should I handle concurrent access?"      │
│   - "Is there a priority for this feature?"   │
│   - "What's the expected output format?"      │
└─────────────────────────────────────────────┘

PHASE 2: PLAN (10-15 min)
┌─────────────────────────────────────────────┐
│ Draw quick class diagram (paper/whiteboard)  │
│ Identify which design patterns to use        │
│ List your files/classes:                      │
│   enums.py, models/, services/, main.py      │
│ Decide on data structures:                    │
│   HashMap for lookups, List for ordered data  │
│ Prioritize features: Must-have vs Nice-to-have│
└─────────────────────────────────────────────┘

PHASE 3: BUILD FOUNDATION (15-25 min)
┌─────────────────────────────────────────────┐
│ Create file structure                         │
│ Write all enums (Status, Type, Priority)      │
│ Write data model classes:                     │
│   - Fields + constructor                      │
│   - Getters (keep it simple)                  │
│   - __str__ / toString for display            │
│ Create empty service classes with method stubs│
└─────────────────────────────────────────────┘

PHASE 4: CORE LOGIC (25-55 min)  ← MOST TIME HERE
┌─────────────────────────────────────────────┐
│ Implement the PRIMARY service                 │
│ This is usually 1-2 core operations:          │
│   - "Book a room" / "Place an order"          │
│   - "Transfer money" / "Schedule a job"       │
│ Write in-memory repository/storage            │
│ Add validation logic                          │
│ Test mentally as you write                    │
└─────────────────────────────────────────────┘

PHASE 5: REMAINING FEATURES (55-70 min)
┌─────────────────────────────────────────────┐
│ Implement secondary features:                 │
│   - Search/filter                             │
│   - Cancel/update                             │
│   - History/reports                           │
│ Add edge case handling                        │
│ If running low on time:                       │
│   - Skip nice-to-have features               │
│   - Focus on making core features bulletproof │
└─────────────────────────────────────────────┘

PHASE 6: DEMO & POLISH (70-85 min)
┌─────────────────────────────────────────────┐
│ Write main/demo function                      │
│ Add sample data creation                      │
│ Call each feature with sample inputs          │
│ Add print statements showing results          │
│ Format output clearly (headers, separators)   │
└─────────────────────────────────────────────┘

PHASE 7: TEST & FIX (85-90 min)
┌─────────────────────────────────────────────┐
│ Run the code!                                 │
│ Fix compilation/runtime errors                │
│ Verify output matches expected                │
│ Quick scan for obvious issues                 │
│ DO NOT refactor at this stage                 │
└─────────────────────────────────────────────┘
```

### Time Allocation Pie Chart (Mental Model)
```
Core Logic:     33%  (30 min) ← Spend most time here
Remaining:      17%  (15 min)
Foundation:     11%  (10 min)
Demo/Output:    17%  (15 min)
Understand:     11%  (10 min)
Plan:            6%  (5 min)
Test/Fix:        6%  (5 min)
```

### Time Management Tips
1. **Set a timer** for each phase
2. If stuck on a feature for > 10 minutes, skip and come back
3. Core logic should be working by minute 55
4. Demo should be running by minute 75
5. Never spend more than 5 minutes debugging one issue
6. If the code doesn't run by minute 80, drop features to make it work

---

## Golden Rules

### Rule 1: ALWAYS Make It Executable
```
Partial working code  >  Complete non-working code

A program that handles 3 out of 5 features correctly
is ALWAYS better than one that handles 5 features
but doesn't compile.
```

### Rule 2: Use In-Memory Storage
```python
# DO THIS: Simple in-memory storage
class UserRepository:
    def __init__(self):
        self._users = {}  # id -> User

    def save(self, user):
        self._users[user.id] = user

    def find_by_id(self, user_id):
        return self._users.get(user_id)

    def find_all(self):
        return list(self._users.values())

# DON'T DO: No databases, no files, no external storage
# cursor.execute("INSERT INTO users ...")  # NEVER
```

### Rule 3: One Class = One Responsibility
```
BAD:  BookingSystem class that has User management + Room management + Booking logic
GOOD: UserService, RoomService, BookingService (each handles one thing)
```

### Rule 4: Write Enums for All Constants
```python
# BAD
status = "ACTIVE"      # Magic string
room_type = 1          # Magic number

# GOOD
class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class RoomType(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
```

### Rule 5: Use Strategy Pattern for Interchangeable Logic
```python
# When the problem says "different types" or "multiple algorithms"
# Use Strategy pattern

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, base_amount):
        pass

class FlatPricing(PricingStrategy):
    def calculate(self, base_amount):
        return base_amount

class PercentagePricing(PricingStrategy):
    def __init__(self, percentage):
        self.percentage = percentage

    def calculate(self, base_amount):
        return base_amount * self.percentage / 100
```

### Rule 6: Use Factory for Object Creation
```python
# When you need to create different types of objects
class NotificationFactory:
    @staticmethod
    def create(notification_type, message):
        if notification_type == NotificationType.EMAIL:
            return EmailNotification(message)
        elif notification_type == NotificationType.SMS:
            return SMSNotification(message)
        elif notification_type == NotificationType.PUSH:
            return PushNotification(message)
        raise ValueError(f"Unknown type: {notification_type}")
```

### Rule 7: Handle Invalid Inputs Gracefully
```python
# DON'T let the program crash
def book_room(self, room_id, user_id, start_time, end_time):
    room = self._room_repo.find_by_id(room_id)
    if not room:
        print(f"Error: Room {room_id} not found")
        return None

    if start_time >= end_time:
        print("Error: Start time must be before end time")
        return None

    if not room.is_available(start_time, end_time):
        print(f"Error: Room {room_id} is not available for the requested time")
        return None

    # Proceed with booking...
```

### Rule 8: Print Clear, Formatted Output
```python
# BAD
print(booking)

# GOOD
print("=" * 60)
print("        BOOKING CONFIRMATION")
print("=" * 60)
print(f"  Booking ID  : {booking.id}")
print(f"  Room        : {booking.room.name}")
print(f"  Organizer   : {booking.organizer.name}")
print(f"  Time        : {booking.start_time} - {booking.end_time}")
print(f"  Status      : {booking.status.value}")
print("=" * 60)
```

### Rule 9: Start With Core Features
```
Priority order:
1. MUST HAVE: Core create/read operations (these MUST work)
2. SHOULD HAVE: Update/delete, search/filter
3. NICE TO HAVE: Reports, analytics, notifications
4. BONUS: Concurrency, undo/redo

If time is short, cut from the bottom up.
```

### Rule 10: Always Have a Demo Function
```python
def main():
    # 1. Setup
    print("=== Setting up the system ===")
    service = BookingService()

    # 2. Create test data
    print("\n=== Creating test data ===")
    service.add_room("R1", "Conference Room A", 10)
    service.add_room("R2", "Conference Room B", 20)

    # 3. Demonstrate each feature
    print("\n=== Feature 1: Book a room ===")
    booking = service.book("R1", "Alice", "10:00", "11:00")

    print("\n=== Feature 2: Search available rooms ===")
    available = service.search_available("10:00", "11:00", min_capacity=5)

    print("\n=== Feature 3: Cancel a booking ===")
    service.cancel(booking.id)

    # 4. Show final state
    print("\n=== Final State ===")
    service.show_all_bookings()

if __name__ == "__main__":
    main()
```

---

## Common Mistakes to Avoid

### Mistake 1: Starting to Code Without Understanding Requirements
```
WRONG: Read problem → Start coding immediately
RIGHT: Read problem → Read again → List entities → Ask questions → THEN code

Spending 10 minutes planning saves 30 minutes of rework.
```

### Mistake 2: The God Class
```python
# WRONG: Everything in one class
class BookingSystem:
    def add_user(self): ...
    def remove_user(self): ...
    def add_room(self): ...
    def remove_room(self): ...
    def book_room(self): ...
    def cancel_booking(self): ...
    def search_rooms(self): ...
    def generate_report(self): ...
    def send_notification(self): ...
    # 500 lines of chaos

# RIGHT: Separate services
class UserService: ...      # User management
class RoomService: ...      # Room management
class BookingService: ...   # Booking logic
class SearchService: ...    # Search/filter
class ReportService: ...    # Reporting
```

### Mistake 3: No Error Handling
```python
# WRONG: Crash on bad input
def get_user(self, user_id):
    return self._users[user_id]  # KeyError if not found!

# RIGHT: Handle gracefully
def get_user(self, user_id):
    user = self._users.get(user_id)
    if not user:
        raise ValueError(f"User with ID '{user_id}' not found")
    return user
```

### Mistake 4: Using Primitives Instead of Enums
```python
# WRONG
booking.status = "confirmed"   # Typo? "Confirmed"? "CONFIRMED"?
room.type = 2                  # What does 2 mean?

# RIGHT
booking.status = BookingStatus.CONFIRMED
room.type = RoomType.LARGE
```

### Mistake 5: Not Making Code Extensible
```python
# WRONG: Hardcoded types
def calculate_fee(self, transaction_type, amount):
    if transaction_type == "TRANSFER":
        return amount * 0.01
    elif transaction_type == "WITHDRAWAL":
        return amount * 0.02
    # Adding a new type means modifying this method

# RIGHT: Strategy pattern
class FeeCalculator(ABC):
    @abstractmethod
    def calculate(self, amount): pass

class TransferFee(FeeCalculator):
    def calculate(self, amount):
        return amount * 0.01

class WithdrawalFee(FeeCalculator):
    def calculate(self, amount):
        return amount * 0.02

# Adding a new type = new class, no existing code changes
```

### Mistake 6: Spending Too Much Time on One Feature
```
If you're stuck for > 10 minutes on a single feature:
1. Add a TODO comment
2. Return a placeholder/dummy value
3. Move on to the next feature
4. Come back if you have time

A program with 4 working features and 1 TODO
beats a program with 2 working features and 3 broken ones.
```

### Mistake 7: Forgetting to Make It Runnable
```
The most critical thing: Your code must RUN.

Checklist before submitting:
[ ] Does it compile without errors?
[ ] Is there a main() function?
[ ] Does main() exercise all features?
[ ] Is the output readable and clear?
[ ] Can the interviewer run it without modifications?
```

### Mistake 8: Over-Engineering
```
WRONG: Building a full dependency injection framework for a 90-minute exercise
WRONG: Adding 5 levels of abstraction for a simple feature
WRONG: Implementing a custom event bus when direct method calls suffice

RIGHT: Use patterns where they genuinely help
RIGHT: Keep abstractions to 1-2 levels deep
RIGHT: Simple and working beats complex and broken
```

### Mistake 9: Poor Naming
```python
# WRONG
def proc(d, t):
    r = self.mgr.get(d)
    if r:
        r.s = t
    return r

# RIGHT
def process_booking(self, booking_id, new_status):
    booking = self.booking_repository.find_by_id(booking_id)
    if booking:
        booking.status = new_status
    return booking
```

### Mistake 10: Not Testing With Sample Inputs
```
The problem statement usually gives sample inputs/outputs.
ALWAYS verify your code produces the expected output.

If the expected output is:
  "Booking B1 created for Room R1"

And your output is:
  "Booking(id=B1, room=Room(id=R1))"

That's a PROBLEM. Match the expected format.
```

---

## Template: How to Structure ANY Solution

### Universal File Structure
```
project/
├── enums.py              # All enumerations
├── models/
│   ├── __init__.py
│   ├── user.py           # User entity
│   ├── item.py           # Domain entity
│   └── order.py          # Domain entity
├── repositories/
│   ├── __init__.py
│   └── repository.py     # In-memory storage
├── services/
│   ├── __init__.py
│   ├── core_service.py   # Primary business logic
│   └── search_service.py # Search/filter logic
├── utils/
│   ├── __init__.py
│   └── id_generator.py   # Utility functions
└── main.py               # Demo / driver
```

### Simplified Structure (Recommended for 90 min)
```
code/
├── enums.py           # All enums
├── user.py            # User model
├── item.py            # Domain model(s)
├── service.py         # Core business logic
├── search_service.py  # Optional: search
├── repository.py      # Optional: if storage is complex
└── demo.py            # Driver with all demos
```

### Generic Class Template
```python
# enums.py
from enum import Enum

class Status(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class Type(Enum):
    TYPE_A = "TYPE_A"
    TYPE_B = "TYPE_B"

# model.py
import uuid

class Entity:
    def __init__(self, name, entity_type):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.entity_type = entity_type
        self.status = Status.ACTIVE

    def __str__(self):
        return f"Entity(id={self.id}, name={self.name}, type={self.entity_type.value})"

# service.py
class EntityService:
    def __init__(self):
        self._entities = {}  # id -> Entity

    def create(self, name, entity_type):
        entity = Entity(name, entity_type)
        self._entities[entity.id] = entity
        return entity

    def get(self, entity_id):
        return self._entities.get(entity_id)

    def get_all(self):
        return list(self._entities.values())

# main.py
def main():
    service = EntityService()
    e1 = service.create("Test", Type.TYPE_A)
    print(f"Created: {e1}")
    print(f"All entities: {service.get_all()}")

if __name__ == "__main__":
    main()
```

---

## 10 Machine Coding Topics You MUST Know

### 1. In-Memory Data Storage (HashMap Patterns)
```python
# The backbone of every machine coding solution
class InMemoryStore:
    def __init__(self):
        self._data = {}           # Primary storage: id -> entity
        self._index_by_name = {}  # Secondary index: name -> [ids]

    def save(self, entity):
        self._data[entity.id] = entity
        # Maintain secondary index
        name = entity.name
        if name not in self._index_by_name:
            self._index_by_name[name] = []
        self._index_by_name[name].append(entity.id)

    def find_by_id(self, entity_id):
        return self._data.get(entity_id)

    def find_by_name(self, name):
        ids = self._index_by_name.get(name, [])
        return [self._data[eid] for eid in ids if eid in self._data]

    def find_all(self, predicate=None):
        entities = self._data.values()
        if predicate:
            entities = filter(predicate, entities)
        return list(entities)

    def delete(self, entity_id):
        if entity_id in self._data:
            del self._data[entity_id]
            return True
        return False
```

### 2. State Machines
```python
# For problems with entity lifecycle (Order, Booking, Game)
from enum import Enum

class OrderStatus(Enum):
    CREATED = "CREATED"
    CONFIRMED = "CONFIRMED"
    PREPARING = "PREPARING"
    OUT_FOR_DELIVERY = "OUT_FOR_DELIVERY"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

# Define valid transitions
VALID_TRANSITIONS = {
    OrderStatus.CREATED: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
    OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
    OrderStatus.PREPARING: [OrderStatus.OUT_FOR_DELIVERY],
    OrderStatus.OUT_FOR_DELIVERY: [OrderStatus.DELIVERED],
    OrderStatus.DELIVERED: [],      # Terminal state
    OrderStatus.CANCELLED: [],      # Terminal state
}

class Order:
    def __init__(self):
        self.status = OrderStatus.CREATED

    def transition_to(self, new_status):
        allowed = VALID_TRANSITIONS.get(self.status, [])
        if new_status not in allowed:
            raise ValueError(
                f"Cannot transition from {self.status.value} to {new_status.value}. "
                f"Allowed: {[s.value for s in allowed]}"
            )
        self.status = new_status
```

### 3. Strategy Pattern (Pluggable Algorithms)
```python
# When the problem has multiple algorithms/approaches for the same operation
from abc import ABC, abstractmethod

class SortingStrategy(ABC):
    @abstractmethod
    def sort(self, items):
        pass

class PriceSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.price)

class RatingSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.rating, reverse=True)

class DistanceSortStrategy(SortingStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.distance)

# Usage
class SearchService:
    def __init__(self):
        self._strategy = PriceSortStrategy()  # Default

    def set_sort_strategy(self, strategy):
        self._strategy = strategy

    def search(self, items, query):
        filtered = [i for i in items if query in i.name.lower()]
        return self._strategy.sort(filtered)
```

### 4. Observer Pattern (Notifications, Events)
```python
# When one action should trigger multiple side effects
from abc import ABC, abstractmethod

class EventListener(ABC):
    @abstractmethod
    def on_event(self, event_type, data):
        pass

class EventBus:
    def __init__(self):
        self._listeners = {}  # event_type -> [listeners]

    def subscribe(self, event_type, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def publish(self, event_type, data):
        for listener in self._listeners.get(event_type, []):
            listener.on_event(event_type, data)

class EmailNotifier(EventListener):
    def on_event(self, event_type, data):
        print(f"[EMAIL] {event_type}: {data}")

class SMSNotifier(EventListener):
    def on_event(self, event_type, data):
        print(f"[SMS] {event_type}: {data}")
```

### 5. Factory Pattern (Creating Different Types)
```python
# When you need to create objects of different types based on input
class VehicleFactory:
    _registry = {}

    @classmethod
    def register(cls, vehicle_type, vehicle_class):
        cls._registry[vehicle_type] = vehicle_class

    @classmethod
    def create(cls, vehicle_type, **kwargs):
        vehicle_class = cls._registry.get(vehicle_type)
        if not vehicle_class:
            raise ValueError(f"Unknown vehicle type: {vehicle_type}")
        return vehicle_class(**kwargs)

# Register types
VehicleFactory.register(VehicleType.CAR, Car)
VehicleFactory.register(VehicleType.BIKE, Bike)
VehicleFactory.register(VehicleType.TRUCK, Truck)

# Usage
vehicle = VehicleFactory.create(VehicleType.CAR, license_plate="ABC123")
```

### 6. Command Pattern (Actions with Undo)
```python
# When the problem requires undo/redo or action history
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddItemCommand(Command):
    def __init__(self, cart, item):
        self.cart = cart
        self.item = item

    def execute(self):
        self.cart.add(self.item)

    def undo(self):
        self.cart.remove(self.item)

class CommandHistory:
    def __init__(self):
        self._history = []

    def execute(self, command):
        command.execute()
        self._history.append(command)

    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()
```

### 7. Input Parsing (Reading Commands)
```python
# Many machine coding problems require parsing text commands
class CommandParser:
    def __init__(self):
        self._handlers = {}

    def register(self, command_name, handler):
        self._handlers[command_name] = handler

    def parse_and_execute(self, line):
        parts = line.strip().split()
        if not parts:
            return

        command = parts[0].upper()
        args = parts[1:]

        handler = self._handlers.get(command)
        if handler:
            try:
                handler(*args)
            except TypeError as e:
                print(f"Error: Invalid arguments for {command}: {e}")
            except Exception as e:
                print(f"Error executing {command}: {e}")
        else:
            print(f"Unknown command: {command}")

# Usage
parser = CommandParser()
parser.register("ADD_USER", lambda name, email: user_service.add(name, email))
parser.register("CREATE_BOOKING", lambda room, user, start, end: booking_service.book(room, user, start, end))

# Process commands
commands = [
    "ADD_USER Alice alice@email.com",
    "CREATE_BOOKING R1 Alice 10:00 11:00",
]
for cmd in commands:
    parser.parse_and_execute(cmd)
```

### 8. Output Formatting
```python
# Clean output makes a great impression
class OutputFormatter:
    @staticmethod
    def header(title):
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    @staticmethod
    def section(title):
        print(f"\n--- {title} ---")

    @staticmethod
    def table(headers, rows):
        # Calculate column widths
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                widths[i] = max(widths[i], len(str(cell)))

        # Print header
        header_line = " | ".join(h.ljust(widths[i]) for i, h in enumerate(headers))
        print(header_line)
        print("-" * len(header_line))

        # Print rows
        for row in rows:
            print(" | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(row)))

    @staticmethod
    def key_value(data):
        max_key_len = max(len(k) for k in data.keys())
        for key, value in data.items():
            print(f"  {key.ljust(max_key_len)} : {value}")

    @staticmethod
    def success(message):
        print(f"[SUCCESS] {message}")

    @staticmethod
    def error(message):
        print(f"[ERROR] {message}")
```

### 9. Error Handling (Graceful Failure)
```python
# Custom exceptions for domain-specific errors
class InsufficientBalanceError(Exception):
    def __init__(self, wallet_id, required, available):
        self.message = (
            f"Insufficient balance in wallet {wallet_id}. "
            f"Required: {required}, Available: {available}"
        )
        super().__init__(self.message)

class EntityNotFoundError(Exception):
    def __init__(self, entity_type, entity_id):
        self.message = f"{entity_type} with ID '{entity_id}' not found"
        super().__init__(self.message)

class InvalidStateTransitionError(Exception):
    def __init__(self, current_state, target_state):
        self.message = (
            f"Cannot transition from {current_state} to {target_state}"
        )
        super().__init__(self.message)

# Use in service layer
class WalletService:
    def transfer(self, from_wallet_id, to_wallet_id, amount):
        from_wallet = self._get_wallet_or_raise(from_wallet_id)
        to_wallet = self._get_wallet_or_raise(to_wallet_id)

        if from_wallet.balance < amount:
            raise InsufficientBalanceError(
                from_wallet_id, amount, from_wallet.balance
            )

        from_wallet.balance -= amount
        to_wallet.balance += amount

    def _get_wallet_or_raise(self, wallet_id):
        wallet = self._wallets.get(wallet_id)
        if not wallet:
            raise EntityNotFoundError("Wallet", wallet_id)
        return wallet
```

### 10. Concurrency Basics (Thread-Safe Collections)
```python
import threading
from collections import defaultdict

class ThreadSafeRepository:
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()

    def save(self, key, value):
        with self._lock:
            self._data[key] = value

    def get(self, key):
        with self._lock:
            return self._data.get(key)

    def delete(self, key):
        with self._lock:
            return self._data.pop(key, None)

    def get_all(self):
        with self._lock:
            return dict(self._data)

# Thread-safe counter for ID generation
class AtomicCounter:
    def __init__(self, start=0):
        self._value = start
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1
            return self._value
```

---

## Language-Specific Tips

### Python Tips
```python
# 1. Use dataclasses for simple models (Python 3.7+)
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Room:
    id: str
    name: str
    capacity: int
    amenities: List[str] = field(default_factory=list)

# 2. Use Enum for all constants
from enum import Enum, auto

class Priority(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()

# 3. Use uuid for generating unique IDs
import uuid
booking_id = f"BK-{str(uuid.uuid4())[:8]}"

# 4. Use defaultdict for grouping
from collections import defaultdict
bookings_by_room = defaultdict(list)

# 5. Use datetime for time handling
from datetime import datetime, timedelta
now = datetime.now()
one_hour_later = now + timedelta(hours=1)

# 6. Use typing for clarity (optional but impressive)
from typing import Dict, List, Optional
def find_available(self, start: datetime, end: datetime) -> List[Room]:
    ...
```

### Java Tips
```java
// 1. Use records for simple models (Java 16+) or Lombok
public record Room(String id, String name, int capacity) {}

// 2. Use enum with fields
public enum RoomType {
    SMALL(5), MEDIUM(10), LARGE(20);
    private final int maxCapacity;
    RoomType(int maxCapacity) { this.maxCapacity = maxCapacity; }
    public int getMaxCapacity() { return maxCapacity; }
}

// 3. Use ConcurrentHashMap for thread safety
private final Map<String, Room> rooms = new ConcurrentHashMap<>();

// 4. Use Optional for nullable returns
public Optional<Room> findById(String id) {
    return Optional.ofNullable(rooms.get(id));
}

// 5. Use Streams for filtering
List<Room> available = rooms.values().stream()
    .filter(r -> r.getCapacity() >= minCapacity)
    .filter(r -> r.isAvailable(start, end))
    .collect(Collectors.toList());
```

---

## Real Interview Examples

### Example 1: Flipkart - Parking Lot
```
Problem: Design a parking lot system
Time: 90 minutes
Requirements:
- Multiple floors, each with parking spots
- Different vehicle types (car, bike, truck)
- Park, unpark, get status
- Search by vehicle number

What they looked for:
- Vehicle hierarchy (Car extends Vehicle)
- Strategy for spot allocation
- Clean separation of ParkingLot, Floor, Spot, Vehicle
- Working demo with all operations
```

### Example 2: Uber - Ride Sharing
```
Problem: Design a simple ride-sharing system
Time: 90 minutes
Requirements:
- Drivers and riders
- Request a ride, match with nearest driver
- Different vehicle types with different pricing
- Trip history

What they looked for:
- Strategy pattern for pricing (Bike, Auto, Car)
- Clean matching algorithm
- State management for trips (REQUESTED -> ONGOING -> COMPLETED)
- Extensibility for adding new vehicle types
```

### Example 3: Swiggy - Food Delivery
```
Problem: Design a food ordering system
Time: 90 minutes
Requirements:
- Restaurants with menus
- Users can browse and order
- Order tracking with status updates
- Delivery assignment

What they looked for:
- Clean separation of Restaurant, Menu, Item, Order
- State machine for order lifecycle
- Observer pattern for status notifications
- Working order flow from browse to delivery
```

### Example 4: Cred - Expense Tracker
```
Problem: Design a personal expense tracker
Time: 90 minutes
Requirements:
- Add expenses with category
- Set monthly budgets per category
- View expenses filtered by category/date
- Budget alerts

What they looked for:
- Clean model design
- Good use of enums for categories
- Filtering and aggregation logic
- Clear output formatting
```

---

## Pre-Round Checklist

### The Night Before
```
[ ] Laptop charged and working
[ ] IDE installed and configured (IntelliJ / VS Code / PyCharm)
[ ] Language runtime installed (Java/Python/Node)
[ ] Know how to create a new project quickly
[ ] Practiced creating project structure in < 2 minutes
[ ] Reviewed common design patterns (Strategy, Factory, Observer)
[ ] Reviewed enum usage in your language
[ ] Practiced the 90-minute framework at least 3 times
```

### 5 Minutes Before the Round
```
[ ] Create a new project/folder
[ ] Create basic file structure:
    - enums.py
    - models (or a models/ folder)
    - services (or a services/ folder)
    - main.py
[ ] Write the main() boilerplate
[ ] Take a deep breath
```

### During the Round
```
[ ] Read problem statement TWICE
[ ] Ask at least 2 clarifying questions
[ ] Identify 3-5 main entities
[ ] Write enums FIRST
[ ] Build models SECOND
[ ] Core service logic THIRD
[ ] Demo/main function FOURTH
[ ] Test and fix FIFTH
```

---

## Post-Round: How to Demo

### The 5-Minute Demo Framework
```
Step 1: "Let me walk you through my design first"
  - Show the file structure
  - Briefly explain each class and its responsibility
  - Mention which design patterns you used and why

Step 2: "Let me run the program"
  - Execute main.py / Main.java
  - Show the output for each feature

Step 3: "Let me highlight a few design decisions"
  - Point out extensibility: "If we need to add X, we just create a new class"
  - Point out error handling: "Invalid inputs are handled like this"
  - Point out pattern usage: "I used Strategy here because..."

Step 4: "With more time, I would add..."
  - Concurrency / thread safety
  - More comprehensive error handling
  - Additional features from the nice-to-have list
  - Unit tests

Step 5: Answer questions confidently
  - "How would you add feature X?" → Show where the new class would go
  - "Why did you use this pattern?" → Explain the benefit
  - "What if we need to scale this?" → Discuss trade-offs
```

### Common Interviewer Questions
```
Q: "How would you add a new type of [entity]?"
A: "I'd create a new class extending [base], register it in the factory,
   and no existing code needs to change."

Q: "What if we need to support concurrent access?"
A: "I'd add locks/synchronized blocks to the repository layer
   and use thread-safe collections."

Q: "Why didn't you use [pattern]?"
A: "I considered it, but [simpler approach] was sufficient for
   the current requirements. If [scenario], then [pattern] would be better."

Q: "What would you do differently with more time?"
A: "I'd add unit tests, improve error messages, add [specific feature],
   and possibly add concurrency support."
```

---

## Quick Reference Card

```
THE MACHINE CODING CHEAT SHEET

TIME:    90 min = 10 plan + 30 core + 15 extra + 15 demo + 10 fix + 10 buffer
GOAL:    Working code > Perfect design
RULE #1: It MUST run. Partial working > Complete broken.
RULE #2: Separate concerns. No God classes.
RULE #3: Use enums. No magic strings.
RULE #4: Handle errors. No crashes.
RULE #5: Format output. Make it readable.

PATTERNS TO KNOW:
  Strategy  → Different algorithms for same operation
  Factory   → Creating different types of objects
  Observer  → Notifications and events
  Command   → Actions with undo/redo
  State     → Entity lifecycle management

FILE STRUCTURE:
  enums.py → models → services → demo.py

STORAGE:
  dict/HashMap for primary storage
  defaultdict/MultiMap for indexing
  list for ordered data

DEMO TEMPLATE:
  Setup → Create data → Show each feature → Final state
```
