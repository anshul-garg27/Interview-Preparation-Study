"""Enums for the Cab Booking System."""

from enum import Enum


class VehicleType(Enum):
    """Types of vehicles available for rides."""
    AUTO = "Auto"
    MINI = "Mini"
    SEDAN = "Sedan"
    SUV = "SUV"
    PREMIUM = "Premium"


class RideStatus(Enum):
    """State machine states for a ride lifecycle."""
    REQUESTED = "Requested"
    ACCEPTED = "Accepted"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"


class DriverStatus(Enum):
    """Availability states for a driver."""
    AVAILABLE = "Available"
    ON_RIDE = "On Ride"
    OFFLINE = "Offline"


class PaymentMethod(Enum):
    """Supported payment methods."""
    CASH = "Cash"
    UPI = "UPI"
    CARD = "Card"
    WALLET = "Wallet"
