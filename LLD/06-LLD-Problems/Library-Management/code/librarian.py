"""Librarian class - manages books in the library."""

from account import Account
from book import Book
from book_item import BookItem


class Librarian(Account):
    """A librarian who can add/remove books from the library."""

    def __init__(self, librarian_id: str, name: str, email: str = ""):
        super().__init__(librarian_id, name, email)

    def get_role(self) -> str:
        return "Librarian"

    def add_book(self, library, book: Book) -> None:
        """Add a book title to the library catalog."""
        library.catalog[book.isbn] = book
        print(f"  [Librarian {self.name}] Added {book}")

    def add_copy(self, book: Book) -> BookItem:
        """Add a physical copy of a book."""
        item = BookItem(book)
        print(f"  [Librarian {self.name}] Added copy {item.barcode} of '{book.title}'")
        return item

    def remove_book(self, library, isbn: str) -> None:
        """Remove a book title from the catalog."""
        if isbn in library.catalog:
            book = library.catalog.pop(isbn)
            print(f"  [Librarian {self.name}] Removed '{book.title}'")
