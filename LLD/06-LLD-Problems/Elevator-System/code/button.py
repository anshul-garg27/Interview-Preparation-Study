"""
Button classes for the Elevator System.
ExternalButton (hall call) and InternalButton (cabin panel).
"""

from enums import Direction


class ExternalButton:
    """Hall call button on a floor - has UP and DOWN."""

    def __init__(self, floor: int) -> None:
        self._floor = floor

    def press_up(self) -> tuple[int, Direction]:
        """Press the UP button on this floor."""
        print(f"    [Button] Floor {self._floor}: UP pressed")
        return self._floor, Direction.UP

    def press_down(self) -> tuple[int, Direction]:
        """Press the DOWN button on this floor."""
        print(f"    [Button] Floor {self._floor}: DOWN pressed")
        return self._floor, Direction.DOWN


class InternalButton:
    """Button panel inside an elevator cabin."""

    def __init__(self, elevator_id: int) -> None:
        self._elevator_id = elevator_id

    def press_floor(self, floor: int) -> int:
        """Press a destination floor button inside the elevator."""
        print(f"    [Button] Elevator-{self._elevator_id}: Floor {floor} pressed")
        return floor
