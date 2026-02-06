"""
ExactSplit - Each participant pays an exact specified amount.
"""

from user import User
from split import Split


class ExactSplit(Split):
    """Split where each user pays a specific exact amount."""

    def __init__(self, user: User, amount: float):
        """
        Args:
            user: The user this split applies to.
            amount: The exact amount this user owes.
        """
        super().__init__(user)
        self.amount = round(amount, 2)

    def get_split_detail(self) -> str:
        return f"{self.user.name} owes ${self.amount:.2f} (exact)"
