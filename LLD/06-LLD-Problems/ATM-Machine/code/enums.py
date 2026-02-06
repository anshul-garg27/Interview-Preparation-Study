"""
Enums for the ATM Machine system.
"""

from enum import Enum


class AccountType(Enum):
    """Type of bank account."""
    SAVINGS = "savings"
    CHECKING = "checking"


class TransactionType(Enum):
    """Type of ATM transaction."""
    WITHDRAWAL = "withdrawal"
    DEPOSIT = "deposit"
    BALANCE_INQUIRY = "balance_inquiry"
    TRANSFER = "transfer"


class TransactionStatus(Enum):
    """Status of a completed transaction."""
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
