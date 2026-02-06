"""Enumerations for the Digital Wallet System."""

from enum import Enum


class TransactionType(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TransactionCategory(Enum):
    TOP_UP = "TOP_UP"
    TRANSFER_IN = "TRANSFER_IN"
    TRANSFER_OUT = "TRANSFER_OUT"
    WITHDRAWAL = "WITHDRAWAL"
    CASHBACK = "CASHBACK"
    REFERRAL_BONUS = "REFERRAL_BONUS"


class WalletStatus(Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"


class TransactionStatus(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
