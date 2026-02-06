"""Transaction entity for the Digital Wallet System."""

from datetime import datetime
from enums import TransactionStatus


class Transaction:
    """Represents a single financial transaction."""

    _counter = 0

    def __init__(self, wallet_id, txn_type, category, amount, description="",
                 balance_after=0.0):
        Transaction._counter += 1
        self.id = f"TXN-{Transaction._counter:03d}"
        self.wallet_id = wallet_id
        self.txn_type = txn_type          # CREDIT or DEBIT
        self.category = category           # TOP_UP, TRANSFER_IN, etc.
        self.amount = amount
        self.description = description
        self.balance_after = balance_after
        self.status = TransactionStatus.SUCCESS
        self.timestamp = datetime.now()

    def mark_failed(self, reason=""):
        self.status = TransactionStatus.FAILED
        if reason:
            self.description = reason

    def __str__(self):
        sign = "+" if self.txn_type.value == "CREDIT" else "-"
        return (f"{self.id}  {self.txn_type.value:<7} {sign}{self.amount:>8.2f}  "
                f"{self.category.value:<16} Balance: {self.balance_after:.2f}  "
                f"[{self.status.value}]")
