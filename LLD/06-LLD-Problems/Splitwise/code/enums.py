"""
Enums for the Splitwise system.
"""

from enum import Enum


class SplitType(Enum):
    """Type of expense split."""
    EQUAL = "equal"
    EXACT = "exact"
    PERCENTAGE = "percentage"
