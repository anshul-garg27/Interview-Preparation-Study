"""
Enums for the Parking Lot system.
Defines vehicle types, spot types, ticket status, and payment status.
"""

from enum import Enum


class VehicleType(Enum):
    """Types of vehicles that can park."""
    MOTORCYCLE = "Motorcycle"
    CAR = "Car"
    TRUCK = "Truck"


class SpotType(Enum):
    """Types of parking spots available."""
    COMPACT = "Compact"
    REGULAR = "Regular"
    LARGE = "Large"


class TicketStatus(Enum):
    """Lifecycle status of a parking ticket."""
    ACTIVE = "Active"
    PAID = "Paid"
    EXITED = "Exited"


class PaymentStatus(Enum):
    """Status of a payment transaction."""
    PENDING = "Pending"
    COMPLETED = "Completed"
    FAILED = "Failed"


# Mapping: which vehicle fits which spot type
VEHICLE_SPOT_MAP: dict[VehicleType, list[SpotType]] = {
    VehicleType.MOTORCYCLE: [SpotType.COMPACT, SpotType.REGULAR, SpotType.LARGE],
    VehicleType.CAR: [SpotType.REGULAR, SpotType.LARGE],
    VehicleType.TRUCK: [SpotType.LARGE],
}

# Hourly rate per spot type
RATE_PER_HOUR: dict[SpotType, int] = {
    SpotType.COMPACT: 10,
    SpotType.REGULAR: 20,
    SpotType.LARGE: 40,
}
