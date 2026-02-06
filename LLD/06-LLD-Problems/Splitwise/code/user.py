"""
User entity for the Splitwise system.
Tracks balances with other users (positive = owed to me, negative = I owe).
"""

from collections import defaultdict
import uuid


class User:
    """Represents a user in the expense-sharing system."""

    def __init__(self, name: str, email: str, phone: str = ""):
        """
        Args:
            name: Display name.
            email: User email.
            phone: Optional phone number.
        """
        self.id: str = str(uuid.uuid4())[:8]
        self.name = name
        self.email = email
        self.phone = phone
        # balances[other_user_id] > 0 means other user owes me
        # balances[other_user_id] < 0 means I owe other user
        self.balances: dict[str, float] = defaultdict(float)

    def update_balance(self, other_user_id: str, amount: float) -> None:
        """
        Update balance with another user.

        Args:
            other_user_id: The other user's ID.
            amount: Positive = they owe me more, negative = I owe them more.
        """
        self.balances[other_user_id] = round(self.balances[other_user_id] + amount, 2)
        if self.balances[other_user_id] == 0:
            del self.balances[other_user_id]

    def get_total_owed_to_me(self) -> float:
        """Total amount others owe this user."""
        return sum(v for v in self.balances.values() if v > 0)

    def get_total_i_owe(self) -> float:
        """Total amount this user owes others."""
        return sum(-v for v in self.balances.values() if v < 0)

    def __repr__(self) -> str:
        return f"User({self.name})"
