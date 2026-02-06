"""
Bank Account entity for the ATM system.
Supports debit, credit, balance inquiry, and daily withdrawal limits.
"""

from enums import AccountType


class Account:
    """Represents a bank account linked to a card."""

    def __init__(self, account_number: str, account_type: AccountType,
                 balance: float, daily_limit: float = 1000.0):
        """
        Args:
            account_number: Unique identifier for the account.
            account_type: SAVINGS or CHECKING.
            balance: Initial account balance.
            daily_limit: Maximum withdrawal amount per day.
        """
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.daily_withdrawal_limit = daily_limit
        self.withdrawn_today: float = 0.0

    def debit(self, amount: float) -> bool:
        """
        Withdraw amount from account.

        Returns:
            True if successful, False if insufficient funds or exceeds daily limit.
        """
        if amount > self.balance:
            return False
        if self.withdrawn_today + amount > self.daily_withdrawal_limit:
            return False
        self.balance -= amount
        self.withdrawn_today += amount
        return True

    def credit(self, amount: float) -> None:
        """Deposit amount into the account."""
        self.balance += amount

    def get_balance(self) -> float:
        """Return the current balance."""
        return self.balance
