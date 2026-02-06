"""
Expense entity for the Splitwise system.
Represents a single expense paid by one user and split among participants.
"""

from datetime import datetime
import uuid

from user import User
from split import Split


class Expense:
    """Represents an expense in the system."""

    def __init__(self, paid_by: User, amount: float, description: str,
                 splits: list[Split]):
        """
        Args:
            paid_by: The user who paid.
            amount: Total expense amount.
            description: Description of the expense.
            splits: How the expense is split among participants.
        """
        self.id: str = str(uuid.uuid4())[:8]
        self.paid_by = paid_by
        self.amount = amount
        self.description = description
        self.splits = splits
        self.created_at: datetime = datetime.now()

    def __repr__(self) -> str:
        return f"Expense({self.description}, ${self.amount:.2f}, paid_by={self.paid_by.name})"
