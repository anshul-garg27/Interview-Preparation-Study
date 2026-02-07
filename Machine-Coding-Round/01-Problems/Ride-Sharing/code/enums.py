"""Enumerations for the Ride-Sharing system."""

from enum import Enum


class VehicleType(Enum):
    """Types of vehicles available for rides."""
    AUTO = "Auto"
    MINI = "Mini"
    SEDAN = "Sedan"


class RideStatus(Enum):
    """Lifecycle states of a ride."""
    REQUESTED = "REQUESTED"
    ACCEPTED = "ACCEPTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Rating(Enum):
    """Valid rating values (1-5 stars)."""
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    @classmethod
    def from_int(cls, value: int) -> "Rating":
        """Convert an integer to a Rating enum value."""
        for rating in cls:
            if rating.value == value:
                return rating
        raise ValueError(f"Invalid rating: {value}. Must be between 1 and 5.")
