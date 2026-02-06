"""
Card entity for the ATM system.
Represents a bank card with PIN validation and linked accounts.
"""

from typing import Optional

from enums import AccountType
from account import Account


class Card:
    """Represents a bank card that can be inserted into the ATM."""

    def __init__(self, card_number: str, pin: str, bank_name: str,
                 accounts: list[Account]):
        """
        Args:
            card_number: Full card number.
            pin: PIN code for authentication.
            bank_name: Issuing bank name.
            accounts: List of accounts linked to this card.
        """
        self.card_number = card_number
        self._pin = pin
        self.bank_name = bank_name
        self.accounts: dict[AccountType, Account] = {
            acc.account_type: acc for acc in accounts
        }

    def validate_pin(self, pin: str) -> bool:
        """Check if the provided PIN matches."""
        return self._pin == pin

    def get_account(self, account_type: AccountType) -> Optional[Account]:
        """Retrieve a linked account by type."""
        return self.accounts.get(account_type)

    def get_masked_number(self) -> str:
        """Return the card number with all but the last 4 digits masked."""
        return "****-****-****-" + self.card_number[-4:]
