"""
Abstract Split base class for the Splitwise system.
Each split represents one user's share of an expense.
"""

from abc import ABC, abstractmethod

from user import User


class Split(ABC):
    """Base class for expense splits."""

    def __init__(self, user: User):
        """
        Args:
            user: The user this split applies to.
        """
        self.user = user
        self.amount: float = 0.0

    @abstractmethod
    def get_split_detail(self) -> str:
        """Return a description of this split."""
        pass
