"""
In-Memory Key-Value Store - Demo
==================================
Run: python demo.py
"""

import time
from key_value_store import KeyValueStore
from command_parser import CommandParser


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    store = KeyValueStore()
    parser = CommandParser(store)

    print_header("IN-MEMORY KEY-VALUE STORE")

    # =========================================================================
    # FEATURE 1: Basic SET/GET/DELETE/EXISTS
    # =========================================================================
    print_header("Feature 1: Basic Operations")

    parser.process_commands([
        "SET name Alice",
        "SET age 30",
        "SET city NewYork",
        "GET name",
        "GET age",
        "GET unknown",
        "EXISTS name",
        "EXISTS unknown",
        "KEYS",
    ])

    # =========================================================================
    # FEATURE 2: DELETE
    # =========================================================================
    print_header("Feature 2: Delete")

    parser.process_commands([
        "DELETE city",
        "GET city",
        "DELETE nonexistent",
        "KEYS",
    ])

    # =========================================================================
    # FEATURE 3: Transactions - BEGIN/COMMIT
    # =========================================================================
    print_header("Feature 3: Transaction - Commit")

    parser.process_commands([
        "BEGIN",
        "SET name Bob",
        "SET email bob@example.com",
        "GET name",
        "COMMIT",
        "GET name",
        "GET email",
    ])

    # =========================================================================
    # FEATURE 4: Transactions - ROLLBACK
    # =========================================================================
    print_header("Feature 4: Transaction - Rollback")

    parser.process_commands([
        "GET name",
        "BEGIN",
        "SET name Charlie",
        "SET phone 12345",
        "GET name",
        "ROLLBACK",
        "GET name",
        "GET phone",
    ])

    # =========================================================================
    # FEATURE 5: Nested Transactions
    # =========================================================================
    print_header("Feature 5: Nested Transactions")

    parser.process_commands([
        "SET name Diana",
        "BEGIN",
        "SET name Eve",
        "BEGIN",
        "SET name Frank",
        "GET name",
        "ROLLBACK",
        "GET name",
        "COMMIT",
        "GET name",
    ])

    # =========================================================================
    # FEATURE 6: Transaction Edge Cases
    # =========================================================================
    print_header("Feature 6: Transaction Edge Cases")

    parser.process_commands([
        "ROLLBACK",
        "COMMIT",
    ])

    # =========================================================================
    # FEATURE 7: TTL (Time-to-Live)
    # =========================================================================
    print_header("Feature 7: TTL (Time-to-Live)")

    parser.process_commands([
        "SET session abc123 TTL 3",
        "SET cache_key data456 TTL 10",
        "GET session",
        "TTL session",
        "TTL cache_key",
        "TTL name",
    ])

    print("\n  (Waiting 4 seconds for session to expire...)")
    time.sleep(4)

    parser.process_commands([
        "GET session",
        "EXISTS session",
        "GET cache_key",
        "TTL cache_key",
    ])

    # =========================================================================
    # FEATURE 8: Snapshots
    # =========================================================================
    print_header("Feature 8: Snapshots")

    parser.process_commands([
        "KEYS",
        "SNAPSHOT",
    ])

    # Make changes after snapshot
    parser.process_commands([
        "SET name Grace",
        "SET new_key hello",
        "DELETE age",
        "KEYS",
    ])

    # Restore snapshot
    print("\n  --- Restoring to snapshot ---")
    parser.process_commands([
        "RESTORE S-001",
        "KEYS",
    ])

    # =========================================================================
    # FEATURE 9: Invalid Snapshot Restore
    # =========================================================================
    print_header("Feature 9: Error Handling")

    parser.process_commands([
        "RESTORE S-999",
        "GET",
        "SET",
        "SET only_key",
        "INVALID_CMD test",
    ])

    # =========================================================================
    # FEATURE 10: COUNT and SNAPSHOTS list
    # =========================================================================
    print_header("Feature 10: Count and Snapshot List")

    parser.process_commands([
        "COUNT",
        "SNAPSHOT",
        "SNAPSHOTS",
    ])

    # =========================================================================
    # FINAL STATE
    # =========================================================================
    print_header("Final State")
    parser.process_commands([
        "KEYS",
    ])

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
