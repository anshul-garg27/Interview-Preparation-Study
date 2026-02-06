"""
Enums for the Notification System.
"""

from enum import Enum


class Priority(Enum):
    """Notification priority level."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class ChannelType(Enum):
    """Supported notification channels."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"
    SLACK = "slack"


class NotificationStatus(Enum):
    """Status of a notification."""
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RATE_LIMITED = "rate_limited"
    SKIPPED = "skipped"
