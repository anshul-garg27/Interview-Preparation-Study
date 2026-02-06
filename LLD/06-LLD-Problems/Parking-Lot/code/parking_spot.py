"""
ParkingSpot class for the Parking Lot system.
Each spot has an ID, type, and tracks the parked vehicle.
"""

from enums import SpotType
from vehicle import Vehicle


class ParkingSpot:
    """Represents a single parking spot on a floor."""

    def __init__(self, spot_id: str, spot_type: SpotType, floor_number: int) -> None:
        self._spot_id = spot_id
        self._spot_type = spot_type
        self._floor_number = floor_number
        self._vehicle: Vehicle | None = None
        self._is_available: bool = True

    @property
    def spot_id(self) -> str:
        return self._spot_id

    @property
    def spot_type(self) -> SpotType:
        return self._spot_type

    @property
    def is_available(self) -> bool:
        return self._is_available

    @property
    def vehicle(self) -> Vehicle | None:
        return self._vehicle

    def assign_vehicle(self, vehicle: Vehicle) -> None:
        """Park a vehicle in this spot."""
        self._vehicle = vehicle
        self._is_available = False

    def remove_vehicle(self) -> None:
        """Free this spot by removing the vehicle."""
        self._vehicle = None
        self._is_available = True

    def __repr__(self) -> str:
        status = "Free" if self._is_available else f"Occupied({self._vehicle})"
        return f"Spot({self._spot_id}, {self._spot_type.value}, {status})"
