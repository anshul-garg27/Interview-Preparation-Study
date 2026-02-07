"""Enumerations for the Pub-Sub messaging system."""

from enum import Enum


class Priority(Enum):
    """Message priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3

    def __ge__(self, other: "Priority") -> bool:
        return self.value >= other.value

    def __gt__(self, other: "Priority") -> bool:
        return self.value > other.value

    def __le__(self, other: "Priority") -> bool:
        return self.value <= other.value

    def __lt__(self, other: "Priority") -> bool:
        return self.value < other.value


class MessageStatus(Enum):
    """Status of a message delivery."""
    PENDING = "PENDING"
    DELIVERED = "DELIVERED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    FAILED = "FAILED"
