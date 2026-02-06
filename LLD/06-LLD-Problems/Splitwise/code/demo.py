"""
Splitwise / Expense Splitter - Demo
=====================================
Group of friends, add expenses, show balances, simplify debts.
Design Patterns: Strategy (split types), Observer (notifications)
"""

from enums import SplitType
from expense_service import ExpenseService


def main():
    service = ExpenseService()

    # Create users
    alice = service.add_user("Alice", "alice@example.com", "555-0001")
    bob = service.add_user("Bob", "bob@example.com", "555-0002")
    charlie = service.add_user("Charlie", "charlie@example.com", "555-0003")
    diana = service.add_user("Diana", "diana@example.com", "555-0004")

    # Create a group
    trip = service.create_group("Goa Trip", [alice, bob, charlie, diana])

    # --- EQUAL SPLIT ---
    print("=" * 60)
    print("1. EQUAL SPLIT: Alice pays $200 dinner for all 4")
    print("=" * 60)
    service.add_expense(alice, 200, [alice, bob, charlie, diana],
                        SplitType.EQUAL, "Dinner")
    service.print_balances(alice)

    # --- EXACT SPLIT ---
    print("\n" + "=" * 60)
    print("2. EXACT SPLIT: Bob pays $150 for activities")
    print("=" * 60)
    service.add_expense(bob, 150, [alice, bob, charlie, diana],
                        SplitType.EXACT, "Activities",
                        {"amounts": [20, 50, 40, 40]})
    service.print_balances(bob)

    # --- PERCENTAGE SPLIT ---
    print("\n" + "=" * 60)
    print("3. PERCENTAGE SPLIT: Charlie pays $100 hotel (40/30/20/10)")
    print("=" * 60)
    service.add_expense(charlie, 100, [alice, bob, charlie, diana],
                        SplitType.PERCENTAGE, "Hotel",
                        {"percentages": [40, 30, 20, 10]})
    service.print_balances(charlie)

    # --- Show all balances ---
    print("\n" + "=" * 60)
    print("ALL BALANCES:")
    print("=" * 60)
    for user in [alice, bob, charlie, diana]:
        service.print_balances(user)

    # --- Debt simplification ---
    print("\n" + "=" * 60)
    print("SIMPLIFIED DEBTS (minimize transactions):")
    print("=" * 60)
    transactions = service.simplify_group_debts(trip)
    for from_u, to_u, amt in transactions:
        print(f"  {from_u.name} pays {to_u.name}: ${amt:.2f}")
    print(f"  Total transactions: {len(transactions)} "
          f"(reduced from potentially {len(trip.members) * (len(trip.members)-1) // 2})")

    # --- Settlement ---
    print("\n" + "=" * 60)
    print("SETTLEMENT:")
    print("=" * 60)
    if transactions:
        from_u, to_u, amt = transactions[0]
        service.settle(from_u, to_u, amt)
        service.print_balances(from_u)

    # --- Validation demo ---
    print("\n" + "=" * 60)
    print("VALIDATION: Bad percentage split (sums to 90%)")
    print("=" * 60)
    try:
        service.add_expense(alice, 100, [alice, bob, charlie],
                            SplitType.PERCENTAGE, "Bad split",
                            {"percentages": [40, 30, 20]})
    except ValueError as e:
        print(f"  Caught: {e}")


if __name__ == "__main__":
    main()
