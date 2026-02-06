"""
PercentageSplit - Each participant pays a specified percentage.
"""

from user import User
from split import Split


class PercentageSplit(Split):
    """Split where each user pays a percentage of the total."""

    def __init__(self, user: User, percentage: float):
        """
        Args:
            user: The user this split applies to.
            percentage: The percentage (0-100) of the total this user pays.
        """
        super().__init__(user)
        self.percentage = percentage

    def get_split_detail(self) -> str:
        return f"{self.user.name} owes ${self.amount:.2f} ({self.percentage}%)"
