# Mock Interview: Elevator System Design

## Interview Setup
- **Level:** SDE-2 / L4
- **Duration:** 45 minutes
- **Interviewer:** Staff Engineer, 12 years experience
- **Format:** Requirements -> Design -> Code -> Scalability Follow-ups

---

## The Interview Transcript

### [0:00 - 0:02] Opening

**INTERVIEWER:** "Today I'd like you to design an elevator system. Take your time to think about it, and walk me through your approach."

**CANDIDATE:** "Sure. An elevator system has quite a bit of complexity in the scheduling algorithm. Let me start by understanding the exact requirements."

---

### [0:02 - 0:10] Requirement Gathering Phase

**CANDIDATE:** "Let me start with some questions:

1. **How many elevators are we dealing with?**"

**INTERVIEWER:** "Let's say a building with 4 elevators and 20 floors."

**CANDIDATE:** "2. **Are all floors accessible by all elevators?** Some buildings have express elevators for high floors."

**INTERVIEWER:** "Good question. For now, all elevators serve all floors."

**CANDIDATE:** "3. **What types of requests?** External (pressing up/down button on a floor) and internal (pressing a floor number inside the elevator)?"

**INTERVIEWER:** "Yes, both."

**CANDIDATE:** "4. **Any capacity constraints?** Weight or person limits?"

**INTERVIEWER:** "Yes, max weight and max person count per elevator."

**CANDIDATE:** "5. **Do we need special floors?** Like basement, restricted access floors?"

**INTERVIEWER:** "Not for now."

**CANDIDATE:** "6. **What scheduling algorithm should we use?** FCFS, shortest seek first, SCAN (elevator algorithm), or LOOK?"

**INTERVIEWER:** "I'd like you to implement the LOOK algorithm but design it so we can swap algorithms."

**CANDIDATE:** "7. **Do we need emergency features?** Emergency stop, fire mode, maintenance mode?"

**INTERVIEWER:** "Include emergency stop but skip fire mode for now."

**CANDIDATE:** "8. **Door operations?** Open/close with sensor to prevent closing on people?"

**INTERVIEWER:** "Yes, basic door operations with open/close."

**CANDIDATE:** "Let me summarize:

**Core Requirements:**
- 4 elevators, 20 floors
- External requests (floor buttons) and internal requests (inside elevator)
- LOOK scheduling algorithm, but pluggable strategy
- Weight and capacity limits
- Emergency stop
- Door open/close operations
- Display current floor and direction

**Out of Scope:**
- Express elevators, restricted floors
- Fire/maintenance mode
- Voice announcements
- VIP priority

Sound good?"

**INTERVIEWER:** "Perfect."

> *INTERVIEWER NOTE: Asking about scheduling algorithms shows prior knowledge of the problem domain. Extra points for asking about express elevators - shows real-world awareness. Score: 5/5*

---

### [0:10 - 0:20] Design Phase

**CANDIDATE:** "Let me identify the entities:

**Core Classes:**
1. `ElevatorSystem` - Manages all elevators and dispatches requests
2. `Elevator` - Individual elevator car
3. `Door` - Elevator door with open/close state
4. `Floor` - Represents a floor with up/down buttons
5. `Request` - External (floor + direction) or Internal (destination floor)
6. `ElevatorScheduler` - Strategy interface for scheduling algorithms
7. `Display` - Shows current floor and direction

**Key Enums:**
- `Direction`: UP, DOWN, IDLE
- `ElevatorState`: MOVING, STOPPED, MAINTENANCE, EMERGENCY
- `DoorState`: OPEN, CLOSED

Let me think about the relationships:
- `ElevatorSystem` HAS many `Elevator`s (composition)
- `ElevatorSystem` HAS one `ElevatorScheduler` (strategy pattern)
- `Elevator` HAS one `Door` (composition)
- `Elevator` HAS one `Display` (composition)
- `Elevator` processes a queue of `Request`s
- `Floor` creates `Request`s when buttons are pressed"

**INTERVIEWER:** "Why did you separate Door into its own class?"

**CANDIDATE:** "Single Responsibility Principle. The Door has its own state machine (OPENING -> OPEN -> CLOSING -> CLOSED), its own sensor logic, and its own timing (stay open for X seconds). Putting all that in Elevator would bloat it. Also, if we later need different door types (single door, double door), we can subclass Door without touching Elevator."

> *INTERVIEWER NOTE: Good SRP justification. The door state machine observation is a bonus.*

**CANDIDATE:** "The most important design decision is the **dispatching strategy**. When someone presses 'Up' on floor 7, which elevator should respond?

I'll use the Strategy pattern:

```
ElevatorScheduler (Interface)
  |-- LOOKScheduler      (elevator/LOOK algorithm)
  |-- FCFSScheduler      (first come first served)
  |-- ShortestSeekScheduler (nearest elevator)
```

The `ElevatorSystem` holds a reference to `ElevatorScheduler` and delegates the decision."

**INTERVIEWER:** "How does the LOOK algorithm work?"

**CANDIDATE:** "LOOK is like the SCAN algorithm but smarter. The elevator moves in one direction, servicing all requests in that direction. When there are no more requests ahead, it reverses direction. Unlike SCAN, LOOK doesn't go all the way to the end floor - it only goes as far as the last request.

For example, if the elevator is at floor 5 going UP with requests for floors 8 and 12:
1. Service floor 8
2. Service floor 12
3. No more UP requests? Reverse to DOWN
4. Service any DOWN requests

This minimizes unnecessary travel."

---

### [0:20 - 0:35] Code Implementation Phase

**CANDIDATE:** "Let me code this up."

```python
from abc import ABC, abstractmethod
from enum import Enum
from collections import deque
import threading
import time


class Direction(Enum):
    UP = 1
    DOWN = -1
    IDLE = 0


class ElevatorState(Enum):
    MOVING = "moving"
    STOPPED = "stopped"
    MAINTENANCE = "maintenance"
    EMERGENCY = "emergency"


class DoorState(Enum):
    OPEN = "open"
    CLOSED = "closed"


# ---- Request ----
class Request:
    def __init__(self, floor: int, direction: Direction = None,
                 is_external: bool = True):
        self.floor = floor
        self.direction = direction  # Only for external requests
        self.is_external = is_external
        self.timestamp = time.time()

    def __repr__(self):
        kind = "EXT" if self.is_external else "INT"
        return f"Request({kind}, floor={self.floor}, dir={self.direction})"


# ---- Door ----
class Door:
    def __init__(self):
        self._state = DoorState.CLOSED
        self._lock = threading.Lock()

    @property
    def state(self) -> DoorState:
        return self._state

    def open(self) -> bool:
        with self._lock:
            if self._state == DoorState.CLOSED:
                self._state = DoorState.OPEN
                return True
            return False

    def close(self) -> bool:
        with self._lock:
            if self._state == DoorState.OPEN:
                self._state = DoorState.CLOSED
                return True
            return False


# ---- Display ----
class Display:
    def __init__(self):
        self._floor = 0
        self._direction = Direction.IDLE

    def update(self, floor: int, direction: Direction):
        self._floor = floor
        self._direction = direction

    def show(self) -> str:
        arrow = {"UP": "^", "DOWN": "v", "IDLE": "-"}
        return f"Floor {self._floor} {arrow.get(self._direction.name, '-')}"


# ---- Elevator ----
class Elevator:
    def __init__(self, elevator_id: int, max_capacity: int,
                 max_weight: float, min_floor: int = 0,
                 max_floor: int = 19):
        self.elevator_id = elevator_id
        self._current_floor = 0
        self._direction = Direction.IDLE
        self._state = ElevatorState.STOPPED
        self._door = Door()
        self._display = Display()

        self._max_capacity = max_capacity
        self._max_weight = max_weight
        self._current_load = 0
        self._min_floor = min_floor
        self._max_floor = max_floor

        # Separate sets for up and down stops
        self._up_stops: set[int] = set()
        self._down_stops: set[int] = set()
        self._lock = threading.Lock()

    @property
    def current_floor(self) -> int:
        return self._current_floor

    @property
    def direction(self) -> Direction:
        return self._direction

    @property
    def state(self) -> ElevatorState:
        return self._state

    @property
    def is_idle(self) -> bool:
        return (self._state == ElevatorState.STOPPED
                and not self._up_stops and not self._down_stops)

    def add_stop(self, floor: int, direction: Direction):
        with self._lock:
            if direction == Direction.UP:
                self._up_stops.add(floor)
            elif direction == Direction.DOWN:
                self._down_stops.add(floor)
            else:
                # Internal request: add to current direction's stops
                if self._direction == Direction.UP or self._direction == Direction.IDLE:
                    if floor >= self._current_floor:
                        self._up_stops.add(floor)
                    else:
                        self._down_stops.add(floor)
                else:
                    if floor <= self._current_floor:
                        self._down_stops.add(floor)
                    else:
                        self._up_stops.add(floor)

    def emergency_stop(self):
        with self._lock:
            self._state = ElevatorState.EMERGENCY
            self._direction = Direction.IDLE
            self._door.open()

    def resume(self):
        with self._lock:
            if self._state == ElevatorState.EMERGENCY:
                self._state = ElevatorState.STOPPED

    def move_one_floor(self):
        """Move one floor in the current direction (LOOK algorithm)."""
        with self._lock:
            if self._state in (ElevatorState.EMERGENCY, ElevatorState.MAINTENANCE):
                return

            # Determine direction if idle
            if self._direction == Direction.IDLE:
                if self._up_stops:
                    self._direction = Direction.UP
                elif self._down_stops:
                    self._direction = Direction.DOWN
                else:
                    return  # Nothing to do

            # Move one floor
            if self._direction == Direction.UP:
                self._current_floor += 1
                self._state = ElevatorState.MOVING

                # Check if we should stop at this floor
                if self._current_floor in self._up_stops:
                    self._up_stops.discard(self._current_floor)
                    self._stop_at_floor()

                # LOOK: reverse if no more UP requests ahead
                if not any(f > self._current_floor for f in self._up_stops):
                    if self._down_stops:
                        self._direction = Direction.DOWN
                    elif not self._up_stops:
                        self._direction = Direction.IDLE

            elif self._direction == Direction.DOWN:
                self._current_floor -= 1
                self._state = ElevatorState.MOVING

                if self._current_floor in self._down_stops:
                    self._down_stops.discard(self._current_floor)
                    self._stop_at_floor()

                # LOOK: reverse if no more DOWN requests below
                if not any(f < self._current_floor for f in self._down_stops):
                    if self._up_stops:
                        self._direction = Direction.UP
                    elif not self._down_stops:
                        self._direction = Direction.IDLE

            self._display.update(self._current_floor, self._direction)

    def _stop_at_floor(self):
        self._state = ElevatorState.STOPPED
        self._door.open()
        # In real system: wait for passengers, then close
        self._door.close()

    def distance_to(self, floor: int, direction: Direction) -> int:
        """Estimate how many floors until this elevator can service the request."""
        if self.is_idle:
            return abs(self._current_floor - floor)

        if self._direction == Direction.UP:
            if direction == Direction.UP and floor >= self._current_floor:
                return floor - self._current_floor
            else:
                # Must go up to max stop, come back down
                max_stop = max(self._up_stops) if self._up_stops else self._current_floor
                return (max_stop - self._current_floor) + (max_stop - floor)
        else:  # DOWN
            if direction == Direction.DOWN and floor <= self._current_floor:
                return self._current_floor - floor
            else:
                min_stop = min(self._down_stops) if self._down_stops else self._current_floor
                return (self._current_floor - min_stop) + (floor - min_stop)


# ---- Scheduling Strategy ----
class ElevatorScheduler(ABC):
    @abstractmethod
    def select_elevator(self, request: Request,
                        elevators: list[Elevator]) -> Elevator:
        pass


class LOOKScheduler(ElevatorScheduler):
    """Select the elevator that can reach the request floor fastest."""
    def select_elevator(self, request: Request,
                        elevators: list[Elevator]) -> Elevator:
        available = [e for e in elevators
                     if e.state not in (ElevatorState.EMERGENCY,
                                        ElevatorState.MAINTENANCE)]
        if not available:
            raise RuntimeError("No elevators available")

        direction = request.direction or Direction.IDLE
        return min(available,
                   key=lambda e: e.distance_to(request.floor, direction))


class FCFSScheduler(ElevatorScheduler):
    """Round-robin assignment."""
    def __init__(self):
        self._next = 0

    def select_elevator(self, request: Request,
                        elevators: list[Elevator]) -> Elevator:
        available = [e for e in elevators
                     if e.state not in (ElevatorState.EMERGENCY,
                                        ElevatorState.MAINTENANCE)]
        if not available:
            raise RuntimeError("No elevators available")
        chosen = available[self._next % len(available)]
        self._next += 1
        return chosen


# ---- Elevator System ----
class ElevatorSystem:
    def __init__(self, num_elevators: int, num_floors: int,
                 max_capacity: int = 10, max_weight: float = 1000.0,
                 scheduler: ElevatorScheduler = None):
        self._elevators = [
            Elevator(i, max_capacity, max_weight, 0, num_floors - 1)
            for i in range(num_elevators)
        ]
        self._num_floors = num_floors
        self._scheduler = scheduler or LOOKScheduler()
        self._lock = threading.Lock()

    def set_scheduler(self, scheduler: ElevatorScheduler):
        with self._lock:
            self._scheduler = scheduler

    def request_elevator(self, floor: int, direction: Direction) -> Elevator:
        """External request: someone on a floor presses UP or DOWN."""
        request = Request(floor, direction, is_external=True)
        with self._lock:
            elevator = self._scheduler.select_elevator(
                request, self._elevators)
            elevator.add_stop(floor, direction)
            return elevator

    def select_floor(self, elevator_id: int, floor: int):
        """Internal request: someone inside presses a floor button."""
        elevator = self._elevators[elevator_id]
        elevator.add_stop(floor, Direction.IDLE)

    def emergency_stop(self, elevator_id: int):
        self._elevators[elevator_id].emergency_stop()

    def resume(self, elevator_id: int):
        self._elevators[elevator_id].resume()

    def status(self) -> list[dict]:
        return [
            {
                "id": e.elevator_id,
                "floor": e.current_floor,
                "direction": e.direction.name,
                "state": e.state.value,
            }
            for e in self._elevators
        ]

    def step(self):
        """Simulate one time step: each elevator moves one floor."""
        for elevator in self._elevators:
            elevator.move_one_floor()
```

**INTERVIEWER:** "Interesting. Let me ask some pointed questions."

---

### [0:35 - 0:40] Interviewer Challenges

**INTERVIEWER:** "Can you handle 50 elevators efficiently? Your `LOOKScheduler.select_elevator` iterates all elevators for every request."

**CANDIDATE:** "For 50 elevators, linear scan is still O(50) per request which is acceptable. But if we had hundreds and very high request throughput, I'd optimize:

1. **Zone-based partitioning:** Divide floors into zones, assign elevator groups to zones. Reduces the search space.

```python
class ZonedScheduler(ElevatorScheduler):
    def __init__(self, zones: dict[range, list[int]]):
        # zones maps floor ranges to elevator IDs
        self._zones = zones

    def select_elevator(self, request, elevators):
        # Only consider elevators in the request's zone
        for floor_range, elevator_ids in self._zones.items():
            if request.floor in floor_range:
                zone_elevators = [e for e in elevators
                                  if e.elevator_id in elevator_ids]
                return min(zone_elevators,
                           key=lambda e: e.distance_to(
                               request.floor, request.direction))
        raise RuntimeError("Floor not in any zone")
```

2. **Priority queue per zone:** Keep elevators sorted by current position for O(log n) lookup of nearest elevator.

3. **Event-driven updates:** Instead of recalculating distances from scratch, update only when elevator positions change."

**INTERVIEWER:** "What about starvation? A floor in the middle might never get served if elevators keep getting redirected."

**CANDIDATE:** "Great point. I'd add **aging** to requests. Each request has a timestamp. If a request has been waiting longer than a threshold, it gets priority:

```python
class AntiStarvationScheduler(ElevatorScheduler):
    STARVATION_THRESHOLD = 60  # seconds

    def select_elevator(self, request, elevators):
        # Check if this is a starving request
        wait_time = time.time() - request.timestamp
        if wait_time > self.STARVATION_THRESHOLD:
            # Find closest idle or same-direction elevator
            # with highest priority (force serve)
            idle = [e for e in elevators if e.is_idle]
            if idle:
                return min(idle,
                           key=lambda e: abs(e.current_floor - request.floor))
        # Default LOOK behavior
        return LOOKScheduler().select_elevator(request, elevators)
```

This ensures no floor waits indefinitely."

**INTERVIEWER:** "How would you handle peak hours, like morning rush where everyone goes from ground floor up?"

**CANDIDATE:** "During peak hours, I'd switch to a **special peak scheduler**:

1. **Morning mode:** Position idle elevators at the ground floor. Use the Strategy pattern - `PeakHourScheduler` replaces the normal scheduler during peak times.
2. **Evening mode:** Position idle elevators at high floors.
3. **Dynamic detection:** Track request patterns. If 80%+ of requests in the last 5 minutes are from floor 0 going UP, automatically switch to peak mode.

```python
class PeakHourScheduler(ElevatorScheduler):
    def __init__(self, base_floor: int = 0):
        self._base_floor = base_floor

    def select_elevator(self, request, elevators):
        # Send idle elevators back to base floor
        for e in elevators:
            if e.is_idle and e.current_floor != self._base_floor:
                e.add_stop(self._base_floor, Direction.DOWN)

        # Normal dispatch for actual requests
        return LOOKScheduler().select_elevator(request, elevators)
```"

> *INTERVIEWER NOTE: Peak hour handling shows real-world systems thinking. The dynamic detection idea is impressive.*

---

### [0:40 - 0:43] Edge Cases

**INTERVIEWER:** "What edge cases do you see?"

**CANDIDATE:** "Several important ones:

1. **Overweight:** Elevator should not move if weight exceeds limit. The door stays open and a buzzer sounds.

```python
def can_move(self) -> bool:
    return self._current_load <= self._max_weight
```

2. **Door obstruction:** If the door sensor detects something, keep the door open and retry closing after a delay. After N retries, sound an alarm.

3. **Power failure:** Save elevator state (floor, direction, pending stops) to persistent storage. On restart, move to nearest floor and open doors.

4. **Simultaneous requests:** Two people on different floors press the button at the exact same time. The lock in `request_elevator` serializes these correctly.

5. **Request while moving:** Someone inside presses a floor that's already passed. Add it to the opposite direction's stop set.

6. **All elevators in emergency/maintenance:** Return an error or queue the request until an elevator becomes available."

---

### [0:43 - 0:45] Design Patterns Summary

**INTERVIEWER:** "Can you summarize the design patterns you used?"

**CANDIDATE:** "
1. **Strategy Pattern** - ElevatorScheduler with multiple algorithm implementations
2. **State Pattern** - Elevator states (MOVING, STOPPED, EMERGENCY, MAINTENANCE) control behavior
3. **Observer Pattern** (implied) - Display updates when elevator moves
4. **Singleton** (intentionally NOT used) - Multiple elevator systems could exist in a campus
5. **Command Pattern** - Each Request is a command object that encapsulates what needs to happen
6. **Template Method** - The `move_one_floor` method defines the skeleton, subclasses could override specific steps"

---

## Interviewer Scoring

### Scoring Breakdown

| Criteria | Score (1-5) | Notes |
|----------|-------------|-------|
| **Requirements Gathering** | 5/5 | Asked about scheduling algorithm by name - shows preparation |
| **Object Identification** | 5/5 | Clean separation: Door, Display, Elevator, Scheduler |
| **Class Design & Relationships** | 5/5 | Strategy pattern for scheduler was perfect |
| **Design Patterns** | 5/5 | Strategy, State, Command, Observer - all justified |
| **Code Quality** | 4/5 | LOOK implementation is solid but could be cleaner |
| **Communication** | 5/5 | Clear, structured, used terminology correctly |
| **Edge Cases** | 4/5 | Good coverage, the overweight/power failure ones are strong |

### Overall: **4.7/5 - Strong Hire**

### What Went Well
- Knew the LOOK algorithm by name and explained it clearly
- Strategy pattern was the perfect choice and was identified early
- Scalability answers (zoning, aging, peak hours) showed systems thinking
- Separation of Door class showed SRP awareness
- The `distance_to` method showed understanding of elevator physics

### What Could Be Better
- LOOK algorithm implementation could be more elegant with sorted containers
- Did not discuss elevator weight/load tracking in the initial code
- Could have drawn a state machine diagram for elevator states
- The `move_one_floor` method is long and could be decomposed

### Key Differentiators
- **L3:** Would implement basic elevator movement but miss scheduling
- **L4 (shown):** Strategy pattern for scheduling, anti-starvation, peak hours
- **L5:** Would discuss distributed coordination, consensus for elevator assignment, real-time constraints

---

## Key Takeaways for Candidates

1. **Know the algorithms** - FCFS, SSTF, SCAN, C-SCAN, LOOK are elevator classics
2. **Strategy pattern is your friend** - Any time there's an algorithm choice, use Strategy
3. **Think about physical constraints** - Weight, door timing, power failure
4. **Scalability has multiple dimensions** - More elevators, more floors, more requests per second
5. **Peak hours show real-world thinking** - Interviewers love this
6. **State machines are natural** - Elevator states should be explicit enums, not if/else chains
