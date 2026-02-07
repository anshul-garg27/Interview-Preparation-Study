"""Rider class representing a person who requests rides."""

import uuid
from typing import List, TYPE_CHECKING

from location import Location

if TYPE_CHECKING:
    from ride import Ride


class Rider:
    """Represents a rider in the ride-sharing system.

    Attributes:
        rider_id: Unique identifier for the rider.
        name: Full name of the rider.
        phone: Phone number of the rider.
        location: Current geographical location.
        ride_history: List of all rides taken.
        ratings: List of ratings received from drivers.
    """

    def __init__(self, name: str, phone: str, location: Location) -> None:
        """Initialize a Rider.

        Args:
            name: Rider's name.
            phone: Rider's phone number.
            location: Rider's current location.

        Raises:
            ValueError: If name or phone is empty.
        """
        if not name or not phone:
            raise ValueError("Name and phone are required.")
        self.rider_id: str = str(uuid.uuid4())[:8]
        self.name = name
        self.phone = phone
        self.location = location
        self.ride_history: List["Ride"] = []
        self._ratings: List[int] = []

    @property
    def average_rating(self) -> float:
        """Calculate and return the average rating."""
        if not self._ratings:
            return 0.0
        return round(sum(self._ratings) / len(self._ratings), 1)

    def add_rating(self, rating: int) -> None:
        """Add a rating to this rider.

        Args:
            rating: Rating value between 1 and 5.

        Raises:
            ValueError: If rating is not between 1 and 5.
        """
        if not 1 <= rating <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {rating}")
        self._ratings.append(rating)

    def has_active_ride(self) -> bool:
        """Check if rider currently has an active (non-completed/cancelled) ride."""
        from enums import RideStatus
        return any(
            r.status in (RideStatus.REQUESTED, RideStatus.ACCEPTED, RideStatus.IN_PROGRESS)
            for r in self.ride_history
        )

    def __str__(self) -> str:
        return f"Rider({self.name}, Phone: {self.phone})"

    def __repr__(self) -> str:
        return f"Rider(id={self.rider_id}, name={self.name})"
