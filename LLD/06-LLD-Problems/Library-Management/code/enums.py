"""Enums for the Library Management System."""

from enum import Enum


class BookStatus(Enum):
    """Status of a physical book copy."""
    AVAILABLE = "Available"
    CHECKED_OUT = "Checked Out"
    RESERVED = "Reserved"
    LOST = "Lost"


class AccountStatus(Enum):
    """Status of a library member account."""
    ACTIVE = "Active"
    SUSPENDED = "Suspended"
    CLOSED = "Closed"


class ReservationStatus(Enum):
    """Status of a book reservation."""
    WAITING = "Waiting"
    FULFILLED = "Fulfilled"
    CANCELLED = "Cancelled"
