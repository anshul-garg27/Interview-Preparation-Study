"""
Transaction record for the ATM system.
Captures all details of a single ATM transaction.
"""

from datetime import datetime
from typing import Optional
import uuid

from enums import TransactionType, TransactionStatus
from account import Account


class Transaction:
    """Immutable record of an ATM transaction."""

    def __init__(self, transaction_type: TransactionType, account: Account,
                 amount: float, target_account: Optional[Account] = None):
        """
        Args:
            transaction_type: Type of transaction performed.
            account: Primary account involved.
            amount: Transaction amount.
            target_account: Destination account (for transfers).
        """
        self.transaction_id: str = str(uuid.uuid4())[:8]
        self.transaction_type = transaction_type
        self.account = account
        self.amount = amount
        self.target_account = target_account
        self.timestamp: datetime = datetime.now()
        self.status: TransactionStatus = TransactionStatus.FAILED
        self.details: dict = {}

    def generate_receipt(self, atm_id: str) -> str:
        """Generate a formatted receipt string."""
        lines = [
            "=" * 40,
            "         ATM TRANSACTION RECEIPT",
            "=" * 40,
            f"  ATM ID:       {atm_id}",
            f"  Date:         {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Transaction:  {self.transaction_id}",
            "-" * 40,
            f"  Type:         {self.transaction_type.value.upper()}",
            f"  Account:      {self.account.account_number}",
            f"  Amount:       ${self.amount:.2f}",
            f"  Status:       {self.status.value.upper()}",
        ]
        if self.details.get("denominations"):
            lines.append("  Denominations:")
            for denom, count in sorted(self.details["denominations"].items(), reverse=True):
                lines.append(f"    ${denom} x {count} = ${denom * count}")
        lines.append("-" * 40)
        lines.append(f"  Balance:      ${self.account.get_balance():.2f}")
        lines.append("=" * 40)
        return "\n".join(lines)
