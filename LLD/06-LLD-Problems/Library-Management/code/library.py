"""Library (Singleton) - manages all library operations."""

import threading
from datetime import datetime, timedelta
from typing import Optional

from enums import BookStatus, AccountStatus
from book import Book
from book_item import BookItem
from member import Member
from book_lending import BookLending
from fine import Fine
from search_service import SearchService


class Library:
    """Singleton library managing catalog, members, lending, and fines."""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls, name: str = "Library"):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, name: str = "Library"):
        if self._initialized:
            return
        self.name = name
        self.catalog = {}   # isbn -> Book
        self.members = {}   # member_id -> Member
        self.lendings = []
        self.fines = []
        self._search = SearchService(self.catalog)
        self._initialized = True

    def register_member(self, member: Member) -> None:
        self.members[member.account_id] = member
        print(f"  [Register] {member.name} joined '{self.name}'")

    def checkout_book(self, member: Member, book_item: BookItem,
                      simulated_due_days: int = 14) -> Optional[BookLending]:
        """Checkout a book copy to a member."""
        if not member.can_checkout():
            reasons = []
            if member.status != AccountStatus.ACTIVE:
                reasons.append("account not active")
            if len(member.checked_out_items) >= Member.MAX_BOOKS:
                reasons.append("max books reached")
            if any(not f.paid for f in member.fines):
                reasons.append("unpaid fines")
            print(f"  [Checkout DENIED] {member.name}: {', '.join(reasons)}")
            return None
        if book_item.status != BookStatus.AVAILABLE:
            print(f"  [Checkout DENIED] '{book_item.book.title}' copy not available")
            return None

        book_item.checkout(member, days=simulated_due_days)
        member.checked_out_items.append(book_item)
        lending = BookLending(member, book_item)
        self.lendings.append(lending)
        print(f"  [Checkout] {member.name} <- '{book_item.book.title}' "
              f"({book_item.barcode}) due {book_item.due_date.strftime('%Y-%m-%d')}")
        return lending

    def return_book(self, member: Member, book_item: BookItem,
                    simulated_overdue_days: int = 0) -> Optional[Fine]:
        """Return a book and calculate any fines."""
        if book_item not in member.checked_out_items:
            print(f"  [Return ERROR] {member.name} doesn't have {book_item.barcode}")
            return None

        if simulated_overdue_days > 0:
            book_item.due_date = datetime.now() - timedelta(days=simulated_overdue_days)

        overdue_days = book_item.return_item()
        member.checked_out_items.remove(book_item)

        for lending in reversed(self.lendings):
            if lending.book_item == book_item and lending.return_date is None:
                lending.complete()
                break

        fine = None
        if overdue_days > 0 or simulated_overdue_days > 0:
            days = max(overdue_days, simulated_overdue_days)
            fine = Fine(member, book_item, days)
            member.fines.append(fine)
            self.fines.append(fine)
            print(f"  [Return + Fine] {member.name} -> '{book_item.book.title}' "
                  f"(${fine.amount:.2f} fine, {days} days late)")
        else:
            print(f"  [Return] {member.name} -> '{book_item.book.title}' (on time)")

        if book_item.book.available_copies():
            book_item.book.notify_observers()

        return fine

    def search_by_title(self, title: str) -> list:
        return self._search.search_by_title(title)

    def search_by_author(self, author: str) -> list:
        return self._search.search_by_author(author)

    def search_by_isbn(self, isbn: str):
        return self._search.search_by_isbn(isbn)

    def search_by_category(self, category: str) -> list:
        return self._search.search_by_category(category)

    def display_catalog(self) -> None:
        print(f"\n  {'='*60}")
        print(f"  {self.name} - Catalog")
        print(f"  {'='*60}")
        for book in self.catalog.values():
            print(f"    {book}")
        print(f"  {'='*60}")
