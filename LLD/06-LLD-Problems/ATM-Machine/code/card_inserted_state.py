"""
CardInsertedState - Card has been inserted, waiting for PIN verification.
Allows up to 3 PIN attempts before retaining the card.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from state import ATMState
from enums import AccountType

if TYPE_CHECKING:
    from atm import ATM
    from card import Card
    from account import Account


class CardInsertedState(ATMState):
    """ATM has a card inserted and is waiting for PIN."""

    def __init__(self):
        self.pin_attempts: int = 0
        self.max_attempts: int = 3

    def insert_card(self, atm: ATM, card: Card) -> str:
        return "Card already inserted. Please enter your PIN."

    def enter_pin(self, atm: ATM, pin: str) -> str:
        from authenticated_state import AuthenticatedState
        from idle_state import IdleState

        if atm.current_card.validate_pin(pin):
            atm.current_account = atm.current_card.get_account(AccountType.SAVINGS)
            atm.set_state(AuthenticatedState())
            return "PIN verified. Welcome! Select a transaction."
        else:
            self.pin_attempts += 1
            remaining = self.max_attempts - self.pin_attempts
            if remaining <= 0:
                atm.current_card = None
                atm.current_account = None
                atm.set_state(IdleState())
                return "Too many failed attempts. Card has been retained. Contact your bank."
            return f"Incorrect PIN. {remaining} attempt(s) remaining."

    def check_balance(self, atm: ATM) -> str:
        return "Please enter your PIN first."

    def withdraw(self, atm: ATM, amount: int) -> str:
        return "Please enter your PIN first."

    def deposit(self, atm: ATM, amount: float) -> str:
        return "Please enter your PIN first."

    def transfer(self, atm: ATM, target: Account, amount: float) -> str:
        return "Please enter your PIN first."

    def eject_card(self, atm: ATM) -> str:
        from idle_state import IdleState
        atm.current_card = None
        atm.set_state(IdleState())
        return "Card ejected."
