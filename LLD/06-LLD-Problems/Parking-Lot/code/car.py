"""Car vehicle type for the Parking Lot system."""

from enums import VehicleType
from vehicle import Vehicle


class Car(Vehicle):
    """A car requires a Regular or Large parking spot."""

    def __init__(self, license_plate: str) -> None:
        super().__init__(license_plate, VehicleType.CAR)
