"""
AuthenticatedState - PIN verified, user can perform transactions.
Supports balance inquiry, withdrawal, deposit, transfer, and card ejection.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from state import ATMState
from enums import TransactionType, TransactionStatus
from transaction import Transaction

if TYPE_CHECKING:
    from atm import ATM
    from card import Card
    from account import Account


class AuthenticatedState(ATMState):
    """ATM user has been authenticated and can perform transactions."""

    def insert_card(self, atm: ATM, card: Card) -> str:
        return "Card already inserted. Please complete or cancel your session."

    def enter_pin(self, atm: ATM, pin: str) -> str:
        return "Already authenticated."

    def check_balance(self, atm: ATM) -> str:
        balance = atm.current_account.get_balance()
        txn = Transaction(TransactionType.BALANCE_INQUIRY, atm.current_account, 0)
        txn.status = TransactionStatus.SUCCESS
        atm.notify_observers(txn)
        return f"Account: {atm.current_account.account_number} | Balance: ${balance:.2f}"

    def withdraw(self, atm: ATM, amount: int) -> str:
        account = atm.current_account
        txn = Transaction(TransactionType.WITHDRAWAL, account, amount)

        if amount <= 0 or amount % 10 != 0:
            txn.status = TransactionStatus.FAILED
            atm.notify_observers(txn)
            return "Amount must be a positive multiple of $10."

        if amount > account.get_balance():
            txn.status = TransactionStatus.FAILED
            atm.notify_observers(txn)
            return f"Insufficient funds. Available: ${account.get_balance():.2f}"

        remaining_limit = account.daily_withdrawal_limit - account.withdrawn_today
        if amount > remaining_limit:
            txn.status = TransactionStatus.FAILED
            atm.notify_observers(txn)
            return f"Exceeds daily limit. Remaining today: ${remaining_limit:.2f}"

        denominations = atm.cash_dispenser.dispense(amount)
        if denominations is None:
            txn.status = TransactionStatus.FAILED
            atm.notify_observers(txn)
            return "ATM cannot dispense this amount. Try a different amount."

        account.debit(amount)
        txn.status = TransactionStatus.SUCCESS
        txn.details["denominations"] = denominations
        atm.notify_observers(txn)
        atm.transactions.append(txn)

        denom_str = ", ".join(f"{c}x${d}" for d, c in
                              sorted(denominations.items(), reverse=True))
        receipt_text = txn.generate_receipt(atm.atm_id)
        return (f"Dispensed ${amount}: [{denom_str}]\n"
                f"Remaining balance: ${account.get_balance():.2f}\n\n{receipt_text}")

    def deposit(self, atm: ATM, amount: float) -> str:
        if amount <= 0:
            return "Invalid deposit amount."
        account = atm.current_account
        account.credit(amount)
        txn = Transaction(TransactionType.DEPOSIT, account, amount)
        txn.status = TransactionStatus.SUCCESS
        atm.notify_observers(txn)
        atm.transactions.append(txn)
        return f"Deposited ${amount:.2f}. New balance: ${account.get_balance():.2f}"

    def transfer(self, atm: ATM, target: Account, amount: float) -> str:
        account = atm.current_account
        txn = Transaction(TransactionType.TRANSFER, account, amount,
                          target_account=target)
        if amount > account.get_balance():
            txn.status = TransactionStatus.FAILED
            atm.notify_observers(txn)
            return "Insufficient funds for transfer."
        account.balance -= amount
        target.credit(amount)
        txn.status = TransactionStatus.SUCCESS
        atm.notify_observers(txn)
        atm.transactions.append(txn)
        return (f"Transferred ${amount:.2f} to {target.account_number}. "
                f"Your balance: ${account.get_balance():.2f}")

    def eject_card(self, atm: ATM) -> str:
        from idle_state import IdleState
        card_num = atm.current_card.get_masked_number()
        atm.current_card = None
        atm.current_account = None
        atm.set_state(IdleState())
        return f"Card {card_num} ejected. Thank you!"
