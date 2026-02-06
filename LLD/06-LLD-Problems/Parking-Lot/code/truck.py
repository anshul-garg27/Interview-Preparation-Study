"""Truck vehicle type for the Parking Lot system."""

from enums import VehicleType
from vehicle import Vehicle


class Truck(Vehicle):
    """A truck requires a Large parking spot only."""

    def __init__(self, license_plate: str) -> None:
        super().__init__(license_plate, VehicleType.TRUCK)
