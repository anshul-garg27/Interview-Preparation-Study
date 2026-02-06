"""
Group entity for the Splitwise system.
A group contains members who share expenses.
"""

from collections import defaultdict
import uuid

from user import User
from expense import Expense


class Group:
    """Represents a group of users sharing expenses."""

    def __init__(self, name: str, members: list[User]):
        """
        Args:
            name: Group name.
            members: Initial list of group members.
        """
        self.id: str = str(uuid.uuid4())[:8]
        self.name = name
        self.members: dict[str, User] = {u.id: u for u in members}
        self.expenses: list[Expense] = []

    def add_member(self, user: User) -> None:
        """Add a member to the group."""
        self.members[user.id] = user

    def get_net_balances(self) -> dict[str, float]:
        """
        Calculate net balance for each member within the group.

        Returns:
            Dict mapping user_id to net balance (positive = owed money).
        """
        member_ids = set(self.members.keys())
        net: dict[str, float] = defaultdict(float)
        for uid, user in self.members.items():
            for other_id, bal in user.balances.items():
                if other_id in member_ids:
                    net[uid] += bal
        return dict(net)
