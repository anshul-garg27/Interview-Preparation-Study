"""Fare calculation using the Strategy pattern.

Each vehicle type has its own fare calculation strategy with
different base fares, per-km rates, and minimum fares.
"""

from abc import ABC, abstractmethod

from enums import VehicleType


class FareCalculator(ABC):
    """Abstract base class for fare calculation strategies."""

    @abstractmethod
    def calculate_fare(self, distance_km: float) -> float:
        """Calculate fare based on distance.

        Args:
            distance_km: Distance of the ride in kilometers.

        Returns:
            Calculated fare amount.
        """
        pass


class AutoFareCalculator(FareCalculator):
    """Fare calculator for Auto rickshaw rides."""

    BASE_FARE = 25.0
    PER_KM_RATE = 8.0
    MIN_FARE = 30.0

    def calculate_fare(self, distance_km: float) -> float:
        """Calculate auto fare: Rs 25 base + Rs 8/km."""
        fare = self.BASE_FARE + (self.PER_KM_RATE * distance_km)
        return round(max(fare, self.MIN_FARE), 2)


class MiniFareCalculator(FareCalculator):
    """Fare calculator for Mini cab rides."""

    BASE_FARE = 50.0
    PER_KM_RATE = 12.0
    MIN_FARE = 60.0

    def calculate_fare(self, distance_km: float) -> float:
        """Calculate mini fare: Rs 50 base + Rs 12/km."""
        fare = self.BASE_FARE + (self.PER_KM_RATE * distance_km)
        return round(max(fare, self.MIN_FARE), 2)


class SedanFareCalculator(FareCalculator):
    """Fare calculator for Sedan rides."""

    BASE_FARE = 100.0
    PER_KM_RATE = 18.0
    MIN_FARE = 120.0

    def calculate_fare(self, distance_km: float) -> float:
        """Calculate sedan fare: Rs 100 base + Rs 18/km."""
        fare = self.BASE_FARE + (self.PER_KM_RATE * distance_km)
        return round(max(fare, self.MIN_FARE), 2)


def get_fare_calculator(vehicle_type: VehicleType) -> FareCalculator:
    """Factory method to get the appropriate fare calculator.

    Args:
        vehicle_type: The type of vehicle.

    Returns:
        The corresponding FareCalculator implementation.

    Raises:
        ValueError: If vehicle type is unknown.
    """
    calculators = {
        VehicleType.AUTO: AutoFareCalculator(),
        VehicleType.MINI: MiniFareCalculator(),
        VehicleType.SEDAN: SedanFareCalculator(),
    }
    calculator = calculators.get(vehicle_type)
    if calculator is None:
        raise ValueError(f"No fare calculator for vehicle type: {vehicle_type}")
    return calculator
