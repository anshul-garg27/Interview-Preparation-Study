"""
Abstract Vehicle base class for the Parking Lot system.
All vehicle types (Car, Bike, Truck) inherit from this.
"""

from abc import ABC, abstractmethod

from enums import VehicleType


class Vehicle(ABC):
    """Base class for all vehicles entering the parking lot."""

    def __init__(self, license_plate: str, vehicle_type: VehicleType) -> None:
        self._license_plate = license_plate
        self._vehicle_type = vehicle_type

    @property
    def license_plate(self) -> str:
        return self._license_plate

    @property
    def vehicle_type(self) -> VehicleType:
        return self._vehicle_type

    def __repr__(self) -> str:
        return f"{self._vehicle_type.value}({self._license_plate})"
