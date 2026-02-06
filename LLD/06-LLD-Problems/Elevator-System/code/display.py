"""
Display class for the Elevator System.
Shows current floor and direction inside the elevator.
"""

from enums import Direction


class Display:
    """Display panel inside an elevator showing current floor."""

    def __init__(self, elevator_id: int) -> None:
        self._elevator_id = elevator_id
        self._current_floor: int = 0
        self._direction: Direction = Direction.IDLE

    def update(self, floor: int, direction: Direction) -> None:
        """Update the display with current floor and direction."""
        self._current_floor = floor
        self._direction = direction

    def show(self) -> str:
        """Return a string representation of the display."""
        arrow = {"UP": "^", "DOWN": "v", "IDLE": "-"}[self._direction.value]
        return f"[{arrow} Floor {self._current_floor}]"
