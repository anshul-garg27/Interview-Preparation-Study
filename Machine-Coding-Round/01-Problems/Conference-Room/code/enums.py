"""Enumerations for the Conference Room Booking System."""

from enum import Enum


class RoomSize(Enum):
    SMALL = "SMALL"       # 1-4 people
    MEDIUM = "MEDIUM"     # 5-10 people
    LARGE = "LARGE"       # 11-20 people


class Amenity(Enum):
    WHITEBOARD = "WHITEBOARD"
    PROJECTOR = "PROJECTOR"
    VIDEO_CONFERENCING = "VIDEO_CONFERENCING"
    PHONE = "PHONE"


class BookingStatus(Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
