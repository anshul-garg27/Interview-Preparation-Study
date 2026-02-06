"""Driver matching service - finds nearest available driver."""

from typing import Optional, Dict
from enums import DriverStatus, VehicleType
from location import Location
from driver import Driver


class DriverMatcher:
    """Finds the nearest available driver for a ride request."""

    def __init__(self, max_distance_km: float = 10.0):
        self.max_distance_km = max_distance_km

    def find_nearest(self, drivers: Dict[str, Driver],
                     location: Location,
                     vehicle_type: VehicleType) -> Optional[Driver]:
        """Return the closest available driver of the requested type."""
        best, best_dist = None, float("inf")
        for driver in drivers.values():
            if (driver.status == DriverStatus.AVAILABLE and
                    driver.vehicle.vehicle_type == vehicle_type):
                dist = driver.location.distance_to(location)
                if dist < best_dist and dist <= self.max_distance_km:
                    best_dist = dist
                    best = driver
        return best
