"""
IdleState - ATM is waiting for a card to be inserted.
Only insert_card is a valid action; everything else returns an error message.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from state import ATMState

if TYPE_CHECKING:
    from atm import ATM
    from card import Card
    from account import Account


class IdleState(ATMState):
    """ATM is idle and waiting for a card."""

    def insert_card(self, atm: ATM, card: Card) -> str:
        from card_inserted_state import CardInsertedState
        atm.current_card = card
        atm.set_state(CardInsertedState())
        return f"Card {card.get_masked_number()} inserted. Please enter your PIN."

    def enter_pin(self, atm: ATM, pin: str) -> str:
        return "Please insert your card first."

    def check_balance(self, atm: ATM) -> str:
        return "Please insert your card first."

    def withdraw(self, atm: ATM, amount: int) -> str:
        return "Please insert your card first."

    def deposit(self, atm: ATM, amount: float) -> str:
        return "Please insert your card first."

    def transfer(self, atm: ATM, target: Account, amount: float) -> str:
        return "Please insert your card first."

    def eject_card(self, atm: ATM) -> str:
        return "No card inserted."
