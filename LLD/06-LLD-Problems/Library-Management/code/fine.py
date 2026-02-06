"""Fine class and FineCalculator for overdue books."""

from book_item import BookItem
from member import Member


class Fine:
    """A fine imposed on a member for an overdue book."""

    def __init__(self, member: Member, book_item: BookItem, overdue_days: int):
        self.member = member
        self.book_item = book_item
        self.overdue_days = overdue_days
        self.amount = FineCalculator.calculate(overdue_days)
        self.paid = False

    def pay(self) -> None:
        """Mark the fine as paid."""
        self.paid = True
        print(f"    [Fine] {self.member.name} paid ${self.amount:.2f} "
              f"({self.overdue_days} days overdue for '{self.book_item.book.title}')")

    def __repr__(self) -> str:
        return (f"Fine({self.member.name}, '{self.book_item.book.title}', "
                f"${self.amount:.2f}, {'Paid' if self.paid else 'Unpaid'})")


class FineCalculator:
    """Calculates fine amount based on overdue days."""

    RATE_PER_DAY = 2.0  # $2 per day

    @staticmethod
    def calculate(overdue_days: int) -> float:
        return overdue_days * FineCalculator.RATE_PER_DAY
