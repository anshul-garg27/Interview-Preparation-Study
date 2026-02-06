"""BookLending class - record of a lending transaction."""

from datetime import datetime
from typing import Optional
from book_item import BookItem
from member import Member


class BookLending:
    """Tracks a single book checkout/return transaction."""

    _counter = 0

    def __init__(self, member: Member, book_item: BookItem):
        BookLending._counter += 1
        self.lending_id = f"LEND-{BookLending._counter:04d}"
        self.member = member
        self.book_item = book_item
        self.checkout_date = datetime.now()
        self.due_date = book_item.due_date
        self.return_date: Optional[datetime] = None

    def complete(self) -> None:
        """Mark lending as returned."""
        self.return_date = datetime.now()

    def __repr__(self) -> str:
        status = "Returned" if self.return_date else "Active"
        return (f"Lending({self.lending_id}, {self.member.name}, "
                f"'{self.book_item.book.title}', {status})")
