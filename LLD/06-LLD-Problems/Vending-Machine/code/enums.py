"""Enums for Vending Machine denominations."""

from enum import Enum


class Coin(Enum):
    """Coins accepted by the vending machine."""
    PENNY = 1
    NICKEL = 5
    DIME = 10
    QUARTER = 25


class Note(Enum):
    """Notes accepted by the vending machine."""
    ONE = 1
    FIVE = 5
    TEN = 10
    TWENTY = 20
    FIFTY = 50
    HUNDRED = 100
