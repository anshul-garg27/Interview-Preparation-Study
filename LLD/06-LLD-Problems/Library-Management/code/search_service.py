"""SearchService - search the library catalog by various criteria."""

from typing import Optional, List
from book import Book


class SearchService:
    """Provides search capabilities across the library catalog."""

    def __init__(self, catalog: dict):
        self._catalog = catalog  # isbn -> Book

    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title (case-insensitive partial match)."""
        return [b for b in self._catalog.values()
                if title.lower() in b.title.lower()]

    def search_by_author(self, author: str) -> List[Book]:
        """Search books by author (case-insensitive partial match)."""
        return [b for b in self._catalog.values()
                if author.lower() in b.author.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        """Look up a book by exact ISBN."""
        return self._catalog.get(isbn)

    def search_by_category(self, category: str) -> List[Book]:
        """Search books by category (case-insensitive partial match)."""
        return [b for b in self._catalog.values()
                if category.lower() in b.category.lower()]
