"""Driver matching logic to find the nearest available driver."""

from typing import List, Optional

from enums import VehicleType
from location import Location
from driver import Driver


class DriverMatcher:
    """Matches riders with the nearest available driver.

    Finds the closest driver within a configurable radius who is
    available and optionally matches the requested vehicle type.

    Attributes:
        max_radius_km: Maximum search radius in kilometers.
    """

    def __init__(self, max_radius_km: float = 10.0) -> None:
        """Initialize the DriverMatcher.

        Args:
            max_radius_km: Maximum radius to search for drivers (default 10 km).
        """
        self.max_radius_km = max_radius_km

    def find_nearest_driver(
        self,
        location: Location,
        drivers: List[Driver],
        vehicle_type: Optional[VehicleType] = None,
    ) -> Optional[Driver]:
        """Find the nearest available driver to a given location.

        Args:
            location: The rider's current location.
            drivers: List of all registered drivers.
            vehicle_type: Optional vehicle type filter.

        Returns:
            The nearest available Driver, or None if no driver found.
        """
        nearest_driver: Optional[Driver] = None
        min_distance = float("inf")

        for driver in drivers:
            if not driver.is_available:
                continue
            if vehicle_type and driver.vehicle.vehicle_type != vehicle_type:
                continue

            distance = location.distance_to(driver.location)
            if distance <= self.max_radius_km and distance < min_distance:
                min_distance = distance
                nearest_driver = driver

        return nearest_driver

    def find_drivers_in_radius(
        self,
        location: Location,
        drivers: List[Driver],
        radius_km: Optional[float] = None,
    ) -> List[tuple]:
        """Find all available drivers within radius, sorted by distance.

        Args:
            location: The search center location.
            drivers: List of all registered drivers.
            radius_km: Search radius (defaults to max_radius_km).

        Returns:
            List of (driver, distance) tuples sorted by distance.
        """
        radius = radius_km or self.max_radius_km
        result = []

        for driver in drivers:
            if not driver.is_available:
                continue
            distance = location.distance_to(driver.location)
            if distance <= radius:
                result.append((driver, distance))

        result.sort(key=lambda x: x[1])
        return result
