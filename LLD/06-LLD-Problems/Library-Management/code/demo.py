"""Library Management System - Full Demo: register, checkout, return, search, fines."""

from book import Book
from book_item import BookItem
from member import Member, MemberObserver
from librarian import Librarian
from library import Library


def main():
    print("=" * 65)
    print("  LIBRARY MANAGEMENT SYSTEM - Modular LLD Demo")
    print("=" * 65)

    # 1. Create library and librarian
    library = Library("City Central Library")
    lib_staff = Librarian("L1", "Ms. Smith", "smith@library.com")

    # 2. Add books with multiple copies
    books = [
        Book("978-0-13-468599-1", "Clean Code", "Robert C. Martin", "Programming"),
        Book("978-0-201-63361-0", "Design Patterns", "Gang of Four", "Programming"),
        Book("978-0-13-235088-4", "Clean Architecture", "Robert C. Martin", "Architecture"),
        Book("978-0-596-51774-8", "JavaScript: Good Parts", "Douglas Crockford", "Web Dev"),
    ]
    print("\n--- Adding Books ---")
    for book in books:
        lib_staff.add_book(library, book)

    print("\n--- Adding Copies ---")
    copies = {}
    for book in books:
        copies[book.isbn] = []
        for _ in range(2):
            copies[book.isbn].append(lib_staff.add_copy(book))

    library.display_catalog()

    # 3. Register members
    print("\n--- Registering Members ---")
    alice = Member("M001", "Alice", "alice@email.com")
    bob = Member("M002", "Bob", "bob@email.com")
    charlie = Member("M003", "Charlie", "charlie@email.com")
    for m in [alice, bob, charlie]:
        library.register_member(m)

    # 4. Checkout books
    print("\n--- Checkout Flow ---")
    library.checkout_book(alice, copies["978-0-13-468599-1"][0])
    library.checkout_book(alice, copies["978-0-201-63361-0"][0])
    library.checkout_book(bob, copies["978-0-13-468599-1"][1])
    library.checkout_book(charlie, copies["978-0-596-51774-8"][0])

    # 5. Bob watches Clean Code availability (Observer)
    print("\n--- Observer: Bob Watches 'Clean Code' ---")
    clean_code = books[0]
    clean_code.add_observer(bob.observer)
    print(f"  Clean Code available copies: {len(clean_code.available_copies())}")

    # 6. Search
    print("\n--- Search ---")
    print("  Search by author 'Robert':")
    for b in library.search_by_author("Robert"):
        print(f"    {b}")

    print("  Search by title 'Design':")
    for b in library.search_by_title("Design"):
        print(f"    {b}")

    print("  Search by ISBN '978-0-596-51774-8':")
    result = library.search_by_isbn("978-0-596-51774-8")
    print(f"    {result}")

    print("  Search by category 'Programming':")
    for b in library.search_by_category("Programming"):
        print(f"    {b}")

    # 7. Returns (some overdue)
    print("\n--- Returns ---")
    library.return_book(alice, copies["978-0-13-468599-1"][0])  # On time -> notifies Bob
    library.return_book(bob, copies["978-0-13-468599-1"][1], simulated_overdue_days=5)

    # 8. Fine handling
    print("\n--- Fine Payment ---")
    print(f"  Bob's fines: {bob.fines}")
    print(f"  Bob can checkout: {bob.can_checkout()}")
    bob.fines[0].pay()
    print(f"  Bob can checkout after paying: {bob.can_checkout()}")

    # 9. Bob checks out again after paying fine
    print("\n--- Bob Checks Out Again ---")
    library.checkout_book(bob, copies["978-0-13-235088-4"][0])

    # 10. Final returns
    print("\n--- Final Returns ---")
    library.return_book(alice, copies["978-0-201-63361-0"][0])
    library.return_book(charlie, copies["978-0-596-51774-8"][0])
    library.return_book(bob, copies["978-0-13-235088-4"][0])

    # 11. Final catalog
    library.display_catalog()

    # 12. Lending history
    print("\n  Lending History:")
    for lending in library.lendings:
        print(f"    {lending}")

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
