"""Enumerations for the Bowling Alley system."""

from enum import Enum


class LaneStatus(Enum):
    """Status of a bowling lane."""
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"


class FrameType(Enum):
    """Type of a bowling frame based on pins knocked down."""
    STRIKE = "STRIKE"
    SPARE = "SPARE"
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"


class GameStatus(Enum):
    """Status of a bowling game."""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
