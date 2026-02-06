"""
Elevator class for the Elevator System.
Uses the State pattern for managing elevator behavior.
States: Idle, MovingUp, MovingDown, DoorOpen.
"""

import threading
from abc import ABC, abstractmethod

from enums import Direction, DoorState
from door import Door
from display import Display


# ---- State Pattern ----

class ElevatorState(ABC):
    """Abstract state for the elevator state machine."""

    @abstractmethod
    def handle(self, elevator: "Elevator") -> None:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class IdleState(ElevatorState):
    def handle(self, elevator: "Elevator") -> None:
        if elevator.pending_requests:
            next_floor = elevator.pending_requests[0]
            if next_floor > elevator.current_floor:
                elevator.direction = Direction.UP
                elevator.set_state(MovingUpState())
            elif next_floor < elevator.current_floor:
                elevator.direction = Direction.DOWN
                elevator.set_state(MovingDownState())
            else:
                elevator.set_state(DoorOpenState())

    def name(self) -> str:
        return "IDLE"


class MovingUpState(ElevatorState):
    def handle(self, elevator: "Elevator") -> None:
        if not elevator.pending_requests:
            elevator.direction = Direction.IDLE
            elevator.set_state(IdleState())
            return
        target = elevator.pending_requests[0]
        if elevator.current_floor < target:
            elevator.current_floor += 1
            elevator.log(f"Moving UP -> Floor {elevator.current_floor}")
            if elevator.current_floor == target:
                elevator.set_state(DoorOpenState())
        else:
            elevator.set_state(DoorOpenState())

    def name(self) -> str:
        return "MOVING_UP"


class MovingDownState(ElevatorState):
    def handle(self, elevator: "Elevator") -> None:
        if not elevator.pending_requests:
            elevator.direction = Direction.IDLE
            elevator.set_state(IdleState())
            return
        target = elevator.pending_requests[0]
        if elevator.current_floor > target:
            elevator.current_floor -= 1
            elevator.log(f"Moving DOWN -> Floor {elevator.current_floor}")
            if elevator.current_floor == target:
                elevator.set_state(DoorOpenState())
        else:
            elevator.set_state(DoorOpenState())

    def name(self) -> str:
        return "MOVING_DOWN"


class DoorOpenState(ElevatorState):
    def handle(self, elevator: "Elevator") -> None:
        elevator.door.open()
        while elevator.current_floor in elevator.pending_requests:
            elevator.pending_requests.remove(elevator.current_floor)
        elevator.log(f"Door OPEN at Floor {elevator.current_floor} (served)")
        elevator.door.close()
        elevator.log(f"Door CLOSED at Floor {elevator.current_floor}")
        if elevator.pending_requests:
            next_floor = elevator.pending_requests[0]
            if next_floor > elevator.current_floor:
                elevator.direction = Direction.UP
                elevator.set_state(MovingUpState())
            else:
                elevator.direction = Direction.DOWN
                elevator.set_state(MovingDownState())
        else:
            elevator.direction = Direction.IDLE
            elevator.set_state(IdleState())

    def name(self) -> str:
        return "DOOR_OPEN"


# ---- Elevator ----

class Elevator:
    """A single elevator car with state machine behavior."""

    def __init__(self, elevator_id: int, min_floor: int = 0, max_floor: int = 10) -> None:
        self.elevator_id = elevator_id
        self.current_floor: int = 0
        self.min_floor = min_floor
        self.max_floor = max_floor
        self.direction: Direction = Direction.IDLE
        self.door = Door(elevator_id)
        self.display = Display(elevator_id)
        self._state: ElevatorState = IdleState()
        self.pending_requests: list[int] = []
        self._lock = threading.Lock()

    def set_state(self, state: ElevatorState) -> None:
        self._state = state

    def add_request(self, floor: int) -> None:
        """Add a floor request if valid and not already queued."""
        with self._lock:
            if self.min_floor <= floor <= self.max_floor and floor not in self.pending_requests:
                self.pending_requests.append(floor)

    def step(self) -> None:
        """Execute one step of the elevator state machine."""
        with self._lock:
            self._state.handle(self)
            self.display.update(self.current_floor, self.direction)

    def is_idle(self) -> bool:
        return isinstance(self._state, IdleState) and not self.pending_requests

    def log(self, msg: str) -> None:
        print(f"    [Elevator-{self.elevator_id}] {msg}")

    def status(self) -> str:
        return (f"Elevator-{self.elevator_id}: Floor={self.current_floor}, "
                f"State={self._state.name()}, Dir={self.direction.value}, "
                f"Queue={self.pending_requests}")
