"""Vehicle class representing a driver's vehicle."""

from enums import VehicleType


class Vehicle:
    """Represents a vehicle with type, make, model, and license plate.

    Attributes:
        vehicle_type: The type of vehicle (AUTO, MINI, SEDAN).
        make: The manufacturer of the vehicle.
        model: The model name of the vehicle.
        license_plate: The vehicle's license plate number.
    """

    def __init__(
        self,
        vehicle_type: VehicleType,
        make: str,
        model: str,
        license_plate: str,
    ) -> None:
        """Initialize a Vehicle.

        Args:
            vehicle_type: Type of vehicle.
            make: Manufacturer name.
            model: Model name.
            license_plate: License plate number.

        Raises:
            ValueError: If any required field is empty.
        """
        if not make or not model or not license_plate:
            raise ValueError("Make, model, and license plate are required.")
        self.vehicle_type = vehicle_type
        self.make = make
        self.model = model
        self.license_plate = license_plate

    def __str__(self) -> str:
        return f"{self.vehicle_type.value} - {self.make} {self.model} ({self.license_plate})"

    def __repr__(self) -> str:
        return f"Vehicle({self.vehicle_type.value}, {self.make}, {self.model})"
