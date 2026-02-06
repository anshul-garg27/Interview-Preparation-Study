"""BookItem class - a physical copy of a book."""

from datetime import datetime, timedelta
from typing import Optional
from enums import BookStatus
from book import Book
from rack import Rack


class BookItem:
    """A physical copy of a book with barcode, status, and rack location."""

    _counter = 0

    def __init__(self, book: Book, rack: Optional[Rack] = None):
        BookItem._counter += 1
        self.barcode = f"BC-{BookItem._counter:04d}"
        self.book = book
        self.status = BookStatus.AVAILABLE
        self.rack = rack
        self.due_date: Optional[datetime] = None
        self.borrowed_by = None
        book.items.append(self)

    def checkout(self, member, days: int = 14) -> None:
        """Mark as checked out with a due date."""
        self.status = BookStatus.CHECKED_OUT
        self.due_date = datetime.now() + timedelta(days=days)
        self.borrowed_by = member

    def return_item(self) -> int:
        """Return the book and calculate overdue days."""
        self.status = BookStatus.AVAILABLE
        overdue_days = 0
        if self.due_date and datetime.now() > self.due_date:
            overdue_days = (datetime.now() - self.due_date).days
        self.due_date = None
        self.borrowed_by = None
        return overdue_days

    def __repr__(self) -> str:
        return f"BookItem({self.barcode}, '{self.book.title}', {self.status.value})"
