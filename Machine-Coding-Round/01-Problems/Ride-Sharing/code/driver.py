"""Driver class representing a person who provides rides."""

import uuid
from typing import List, TYPE_CHECKING

from location import Location
from vehicle import Vehicle

if TYPE_CHECKING:
    from ride import Ride


class Driver:
    """Represents a driver in the ride-sharing system.

    Attributes:
        driver_id: Unique identifier for the driver.
        name: Full name of the driver.
        phone: Phone number of the driver.
        vehicle: The vehicle the driver operates.
        location: Current geographical location.
        is_available: Whether the driver is accepting rides.
        ride_history: List of all rides completed.
        ratings: List of ratings received from riders.
    """

    def __init__(
        self, name: str, phone: str, vehicle: Vehicle, location: Location
    ) -> None:
        """Initialize a Driver.

        Args:
            name: Driver's name.
            phone: Driver's phone number.
            vehicle: Driver's vehicle.
            location: Driver's current location.

        Raises:
            ValueError: If name or phone is empty.
        """
        if not name or not phone:
            raise ValueError("Name and phone are required.")
        self.driver_id: str = str(uuid.uuid4())[:8]
        self.name = name
        self.phone = phone
        self.vehicle = vehicle
        self.location = location
        self.is_available: bool = True
        self.ride_history: List["Ride"] = []
        self._ratings: List[int] = []

    @property
    def average_rating(self) -> float:
        """Calculate and return the average rating."""
        if not self._ratings:
            return 0.0
        return round(sum(self._ratings) / len(self._ratings), 1)

    def add_rating(self, rating: int) -> None:
        """Add a rating to this driver.

        Args:
            rating: Rating value between 1 and 5.

        Raises:
            ValueError: If rating is not between 1 and 5.
        """
        if not 1 <= rating <= 5:
            raise ValueError(f"Rating must be between 1 and 5, got {rating}")
        self._ratings.append(rating)

    def toggle_availability(self) -> None:
        """Toggle the driver's availability status."""
        self.is_available = not self.is_available

    def __str__(self) -> str:
        return f"Driver({self.name}, {self.vehicle.vehicle_type.value})"

    def __repr__(self) -> str:
        return f"Driver(id={self.driver_id}, name={self.name})"
