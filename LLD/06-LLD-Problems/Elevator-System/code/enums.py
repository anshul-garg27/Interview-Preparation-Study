"""
Enums for the Elevator System.
Defines direction, elevator state names, and door state.
"""

from enum import Enum


class Direction(Enum):
    """Direction of elevator movement."""
    UP = "UP"
    DOWN = "DOWN"
    IDLE = "IDLE"


class ElevatorStateName(Enum):
    """Named states for the elevator state machine."""
    IDLE = "IDLE"
    MOVING_UP = "MOVING_UP"
    MOVING_DOWN = "MOVING_DOWN"
    DOOR_OPEN = "DOOR_OPEN"


class DoorState(Enum):
    """Physical state of the elevator door."""
    OPEN = "OPEN"
    CLOSED = "CLOSED"
