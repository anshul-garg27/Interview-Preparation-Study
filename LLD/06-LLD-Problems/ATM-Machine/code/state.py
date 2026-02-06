"""
Abstract ATM State interface (State Pattern).
Defines all actions available on the ATM; concrete states decide what is valid.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from atm import ATM
    from card import Card
    from account import Account


class ATMState(ABC):
    """Abstract base class for ATM states."""

    @abstractmethod
    def insert_card(self, atm: ATM, card: Card) -> str:
        pass

    @abstractmethod
    def enter_pin(self, atm: ATM, pin: str) -> str:
        pass

    @abstractmethod
    def check_balance(self, atm: ATM) -> str:
        pass

    @abstractmethod
    def withdraw(self, atm: ATM, amount: int) -> str:
        pass

    @abstractmethod
    def deposit(self, atm: ATM, amount: float) -> str:
        pass

    @abstractmethod
    def transfer(self, atm: ATM, target: Account, amount: float) -> str:
        pass

    @abstractmethod
    def eject_card(self, atm: ATM) -> str:
        pass
