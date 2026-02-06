"""
ATM class - Context for the State Pattern.
Delegates all user actions to the current state object.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from enums import AccountType
from state import ATMState
from idle_state import IdleState
from cash_dispenser import CashDispenser
from card import Card
from account import Account
from transaction import Transaction


class TransactionObserver(ABC):
    """Observer interface for transaction events."""

    @abstractmethod
    def on_transaction(self, transaction: Transaction) -> None:
        pass


class AuditLogger(TransactionObserver):
    """Logs every transaction for audit purposes."""

    def on_transaction(self, transaction: Transaction) -> None:
        print(f"  [AUDIT] {transaction.transaction_type.value.upper()} | "
              f"Account: {transaction.account.account_number} | "
              f"Amount: ${transaction.amount:.2f} | Status: {transaction.status.value}")


class ATMNotificationService(TransactionObserver):
    """Sends SMS notifications for successful transactions."""

    def on_transaction(self, transaction: Transaction) -> None:
        from enums import TransactionStatus
        if transaction.status == TransactionStatus.SUCCESS:
            print(f"  [NOTIFY] SMS sent: Your {transaction.transaction_type.value} "
                  f"of ${transaction.amount:.2f} was successful.")


class ATM:
    """
    ATM machine implementing the State Pattern.
    All user operations are delegated to the current ATMState.
    """

    def __init__(self, atm_id: str, location: str):
        """
        Args:
            atm_id: Unique ATM identifier.
            location: Physical location description.
        """
        self.atm_id = atm_id
        self.location = location
        self.cash_dispenser = CashDispenser()
        self.state: ATMState = IdleState()
        self.current_card: Optional[Card] = None
        self.current_account: Optional[Account] = None
        self.transactions: list[Transaction] = []
        self._observers: list[TransactionObserver] = []

    def add_observer(self, observer: TransactionObserver) -> None:
        """Register a transaction observer."""
        self._observers.append(observer)

    def notify_observers(self, transaction: Transaction) -> None:
        """Notify all observers of a transaction event."""
        for observer in self._observers:
            observer.on_transaction(transaction)

    def set_state(self, state: ATMState) -> None:
        """Transition to a new ATM state."""
        self.state = state

    def insert_card(self, card: Card) -> str:
        """Insert a card into the ATM."""
        return self.state.insert_card(self, card)

    def enter_pin(self, pin: str) -> str:
        """Enter PIN for authentication."""
        return self.state.enter_pin(self, pin)

    def select_account(self, account_type: AccountType) -> str:
        """Select an account type for transactions."""
        if self.current_card:
            acc = self.current_card.get_account(account_type)
            if acc:
                self.current_account = acc
                return f"Selected {account_type.value} account: {acc.account_number}"
        return "Account not found."

    def check_balance(self) -> str:
        """Check the balance of the selected account."""
        return self.state.check_balance(self)

    def withdraw(self, amount: int) -> str:
        """Withdraw cash from the selected account."""
        return self.state.withdraw(self, amount)

    def deposit(self, amount: float) -> str:
        """Deposit cash into the selected account."""
        return self.state.deposit(self, amount)

    def transfer(self, target: Account, amount: float) -> str:
        """Transfer money to another account."""
        return self.state.transfer(self, target, amount)

    def eject_card(self) -> str:
        """Eject the card and return to idle state."""
        return self.state.eject_card(self)
