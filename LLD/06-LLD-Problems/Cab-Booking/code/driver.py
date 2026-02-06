"""Driver class for the Cab Booking System."""

from enums import DriverStatus
from location import Location
from vehicle import Vehicle
from rating import Rating


class Driver:
    """A driver who accepts and completes rides."""

    def __init__(self, driver_id: str, name: str, phone: str,
                 vehicle: Vehicle, location: Location, is_available: bool = True):
        self.driver_id = driver_id
        self.name = name
        self.phone = phone
        self.vehicle = vehicle
        self.location = location
        self.status = DriverStatus.AVAILABLE if is_available else DriverStatus.OFFLINE
        self.rating = Rating()
        self.total_rides = 0
        self.total_earnings = 0.0

    def accept_ride(self) -> None:
        """Mark driver as on a ride."""
        self.status = DriverStatus.ON_RIDE

    def complete_ride(self, earnings: float, new_location: Location) -> None:
        """Complete ride, update stats, and become available."""
        self.status = DriverStatus.AVAILABLE
        self.total_rides += 1
        self.total_earnings += earnings
        self.location = new_location

    def go_offline(self) -> None:
        self.status = DriverStatus.OFFLINE

    def __repr__(self) -> str:
        return (f"Driver({self.name}, {self.vehicle.vehicle_type.value}, "
                f"Rating={self.rating.average:.1f}, Status={self.status.value})")
