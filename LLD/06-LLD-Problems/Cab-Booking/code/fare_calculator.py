"""Strategy Pattern: Fare calculators for different vehicle types."""

from abc import ABC, abstractmethod
from enums import VehicleType

MINIMUM_FARE = {
    VehicleType.AUTO: 30, VehicleType.MINI: 50,
    VehicleType.SEDAN: 80, VehicleType.SUV: 100, VehicleType.PREMIUM: 150,
}


class FareCalculator(ABC):
    """Abstract fare calculation strategy."""

    @abstractmethod
    def calculate(self, distance_km: float, surge: float) -> float:
        pass


class AutoFare(FareCalculator):
    """Fare strategy for Auto rickshaws: Rs 8/km."""

    def calculate(self, distance_km: float, surge: float) -> float:
        return max(8 * distance_km * surge, MINIMUM_FARE[VehicleType.AUTO])


class MiniFare(FareCalculator):
    """Fare strategy for Mini cabs: Rs 10/km."""

    def calculate(self, distance_km: float, surge: float) -> float:
        return max(10 * distance_km * surge, MINIMUM_FARE[VehicleType.MINI])


class SedanFare(FareCalculator):
    """Fare strategy for Sedan cabs: Rs 14/km."""

    def calculate(self, distance_km: float, surge: float) -> float:
        return max(14 * distance_km * surge, MINIMUM_FARE[VehicleType.SEDAN])


class SUVFare(FareCalculator):
    """Fare strategy for SUV cabs: Rs 18/km."""

    def calculate(self, distance_km: float, surge: float) -> float:
        return max(18 * distance_km * surge, MINIMUM_FARE[VehicleType.SUV])
