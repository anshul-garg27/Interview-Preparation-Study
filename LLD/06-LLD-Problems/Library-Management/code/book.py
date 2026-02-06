"""Book class - represents a book title (can have multiple copies)."""

from enums import BookStatus


class Book:
    """A book title in the library catalog (may have multiple physical copies)."""

    def __init__(self, isbn: str, title: str, author: str, category: str):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.category = category
        self.items = []       # List of BookItem (physical copies)
        self._observers = []  # Members waiting for availability

    def add_observer(self, observer) -> None:
        """Subscribe an observer for availability notifications."""
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"    [Subscribe] {observer.member.name} watching '{self.title}'")

    def remove_observer(self, observer) -> None:
        self._observers = [o for o in self._observers if o is not observer]

    def notify_observers(self) -> None:
        """Notify all waiting observers that a copy is available."""
        for obs in self._observers:
            obs.notify(f"'{self.title}' is now available!")
        self._observers.clear()

    def available_copies(self) -> list:
        return [item for item in self.items if item.status == BookStatus.AVAILABLE]

    def __repr__(self) -> str:
        avail = len(self.available_copies())
        return (f"'{self.title}' by {self.author} [ISBN:{self.isbn}] "
                f"({avail}/{len(self.items)} available)")
