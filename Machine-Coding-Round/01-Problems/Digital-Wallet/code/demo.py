"""
Digital Wallet System - Demo
==============================
Run: python demo.py
"""

from enums import TransactionType
from transaction_service import TransactionService
from statement_service import StatementService
from offer_service import OfferService


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def main():
    # =========================================================================
    # SETUP
    # =========================================================================
    print_header("DIGITAL WALLET SYSTEM")

    txn_service = TransactionService()
    stmt_service = StatementService(txn_service)
    offer_service = OfferService(txn_service)

    # =========================================================================
    # FEATURE 1: Create Users
    # =========================================================================
    print_header("Feature 1: Create Users")

    alice = txn_service.create_user("Alice")
    bob = txn_service.create_user("Bob")
    charlie = txn_service.create_user("Charlie")
    diana = txn_service.create_user("Diana")

    # Try duplicate user
    txn_service.create_user("Alice")

    # =========================================================================
    # FEATURE 2: Add Money (Top-up) with Cashback
    # =========================================================================
    print_header("Feature 2: Add Money (Top-up)")

    # Alice adds 1000 - first top-up gets 10% cashback (max 100)
    result = txn_service.add_money(alice.id, 1000.00)
    if result:
        _, is_first = result
        if is_first:
            offer_service.apply_first_topup_cashback(alice.id, 1000.00)

    # Bob adds 500 - first top-up gets 10% cashback = 50
    result = txn_service.add_money(bob.id, 500.00)
    if result:
        _, is_first = result
        if is_first:
            offer_service.apply_first_topup_cashback(bob.id, 500.00)

    # Alice adds more money - NOT first top-up, no cashback
    result = txn_service.add_money(alice.id, 200.00)
    if result:
        _, is_first = result
        if is_first:
            offer_service.apply_first_topup_cashback(alice.id, 200.00)
    print("  (No cashback - not Alice's first top-up)")

    # Charlie adds 2000 - cashback capped at 100
    result = txn_service.add_money(charlie.id, 2000.00)
    if result:
        _, is_first = result
        if is_first:
            offer_service.apply_first_topup_cashback(charlie.id, 2000.00)

    # =========================================================================
    # FEATURE 3: Referral Bonus
    # =========================================================================
    print_header("Feature 3: Referral Bonus")

    # Alice refers Diana - both get 50
    offer_service.apply_referral_bonus(alice.id, diana.id)

    # Error: self-referral
    offer_service.apply_referral_bonus(bob.id, bob.id)

    # =========================================================================
    # FEATURE 4: Transfer Money
    # =========================================================================
    print_header("Feature 4: Transfer Money")

    # Alice -> Bob: 200
    txn_service.transfer(alice.id, bob.id, 200.00)

    # Bob -> Charlie: 100
    txn_service.transfer(bob.id, charlie.id, 100.00)

    # Diana tries to transfer more than she has
    txn_service.transfer(diana.id, alice.id, 100.00)

    # Self-transfer error
    txn_service.transfer(alice.id, alice.id, 50.00)

    # =========================================================================
    # FEATURE 5: Withdraw Money
    # =========================================================================
    print_header("Feature 5: Withdraw Money")

    txn_service.withdraw(alice.id, 150.00)

    # Try to withdraw more than balance
    txn_service.withdraw(diana.id, 200.00)

    # Try negative amount
    txn_service.withdraw(bob.id, -50.00)

    # =========================================================================
    # FEATURE 6: Transaction History
    # =========================================================================
    print_header("Feature 6: Transaction History")

    # Full statement for Alice
    stmt_service.display_statement(alice.id)

    # Only credits for Bob
    stmt_service.display_statement(bob.id, txn_type_filter=TransactionType.CREDIT,
                                    title="Bob's Credits Only")

    # Charlie's statement
    stmt_service.display_statement(charlie.id)

    # Diana's statement
    stmt_service.display_statement(diana.id)

    # =========================================================================
    # FEATURE 7: Wallet Summary
    # =========================================================================
    print_header("Feature 7: Wallet Summary")

    stmt_service.display_wallet_summary()

    # =========================================================================
    # FEATURE 8: Offers Applied
    # =========================================================================
    print_header("Feature 8: Offers Applied")

    offer_service.display_offers(alice.id)
    offer_service.display_offers(bob.id)
    offer_service.display_offers(charlie.id)
    offer_service.display_offers(diana.id)

    # =========================================================================
    # FEATURE 9: Edge Cases
    # =========================================================================
    print_header("Feature 9: Edge Cases")

    # Non-existent user
    txn_service.add_money("U-999", 100.00)
    txn_service.transfer("U-999", alice.id, 50.00)
    txn_service.withdraw("U-999", 50.00)

    # Zero/negative amounts
    txn_service.add_money(alice.id, 0)
    txn_service.add_money(alice.id, -100)

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
