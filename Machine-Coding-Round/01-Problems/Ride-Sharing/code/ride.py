"""Ride class representing a single ride from source to destination."""

import uuid
from datetime import datetime
from typing import Optional

from enums import RideStatus
from location import Location
from rider import Rider
from driver import Driver


class Ride:
    """Represents a ride in the system with full lifecycle management.

    Attributes:
        ride_id: Unique identifier for the ride.
        rider: The rider who requested the ride.
        driver: The driver assigned to the ride (None until matched).
        source: Starting location of the ride.
        destination: Ending location of the ride.
        status: Current state of the ride.
        fare: Calculated fare for the ride.
        distance: Distance in km between source and destination.
        created_at: Timestamp when the ride was created.
    """

    def __init__(
        self,
        rider: Rider,
        source: Location,
        destination: Location,
    ) -> None:
        """Initialize a Ride.

        Args:
            rider: The rider requesting the ride.
            source: Pickup location.
            destination: Drop-off location.
        """
        self.ride_id: str = str(uuid.uuid4())[:8]
        self.rider = rider
        self.driver: Optional[Driver] = None
        self.source = source
        self.destination = destination
        self.status: RideStatus = RideStatus.REQUESTED
        self.fare: float = 0.0
        self.distance: float = source.distance_to(destination)
        self.created_at: datetime = datetime.now()

    def assign_driver(self, driver: Driver) -> None:
        """Assign a driver to this ride.

        Args:
            driver: The driver to assign.
        """
        self.driver = driver

    def accept(self) -> None:
        """Driver accepts the ride. Transition: REQUESTED -> ACCEPTED.

        Raises:
            ValueError: If ride is not in REQUESTED state.
        """
        if self.status != RideStatus.REQUESTED:
            raise ValueError(f"Cannot accept ride in {self.status.value} state.")
        self.status = RideStatus.ACCEPTED

    def start(self) -> None:
        """Start the ride. Transition: ACCEPTED -> IN_PROGRESS.

        Raises:
            ValueError: If ride is not in ACCEPTED state.
        """
        if self.status != RideStatus.ACCEPTED:
            raise ValueError(f"Cannot start ride in {self.status.value} state.")
        self.status = RideStatus.IN_PROGRESS

    def complete(self) -> None:
        """Complete the ride. Transition: IN_PROGRESS -> COMPLETED.

        Raises:
            ValueError: If ride is not in IN_PROGRESS state.
        """
        if self.status != RideStatus.IN_PROGRESS:
            raise ValueError(f"Cannot complete ride in {self.status.value} state.")
        self.status = RideStatus.COMPLETED
        if self.driver:
            self.driver.is_available = True

    def cancel(self) -> None:
        """Cancel the ride. Allowed from REQUESTED, ACCEPTED, or IN_PROGRESS.

        Raises:
            ValueError: If ride is already COMPLETED or CANCELLED.
        """
        if self.status in (RideStatus.COMPLETED, RideStatus.CANCELLED):
            raise ValueError(f"Cannot cancel ride in {self.status.value} state.")
        self.status = RideStatus.CANCELLED
        if self.driver:
            self.driver.is_available = True

    def __str__(self) -> str:
        driver_name = self.driver.name if self.driver else "Unassigned"
        return (
            f"Ride({self.ride_id}) | {self.rider.name} -> {driver_name} | "
            f"{self.status.value} | Rs {self.fare:.2f}"
        )
