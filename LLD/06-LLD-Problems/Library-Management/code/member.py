"""Member class - a library member who borrows books."""

from abc import ABC, abstractmethod
from account import Account
from enums import AccountStatus


class MemberObserver:
    """Observer to receive notifications for a member."""

    def __init__(self, member: "Member"):
        self.member = member

    def notify(self, message: str) -> None:
        print(f"    [Notification -> {self.member.name}] {message}")


class Member(Account):
    """A library member who can borrow and reserve books."""

    MAX_BOOKS = 5

    def __init__(self, member_id: str, name: str, email: str):
        super().__init__(member_id, name, email)
        self.checked_out_items = []
        self.reservations = []
        self.fines = []
        self.observer = MemberObserver(self)

    def get_role(self) -> str:
        return "Member"

    def can_checkout(self) -> bool:
        """Check if member is allowed to borrow more books."""
        if self.status != AccountStatus.ACTIVE:
            return False
        if len(self.checked_out_items) >= self.MAX_BOOKS:
            return False
        if any(not f.paid for f in self.fines):
            return False
        return True

    def __repr__(self) -> str:
        return (f"Member({self.account_id}, {self.name}, "
                f"Books={len(self.checked_out_items)}/{self.MAX_BOOKS})")
