"""
EqualSplit - Each participant pays an equal share.
"""

from user import User
from split import Split


class EqualSplit(Split):
    """Split where each user pays an equal portion."""

    def __init__(self, user: User):
        super().__init__(user)

    def get_split_detail(self) -> str:
        return f"{self.user.name} owes ${self.amount:.2f} (equal split)"
