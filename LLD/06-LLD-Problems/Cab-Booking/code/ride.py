"""Ride class with state machine lifecycle."""

import threading
from typing import Optional
from datetime import datetime

from enums import RideStatus, DriverStatus, VehicleType
from location import Location
from rider import Rider
from driver import Driver


class Ride:
    """A ride request with full lifecycle state management."""

    _counter = 0
    _lock = threading.Lock()

    def __init__(self, rider: Rider, pickup: Location,
                 dropoff: Location, vehicle_type: VehicleType):
        with Ride._lock:
            Ride._counter += 1
            self.ride_id = f"RIDE-{Ride._counter:04d}"
        self.rider = rider
        self.pickup = pickup
        self.dropoff = dropoff
        self.vehicle_type = vehicle_type
        self.driver: Optional[Driver] = None
        self.status = RideStatus.REQUESTED
        self.distance = pickup.distance_to(dropoff)
        self.fare = 0.0
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None

    def accept(self, driver: Driver) -> bool:
        """Driver accepts the ride request."""
        if self.status != RideStatus.REQUESTED:
            print(f"    [Error] Ride {self.ride_id} cannot be accepted")
            return False
        self.driver = driver
        self.status = RideStatus.ACCEPTED
        driver.accept_ride()
        print(f"    [Accepted] {driver.name} accepted {self.ride_id}")
        return True

    def start(self) -> bool:
        """Begin the ride after driver reaches pickup."""
        if self.status != RideStatus.ACCEPTED:
            return False
        self.status = RideStatus.IN_PROGRESS
        self.start_time = datetime.now()
        print(f"    [Started] {self.ride_id}: {self.pickup} -> {self.dropoff} "
              f"({self.distance:.1f} km)")
        return True

    def complete(self, fare: float) -> bool:
        """Complete ride with calculated fare."""
        if self.status != RideStatus.IN_PROGRESS:
            return False
        self.status = RideStatus.COMPLETED
        self.fare = fare
        self.end_time = datetime.now()
        self.driver.complete_ride(fare, self.dropoff)
        self.rider.ride_history.append(self)
        print(f"    [Completed] {self.ride_id}: Fare=${fare:.2f}")
        return True

    def cancel(self, reason: str = "") -> bool:
        """Cancel the ride at any non-terminal state."""
        if self.status in (RideStatus.COMPLETED, RideStatus.CANCELLED):
            return False
        if self.driver:
            self.driver.status = DriverStatus.AVAILABLE
        self.status = RideStatus.CANCELLED
        print(f"    [Cancelled] {self.ride_id}: {reason}")
        return True

    def __repr__(self) -> str:
        return (f"Ride({self.ride_id}, {self.rider.name}, "
                f"{self.pickup}->{self.dropoff}, "
                f"{self.distance:.1f}km, {self.status.value})")
