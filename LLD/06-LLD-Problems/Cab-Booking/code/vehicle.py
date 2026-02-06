"""Vehicle class for the Cab Booking System."""

from enums import VehicleType


class Vehicle:
    """Represents a driver's vehicle."""

    def __init__(self, vehicle_id: str, vehicle_type: VehicleType,
                 make: str, model: str, license_plate: str):
        self.vehicle_id = vehicle_id
        self.vehicle_type = vehicle_type
        self.make = make
        self.model = model
        self.license_plate = license_plate

    def __repr__(self) -> str:
        return f"{self.make} {self.model} ({self.vehicle_type.value}, {self.license_plate})"
