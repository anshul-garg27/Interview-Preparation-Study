"""
Door class for the Elevator System.
Manages the physical open/close state of an elevator door.
"""

from enums import DoorState


class Door:
    """Represents the elevator door with open/close operations."""

    def __init__(self, elevator_id: int) -> None:
        self._elevator_id = elevator_id
        self._state: DoorState = DoorState.CLOSED

    @property
    def state(self) -> DoorState:
        return self._state

    def open(self) -> None:
        """Open the door."""
        self._state = DoorState.OPEN

    def close(self) -> None:
        """Close the door."""
        self._state = DoorState.CLOSED

    def is_open(self) -> bool:
        return self._state == DoorState.OPEN
