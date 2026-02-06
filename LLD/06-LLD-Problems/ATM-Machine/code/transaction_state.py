"""
TransactionState - ATM is actively processing a transaction.
Used when a multi-step transaction is in progress (e.g., counting cash).
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from state import ATMState

if TYPE_CHECKING:
    from atm import ATM
    from card import Card
    from account import Account


class TransactionState(ATMState):
    """ATM is currently processing a transaction."""

    def insert_card(self, atm: ATM, card: Card) -> str:
        return "Transaction in progress. Please wait."

    def enter_pin(self, atm: ATM, pin: str) -> str:
        return "Transaction in progress. Please wait."

    def check_balance(self, atm: ATM) -> str:
        return "Transaction in progress. Please wait."

    def withdraw(self, atm: ATM, amount: int) -> str:
        return "Transaction in progress. Please wait."

    def deposit(self, atm: ATM, amount: float) -> str:
        return "Transaction in progress. Please wait."

    def transfer(self, atm: ATM, target: Account, amount: float) -> str:
        return "Transaction in progress. Please wait."

    def eject_card(self, atm: ATM) -> str:
        return "Cannot eject card during a transaction. Please wait."
