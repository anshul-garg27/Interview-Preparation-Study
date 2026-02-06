"""RideService (Singleton) - manages the full ride lifecycle."""

import threading
from enums import VehicleType
from location import Location
from rider import Rider
from driver import Driver
from ride import Ride
from fare_calculator import FareCalculator, MiniFare, SedanFare, SUVFare, AutoFare
from driver_matcher import DriverMatcher
from notification import RideNotification, RideNotificationService


FARE_MAP = {
    VehicleType.AUTO: AutoFare(), VehicleType.MINI: MiniFare(),
    VehicleType.SEDAN: SedanFare(), VehicleType.SUV: SUVFare(),
}


class RideService:
    """Singleton service orchestrating ride request, matching, and completion."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.drivers = {}
        self.riders = {}
        self.rides = []
        self.surge_multiplier = 1.0
        self._matcher = DriverMatcher()
        self._notifier = RideNotificationService()
        self._notifier.subscribe(RideNotification())
        self._initialized = True

    def register_driver(self, driver: Driver) -> None:
        self.drivers[driver.driver_id] = driver

    def register_rider(self, rider: Rider) -> None:
        self.riders[rider.rider_id] = rider

    def set_surge(self, multiplier: float) -> None:
        self.surge_multiplier = multiplier
        if multiplier > 1.0:
            print(f"\n  [Surge Pricing] {multiplier:.1f}x active!")

    def request_ride(self, rider: Rider, pickup: Location,
                     dropoff: Location, vehicle_type: VehicleType) -> Ride:
        """Full ride lifecycle: request -> match -> start -> complete."""
        print(f"\n  {'─'*55}")
        print(f"  {rider.name} requests {vehicle_type.value} ride: {pickup} -> {dropoff}")

        ride = Ride(rider, pickup, dropoff, vehicle_type)
        driver = self._matcher.find_nearest(self.drivers, pickup, vehicle_type)

        if not driver:
            print(f"    [No Driver] No {vehicle_type.value} available nearby")
            ride.cancel("No drivers available")
            return ride

        pickup_dist = driver.location.distance_to(pickup)
        print(f"    [Match] {driver.name} is {pickup_dist:.1f}km away")

        ride.accept(driver)
        ride.start()

        calculator = FARE_MAP.get(vehicle_type, MiniFare())
        fare = calculator.calculate(ride.distance, self.surge_multiplier)
        ride.complete(fare)

        self._notifier.notify_all(ride, f"Ride {ride.ride_id} completed, fare=${fare:.2f}")
        self.rides.append(ride)
        return ride

    def display_drivers(self) -> None:
        print(f"\n  {'='*60}")
        print(f"  Driver Dashboard")
        print(f"  {'='*60}")
        for d in self.drivers.values():
            print(f"    {d.name:12s} | {d.vehicle.vehicle_type.value:7s} | "
                  f"Rating: {d.rating.average:3.1f} ({d.rating.count} reviews) | "
                  f"Rides: {d.total_rides} | Earned: ${d.total_earnings:.2f} | "
                  f"{d.status.value}")
        print(f"  {'='*60}")
