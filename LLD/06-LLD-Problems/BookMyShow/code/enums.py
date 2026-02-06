"""Enums for BookMyShow booking system."""

from enum import Enum


class SeatType(Enum):
    """Type of seat in a cinema hall."""
    REGULAR = "Regular"
    PREMIUM = "Premium"
    VIP = "VIP"


class BookingStatus(Enum):
    """Status of a booking."""
    PENDING = "Pending"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"


class PaymentStatus(Enum):
    """Status of a payment transaction."""
    PENDING = "Pending"
    SUCCESS = "Success"
    FAILED = "Failed"


class SeatStatus(Enum):
    """Availability status of a seat for a show."""
    AVAILABLE = "Available"
    LOCKED = "Locked"
    BOOKED = "Booked"
