"""
ExpenseService - Facade for adding expenses and computing balances.
Coordinates split strategies, balance updates, and debt simplification.
"""

from enums import SplitType
from user import User
from split import Split
from equal_split import EqualSplit
from exact_split import ExactSplit
from percentage_split import PercentageSplit
from expense import Expense
from group import Group
from balance_sheet import BalanceSheet


class ExpenseService:
    """Service layer for managing expenses and balances."""

    def __init__(self):
        self.users: dict[str, User] = {}
        self.groups: dict[str, Group] = {}

    def add_user(self, name: str, email: str, phone: str = "") -> User:
        """Register a new user."""
        user = User(name, email, phone)
        self.users[user.id] = user
        return user

    def create_group(self, name: str, members: list[User]) -> Group:
        """Create a new expense group."""
        group = Group(name, members)
        self.groups[group.id] = group
        return group

    def add_expense(self, paid_by: User, amount: float, participants: list[User],
                    split_type: SplitType, description: str = "",
                    params: dict = None) -> Expense:
        """
        Add an expense and update all participant balances.

        Args:
            paid_by: The user who paid.
            amount: Total expense amount.
            participants: Users involved in the expense.
            split_type: How to split (EQUAL, EXACT, PERCENTAGE).
            description: Description of the expense.
            params: Additional parameters (amounts for EXACT, percentages for PERCENTAGE).

        Returns:
            The created Expense.

        Raises:
            ValueError: If split parameters are invalid.
        """
        splits = self._calculate_splits(amount, participants, split_type, params)
        expense = Expense(paid_by, amount, description, splits)

        # Update balances between payer and each participant
        for split in splits:
            if split.user.id != paid_by.id:
                paid_by.update_balance(split.user.id, split.amount)
                split.user.update_balance(paid_by.id, -split.amount)
                print(f"  [Notify] {split.user.name} owes {paid_by.name}: ${split.amount:.2f}")

        return expense

    def _calculate_splits(self, amount: float, participants: list[User],
                          split_type: SplitType, params: dict = None) -> list[Split]:
        """Calculate splits based on the split type."""
        if split_type == SplitType.EQUAL:
            return self._equal_split(amount, participants)
        elif split_type == SplitType.EXACT:
            return self._exact_split(amount, participants, params)
        elif split_type == SplitType.PERCENTAGE:
            return self._percentage_split(amount, participants, params)
        raise ValueError(f"Unknown split type: {split_type}")

    def _equal_split(self, amount: float, participants: list[User]) -> list[Split]:
        """Split equally among all participants."""
        if len(participants) == 0 or amount <= 0:
            raise ValueError("Invalid equal split: need participants and positive amount")
        per_person = amount / len(participants)
        splits = []
        for u in participants:
            s = EqualSplit(u)
            s.amount = round(per_person, 2)
            splits.append(s)
        # Handle rounding: give remainder to last person
        total_assigned = sum(s.amount for s in splits)
        diff = round(amount - total_assigned, 2)
        if diff != 0:
            splits[-1].amount = round(splits[-1].amount + diff, 2)
        return splits

    def _exact_split(self, amount: float, participants: list[User],
                     params: dict = None) -> list[Split]:
        """Split by exact amounts specified per participant."""
        if not params or "amounts" not in params:
            raise ValueError("Exact split requires 'amounts' parameter")
        exact_amounts = params["amounts"]
        if len(exact_amounts) != len(participants):
            raise ValueError("Number of amounts must match participants")
        if abs(sum(exact_amounts) - amount) > 0.01:
            raise ValueError("Exact amounts must sum to total expense amount")
        return [ExactSplit(u, amt) for u, amt in zip(participants, exact_amounts)]

    def _percentage_split(self, amount: float, participants: list[User],
                          params: dict = None) -> list[Split]:
        """Split by percentages specified per participant."""
        if not params or "percentages" not in params:
            raise ValueError("Percentage split requires 'percentages' parameter")
        pcts = params["percentages"]
        if len(pcts) != len(participants):
            raise ValueError("Number of percentages must match participants")
        if abs(sum(pcts) - 100.0) > 0.01:
            raise ValueError(f"Invalid split parameters for {SplitType.PERCENTAGE.value}")
        splits = []
        for u, p in zip(participants, pcts):
            s = PercentageSplit(u, p)
            s.amount = round(amount * p / 100, 2)
            splits.append(s)
        total_assigned = sum(s.amount for s in splits)
        diff = round(amount - total_assigned, 2)
        if diff != 0:
            splits[-1].amount = round(splits[-1].amount + diff, 2)
        return splits

    def settle(self, from_user: User, to_user: User, amount: float) -> None:
        """Record a settlement payment between two users."""
        from_user.update_balance(to_user.id, amount)
        to_user.update_balance(from_user.id, -amount)
        print(f"  [Settle] {from_user.name} paid {to_user.name}: ${amount:.2f}")

    def simplify_group_debts(self, group: Group) -> list[tuple[User, User, float]]:
        """Simplify debts within a group to minimize transactions."""
        net = group.get_net_balances()
        return BalanceSheet.simplify_debts(net, self.users)

    def print_balances(self, user: User) -> None:
        """Print a user's balance summary."""
        print(f"\n  Balances for {user.name}:")
        if not user.balances:
            print("    All settled up!")
            return
        for other_id, amount in user.balances.items():
            other = self.users[other_id]
            if amount > 0:
                print(f"    {other.name} owes you ${amount:.2f}")
            else:
                print(f"    You owe {other.name} ${-amount:.2f}")
