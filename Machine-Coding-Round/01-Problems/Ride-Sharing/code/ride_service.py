"""Ride Service - Singleton orchestrator for the ride-sharing system."""

from typing import Dict, List, Optional

from enums import VehicleType, RideStatus
from location import Location
from vehicle import Vehicle
from rider import Rider
from driver import Driver
from ride import Ride
from fare_calculator import get_fare_calculator
from driver_matcher import DriverMatcher
from rating_service import RatingService


class RideService:
    """Singleton service that orchestrates all ride-sharing operations.

    Manages driver/rider registration, ride lifecycle, fare calculation,
    driver matching, and ratings.
    """

    _instance: Optional["RideService"] = None

    def __new__(cls) -> "RideService":
        """Ensure only one instance of RideService exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        """Initialize the RideService (only once due to Singleton)."""
        if self._initialized:
            return
        self._initialized = True
        self._drivers: Dict[str, Driver] = {}
        self._riders: Dict[str, Rider] = {}
        self._rides: Dict[str, Ride] = {}
        self._matcher = DriverMatcher(max_radius_km=15.0)
        self._rating_service = RatingService()

    @classmethod
    def reset(cls) -> None:
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None

    def register_rider(self, name: str, phone: str, location: Location) -> Rider:
        """Register a new rider in the system.

        Args:
            name: Rider's name.
            phone: Rider's phone number.
            location: Rider's current location.

        Returns:
            The newly registered Rider.
        """
        rider = Rider(name, phone, location)
        self._riders[rider.rider_id] = rider
        return rider

    def register_driver(
        self, name: str, phone: str, vehicle: Vehicle, location: Location
    ) -> Driver:
        """Register a new driver in the system.

        Args:
            name: Driver's name.
            phone: Driver's phone number.
            vehicle: Driver's vehicle.
            location: Driver's current location.

        Returns:
            The newly registered Driver.
        """
        driver = Driver(name, phone, vehicle, location)
        self._drivers[driver.driver_id] = driver
        return driver

    def request_ride(
        self,
        rider: Rider,
        source: Location,
        destination: Location,
        vehicle_type: VehicleType,
    ) -> Ride:
        """Request a new ride for a rider.

        Args:
            rider: The rider requesting the ride.
            source: Pickup location.
            destination: Drop-off location.
            vehicle_type: Preferred vehicle type.

        Returns:
            The created Ride object.

        Raises:
            ValueError: If rider already has an active ride or no driver found.
        """
        if rider.has_active_ride():
            raise ValueError(f"Rider {rider.name} already has an active ride.")

        driver = self._matcher.find_nearest_driver(
            source, list(self._drivers.values()), vehicle_type
        )
        if driver is None:
            raise ValueError(
                f"No available {vehicle_type.value} driver within radius."
            )

        ride = Ride(rider, source, destination)
        ride.assign_driver(driver)

        fare_calc = get_fare_calculator(vehicle_type)
        ride.fare = fare_calc.calculate_fare(ride.distance)

        driver.is_available = False
        self._rides[ride.ride_id] = ride
        rider.ride_history.append(ride)
        driver.ride_history.append(ride)

        return ride

    def accept_ride(self, ride: Ride) -> None:
        """Driver accepts a ride request.

        Args:
            ride: The ride to accept.
        """
        ride.accept()

    def start_ride(self, ride: Ride) -> None:
        """Start a ride (driver has picked up rider).

        Args:
            ride: The ride to start.
        """
        ride.start()

    def complete_ride(self, ride: Ride) -> None:
        """Complete a ride (rider has been dropped off).

        Args:
            ride: The ride to complete.
        """
        ride.complete()

    def cancel_ride(self, ride: Ride) -> None:
        """Cancel a ride.

        Args:
            ride: The ride to cancel.
        """
        ride.cancel()

    def rate_driver(self, ride: Ride, rating: int) -> None:
        """Rate the driver of a completed ride.

        Args:
            ride: The completed ride.
            rating: Rating value (1-5).
        """
        self._rating_service.rate_driver(ride, rating)

    def rate_rider(self, ride: Ride, rating: int) -> None:
        """Rate the rider of a completed ride.

        Args:
            ride: The completed ride.
            rating: Rating value (1-5).
        """
        self._rating_service.rate_rider(ride, rating)

    def get_ride_history(self, rider: Rider) -> List[Ride]:
        """Get ride history for a rider."""
        return rider.ride_history

    def get_driver_history(self, driver: Driver) -> List[Ride]:
        """Get ride history for a driver."""
        return driver.ride_history
