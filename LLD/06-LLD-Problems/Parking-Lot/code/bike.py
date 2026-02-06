"""Bike (motorcycle) vehicle type for the Parking Lot system."""

from enums import VehicleType
from vehicle import Vehicle


class Bike(Vehicle):
    """A motorcycle can fit in Compact, Regular, or Large spots."""

    def __init__(self, license_plate: str) -> None:
        super().__init__(license_plate, VehicleType.MOTORCYCLE)
