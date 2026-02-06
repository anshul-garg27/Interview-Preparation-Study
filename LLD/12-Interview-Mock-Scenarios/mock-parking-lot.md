# Mock Interview: Parking Lot System Design

## Interview Setup
- **Level:** SDE-2 / L4
- **Duration:** 45 minutes
- **Interviewer:** Senior Engineer, 8 years experience
- **Format:** Requirements -> Design -> Code -> Follow-ups

---

## The Interview Transcript

### [0:00 - 0:02] Opening

**INTERVIEWER:** "Thanks for joining today. For our low-level design round, I'd like you to design a Parking Lot system. Take a moment to think about it, and when you're ready, walk me through your approach."

**CANDIDATE:** "Sure, thank you. Before jumping into the design, I'd like to ask some clarifying questions to make sure I understand the scope correctly."

**INTERVIEWER:** "Absolutely, go ahead."

> *INTERVIEWER NOTE: Good start. Candidate didn't jump straight into coding. This shows discipline.*

---

### [0:02 - 0:08] Requirement Gathering Phase

**CANDIDATE:** "Let me understand the basic requirements first:

1. **What types of vehicles do we need to support?** Motorcycles, cars, buses, or anything else?"

**INTERVIEWER:** "Let's support motorcycles, cars, and buses."

**CANDIDATE:** "2. **Is this a single parking lot or do we need to support multiple lots?**"

**INTERVIEWER:** "Start with a single lot. We can discuss multiple later."

**CANDIDATE:** "3. **How is parking structured?** Is it multi-floor? Different zones?"

**INTERVIEWER:** "Yes, multiple floors. Each floor has a fixed number of spots."

**CANDIDATE:** "4. **Do different vehicle types need different spot sizes?**"

**INTERVIEWER:** "Yes. A motorcycle takes a small spot, a car takes a medium, and a bus takes a large spot."

**CANDIDATE:** "5. **Do we need a payment system, or is it just about managing spots?**"

**INTERVIEWER:** "Include basic payment. Hourly rate based on vehicle type."

**CANDIDATE:** "6. **Do we need real-time availability display?**"

**INTERVIEWER:** "Yes, we should be able to check available spots per floor."

**CANDIDATE:** "7. **Any specific entry/exit gate requirements?**"

**INTERVIEWER:** "Let's have multiple entry and exit points. A ticket is issued at entry."

**CANDIDATE:** "Great. Let me summarize the requirements before proceeding:

**Core Requirements:**
- Multi-floor parking lot with small, medium, and large spots
- Support motorcycles, cars, and buses
- Multiple entry/exit gates
- Ticket-based system: ticket issued at entry, payment at exit
- Hourly rate based on vehicle type
- Real-time availability tracking per floor

**Out of scope (for now):**
- Reservation system
- Electric vehicle charging
- Handicap spots
- Valet parking

Does that sound right?"

**INTERVIEWER:** "Perfect. Let's proceed with that."

> *INTERVIEWER NOTE: Excellent requirement gathering. Candidate asked targeted questions, summarized clearly, and explicitly stated what's out of scope. Score: 5/5 for this phase.*

---

### [0:08 - 0:18] Class Identification & Design Phase

**CANDIDATE:** "Let me identify the main entities first. I'll think out loud.

**Core Entities:**
1. `ParkingLot` - The main system, singleton since we're starting with one lot
2. `ParkingFloor` - Each floor in the lot
3. `ParkingSpot` - Individual spots (Small, Medium, Large)
4. `Vehicle` - Abstract base for Motorcycle, Car, Bus
5. `Ticket` - Issued at entry, tracks duration
6. `EntryGate` / `ExitGate` - Handle entry and exit
7. `Payment` - Handles payment calculation

Let me think about the relationships:
- ParkingLot HAS many ParkingFloors (composition)
- ParkingFloor HAS many ParkingSpots (composition)
- ParkingSpot can hold one Vehicle (association)
- Ticket references a Vehicle and a ParkingSpot
- EntryGate creates Tickets
- ExitGate processes Payment"

**INTERVIEWER:** "Good. Why did you choose composition over inheritance for ParkingLot and ParkingFloor?"

**CANDIDATE:** "Because a ParkingFloor cannot exist independently without a ParkingLot. If the lot is destroyed, the floors go with it. That's the textbook definition of composition. If floors could be shared between lots, I'd use aggregation instead."

> *INTERVIEWER NOTE: Clean justification of composition. Shows understanding beyond just the code.*

**CANDIDATE:** "Now let me sketch the class hierarchy:

```
Vehicle (Abstract)
  |-- Motorcycle
  |-- Car
  |-- Bus

ParkingSpot (Abstract)
  |-- SmallSpot      -> fits Motorcycle
  |-- MediumSpot     -> fits Motorcycle, Car
  |-- LargeSpot      -> fits Motorcycle, Car, Bus

ParkingFloor
  |-- floor_number
  |-- spots: List[ParkingSpot]
  |-- display_board: DisplayBoard

ParkingLot (Singleton)
  |-- floors: List[ParkingFloor]
  |-- entry_gates: List[EntryGate]
  |-- exit_gates: List[ExitGate]

Ticket
  |-- ticket_id
  |-- vehicle: Vehicle
  |-- spot: ParkingSpot
  |-- entry_time
  |-- exit_time
  |-- payment: Payment

Payment
  |-- amount
  |-- payment_method
  |-- status
```"

**INTERVIEWER:** "I notice you made ParkingSpot abstract. What methods would it have?"

**CANDIDATE:** "The abstract ParkingSpot would have:
- `can_fit(vehicle: Vehicle) -> bool` - abstract method, each subclass determines what fits
- `assign_vehicle(vehicle)` and `remove_vehicle()` - concrete methods
- `is_available() -> bool` - concrete method checking if a vehicle is assigned

The key design decision is that the **spot determines if it can hold a vehicle**, not the other way around. This follows the Tell-Don't-Ask principle."

**INTERVIEWER:** "Interesting. Why not have Vehicle know which spot types it fits?"

**CANDIDATE:** "If Vehicle knows about spot types, then adding a new spot type means modifying all Vehicle subclasses. That violates the Open-Closed Principle. With my approach, I can add a new spot type (say, CompactSpot) without touching Vehicle at all. The new spot just implements `can_fit()` to define which vehicles it accepts."

> *INTERVIEWER NOTE: Excellent. Candidate justified design with SOLID principles without being prompted. This is L4+ behavior.*

---

### [0:18 - 0:32] Code Implementation Phase

**CANDIDATE:** "Let me start coding. I'll begin with the core classes."

```python
from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime
import threading


class VehicleType(Enum):
    MOTORCYCLE = 1
    CAR = 2
    BUS = 3


class PaymentStatus(Enum):
    PENDING = 1
    COMPLETED = 2
    FAILED = 3


class SpotType(Enum):
    SMALL = 1
    MEDIUM = 2
    LARGE = 3


# ---- Vehicle Hierarchy ----
class Vehicle(ABC):
    def __init__(self, license_plate: str, vehicle_type: VehicleType):
        self._license_plate = license_plate
        self._vehicle_type = vehicle_type

    @property
    def license_plate(self) -> str:
        return self._license_plate

    @property
    def vehicle_type(self) -> VehicleType:
        return self._vehicle_type


class Motorcycle(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.MOTORCYCLE)


class Car(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.CAR)


class Bus(Vehicle):
    def __init__(self, license_plate: str):
        super().__init__(license_plate, VehicleType.BUS)


# ---- Parking Spot Hierarchy ----
class ParkingSpot(ABC):
    def __init__(self, spot_id: str, spot_type: SpotType):
        self._spot_id = spot_id
        self._spot_type = spot_type
        self._vehicle = None
        self._lock = threading.Lock()

    @property
    def is_available(self) -> bool:
        return self._vehicle is None

    @abstractmethod
    def can_fit(self, vehicle: Vehicle) -> bool:
        pass

    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        with self._lock:
            if not self.is_available or not self.can_fit(vehicle):
                return False
            self._vehicle = vehicle
            return True

    def remove_vehicle(self) -> Vehicle:
        with self._lock:
            vehicle = self._vehicle
            self._vehicle = None
            return vehicle


class SmallSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, SpotType.SMALL)

    def can_fit(self, vehicle: Vehicle) -> bool:
        return vehicle.vehicle_type == VehicleType.MOTORCYCLE


class MediumSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, SpotType.MEDIUM)

    def can_fit(self, vehicle: Vehicle) -> bool:
        return vehicle.vehicle_type in (VehicleType.MOTORCYCLE, VehicleType.CAR)


class LargeSpot(ParkingSpot):
    def __init__(self, spot_id: str):
        super().__init__(spot_id, SpotType.LARGE)

    def can_fit(self, vehicle: Vehicle) -> bool:
        return True  # Large spots fit any vehicle
```

**INTERVIEWER:** "I see you added a lock to ParkingSpot. Walk me through why."

**CANDIDATE:** "In a real parking lot, multiple entry gates operate concurrently. Two gates might try to assign the last available spot simultaneously. Without the lock, we could have a race condition where both `is_available` checks pass, and two vehicles get assigned the same spot. The lock on `assign_vehicle` ensures atomicity."

**INTERVIEWER:** "Good. What about the check-then-act issue? You check `is_available` and then assign inside the lock, but couldn't someone call `is_available` from outside and get a stale result?"

**CANDIDATE:** "Yes, that's a valid concern. The `is_available` property is for display purposes only - showing available count on the board. The actual assignment is protected by the lock in `assign_vehicle`. The caller should always check the boolean return value of `assign_vehicle` rather than relying on `is_available` beforehand."

> *INTERVIEWER NOTE: Candidate identified and handled the TOCTOU (Time of Check, Time of Use) race condition correctly.*

**CANDIDATE:** "Let me continue with ParkingFloor and the Ticket system."

```python
class ParkingFloor:
    def __init__(self, floor_number: int, small: int, medium: int, large: int):
        self._floor_number = floor_number
        self._spots: list[ParkingSpot] = []

        for i in range(small):
            self._spots.append(SmallSpot(f"F{floor_number}-S{i}"))
        for i in range(medium):
            self._spots.append(MediumSpot(f"F{floor_number}-M{i}"))
        for i in range(large):
            self._spots.append(LargeSpot(f"F{floor_number}-L{i}"))

    def find_spot(self, vehicle: Vehicle) -> ParkingSpot | None:
        for spot in self._spots:
            if spot.is_available and spot.can_fit(vehicle):
                return spot
        return None

    def available_spots(self) -> dict[SpotType, int]:
        counts = {st: 0 for st in SpotType}
        for spot in self._spots:
            if spot.is_available:
                counts[spot._spot_type] += 1
        return counts


class Ticket:
    _counter = 0
    _lock = threading.Lock()

    def __init__(self, vehicle: Vehicle, spot: ParkingSpot):
        with Ticket._lock:
            Ticket._counter += 1
            self._ticket_id = f"T-{Ticket._counter}"
        self._vehicle = vehicle
        self._spot = spot
        self._entry_time = datetime.now()
        self._exit_time = None
        self._payment = None

    @property
    def ticket_id(self) -> str:
        return self._ticket_id

    def close(self):
        self._exit_time = datetime.now()

    def get_duration_hours(self) -> float:
        end = self._exit_time or datetime.now()
        delta = end - self._entry_time
        return max(1.0, delta.total_seconds() / 3600)  # Minimum 1 hour


class PaymentProcessor:
    HOURLY_RATES = {
        VehicleType.MOTORCYCLE: 10,
        VehicleType.CAR: 20,
        VehicleType.BUS: 40,
    }

    def process(self, ticket: Ticket) -> float:
        hours = ticket.get_duration_hours()
        rate = self.HOURLY_RATES[ticket._vehicle.vehicle_type]
        amount = hours * rate
        ticket._payment = amount
        return amount


class ParkingLot:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self, name: str, floors: list[ParkingFloor]):
        if hasattr(self, '_initialized'):
            return
        self._name = name
        self._floors = floors
        self._active_tickets: dict[str, Ticket] = {}  # license -> ticket
        self._payment_processor = PaymentProcessor()
        self._initialized = True

    def enter(self, vehicle: Vehicle) -> Ticket | None:
        for floor in self._floors:
            spot = floor.find_spot(vehicle)
            if spot:
                if spot.assign_vehicle(vehicle):
                    ticket = Ticket(vehicle, spot)
                    self._active_tickets[vehicle.license_plate] = ticket
                    return ticket
        return None  # Parking full

    def exit(self, license_plate: str) -> float:
        ticket = self._active_tickets.pop(license_plate, None)
        if not ticket:
            raise ValueError(f"No active ticket for {license_plate}")

        ticket.close()
        amount = self._payment_processor.process(ticket)
        ticket._spot.remove_vehicle()
        return amount

    def get_availability(self) -> dict[int, dict[SpotType, int]]:
        result = {}
        for floor in self._floors:
            result[floor._floor_number] = floor.available_spots()
        return result
```

**INTERVIEWER:** "Walk me through the `enter` method. What happens if `find_spot` returns a spot but `assign_vehicle` fails?"

**CANDIDATE:** "Good catch. That can happen if between `find_spot` and `assign_vehicle`, another thread takes that spot. In my current code, if `assign_vehicle` fails, I move to the next floor. But I should really retry on the same floor since there might be other available spots. Let me fix that."

```python
    def enter(self, vehicle: Vehicle) -> Ticket | None:
        for floor in self._floors:
            while True:
                spot = floor.find_spot(vehicle)
                if spot is None:
                    break  # No spots on this floor, try next
                if spot.assign_vehicle(vehicle):
                    ticket = Ticket(vehicle, spot)
                    self._active_tickets[vehicle.license_plate] = ticket
                    return ticket
                # Assignment failed (race condition), retry on same floor
        return None
```

> *INTERVIEWER NOTE: Candidate identified the race condition in their own code when prompted, and fixed it correctly. This is strong problem-solving ability.*

---

### [0:32 - 0:38] Follow-up Questions

**INTERVIEWER:** "Now, what if we need to support multiple parking lots?"

**CANDIDATE:** "I'd remove the Singleton pattern and introduce a ParkingLotManager:

```python
class ParkingLotManager:
    def __init__(self):
        self._lots: dict[str, ParkingLot] = {}

    def add_lot(self, lot: ParkingLot):
        self._lots[lot._name] = lot

    def find_nearest_lot(self, location) -> ParkingLot:
        # Strategy pattern: could be nearest, cheapest, most available
        pass
```

The key change is applying the Strategy pattern for lot selection. Different strategies could be NearestLotStrategy, CheapestLotStrategy, MostAvailableStrategy."

**INTERVIEWER:** "How would you handle reserved spots?"

**CANDIDATE:** "I'd add a `ReservedSpot` decorator around any ParkingSpot:

```python
class ReservedSpotDecorator(ParkingSpot):
    def __init__(self, spot: ParkingSpot, reserved_for: str):
        self._wrapped_spot = spot
        self._reserved_for = reserved_for

    def can_fit(self, vehicle: Vehicle) -> bool:
        return (vehicle.license_plate == self._reserved_for
                and self._wrapped_spot.can_fit(vehicle))
```

This uses the Decorator pattern so I don't have to modify existing spot classes."

**INTERVIEWER:** "What about electric vehicle charging spots?"

**CANDIDATE:** "I'd add an `EVChargingSpot` subclass of ParkingSpot that has a `charger` field. The charger itself would be a separate class with `start_charging()` and `stop_charging()` methods. This follows composition - the spot HAS a charger rather than IS a charger."

---

### [0:38 - 0:42] Edge Cases Discussion

**INTERVIEWER:** "What edge cases should we handle?"

**CANDIDATE:** "Several:

1. **Vehicle already parked:** Check `_active_tickets` before allowing entry
2. **Exit without entry:** Handle missing ticket gracefully
3. **Lot is full:** Return None from `enter()`, display 'FULL' at gates
4. **Payment failure:** Need retry logic and a way to hold the vehicle until paid
5. **System crash mid-transaction:** Tickets should be persisted, not just in-memory
6. **Overflow timing:** For long stays crossing midnight or day boundaries
7. **Bus needing multiple spots:** A bus might need 3-5 large spots in sequence

Let me handle the first one in code:"

```python
    def enter(self, vehicle: Vehicle) -> Ticket | None:
        if vehicle.license_plate in self._active_tickets:
            raise ValueError(f"Vehicle {vehicle.license_plate} already parked")
        # ... rest of the method
```

**INTERVIEWER:** "Good. What about the bus needing multiple spots?"

**CANDIDATE:** "For that, I'd modify LargeSpot to potentially be grouped. I'd add a `SpotGroup` class:

```python
class SpotGroup:
    def __init__(self, spots: list[ParkingSpot]):
        self._spots = spots

    def can_fit(self, vehicle: Vehicle) -> bool:
        return all(spot.can_fit(vehicle) and spot.is_available
                   for spot in self._spots)

    def assign_vehicle(self, vehicle: Vehicle) -> bool:
        # Need to lock ALL spots atomically
        locks_acquired = []
        try:
            for spot in self._spots:
                spot._lock.acquire()
                locks_acquired.append(spot)
            # Check again after acquiring all locks
            if all(s.is_available and s.can_fit(vehicle) for s in self._spots):
                for spot in self._spots:
                    spot._vehicle = vehicle
                return True
            return False
        finally:
            for spot in locks_acquired:
                spot._lock.release()
```

Notice I acquire all locks before assigning to prevent partial assignment - that's the all-or-nothing pattern."

> *INTERVIEWER NOTE: The SpotGroup with atomic locking is an advanced concept. Candidate demonstrates awareness of distributed locking concerns.*

---

### [0:42 - 0:45] Wrap-up

**INTERVIEWER:** "Great job. Any final thoughts on the design?"

**CANDIDATE:** "A few things I'd add in a production system:
1. **Observer pattern** for the display board - spots notify the board when status changes
2. **Database persistence** for tickets and payment records
3. **Event sourcing** for audit trail - every entry/exit/payment is an event
4. **Rate limiting** at entry gates to prevent system overload
5. **Monitoring** - alerts when lot is nearly full, or when average wait time exceeds threshold"

**INTERVIEWER:** "Thank you, that was a solid discussion."

---

## Interviewer Scoring

### Scoring Breakdown

| Criteria | Score (1-5) | Notes |
|----------|-------------|-------|
| **Requirements Gathering** | 5/5 | Asked 7 targeted questions, summarized well, defined scope and out-of-scope |
| **Object Identification** | 5/5 | Identified all core entities, clear hierarchy |
| **Class Design & Relationships** | 4/5 | Good composition/inheritance choices. Could have discussed more interfaces |
| **Design Patterns** | 5/5 | Singleton, Strategy, Decorator, Observer - all used appropriately |
| **Code Quality** | 4/5 | Clean code, thread-safe, but initial race condition in enter() |
| **Communication** | 5/5 | Thought out loud, explained trade-offs, accepted feedback well |
| **Edge Cases** | 4/5 | Good coverage, atomic locking for bus spots was impressive |

### Overall: **4.6/5 - Strong Hire**

### What Went Well
- Requirement gathering was textbook perfect
- Justified every design decision with principles (OCP, Tell-Don't-Ask)
- Identified race condition when prompted, fixed it correctly
- Extension discussion (reservations, EV, multi-lot) showed scalable thinking
- Thread safety was baked in from the start

### What Could Be Better
- Initial `enter()` method had a race condition (caught when prompted)
- Could have introduced interfaces (Protocol classes) for better abstraction
- The `find_spot()` method uses linear search - could discuss optimization
- Did not discuss the DisplayBoard implementation in detail

### Key Differentiators (L3 vs L4)
- **L3 behavior:** Would have designed the spot-vehicle relationship but missed concurrency
- **L4 behavior (shown):** Thread-safe from start, multiple design patterns, atomic locking for bus, Strategy pattern for lot selection

---

## Key Takeaways for Candidates

1. **Always start with requirements** - Spend 5-8 minutes clarifying. It shows maturity.
2. **Think out loud** - The interviewer can't score what they can't hear.
3. **Justify with principles** - Don't just design; explain WHY using SOLID, GRASP, etc.
4. **Handle concurrency** - This separates L3 from L4 candidates.
5. **Accept feedback gracefully** - When the interviewer hints at a bug, find it and fix it.
6. **Discuss extensions** - Show that your design is extensible without saying "I'd refactor."
