"""
ATM Machine - Demo
===================
Full ATM workflow: insert card -> PIN -> balance -> withdraw -> receipt.
Design Patterns: State, Chain of Responsibility, Observer
"""

from enums import AccountType
from account import Account
from card import Card
from atm import ATM, AuditLogger, ATMNotificationService


def main():
    print("=" * 60)
    print("           ATM MACHINE - LOW LEVEL DESIGN DEMO")
    print("=" * 60)

    # Setup ATM
    atm = ATM("ATM-001", "Main Street Branch")
    atm.add_observer(AuditLogger())
    atm.add_observer(ATMNotificationService())

    print(f"\nATM: {atm.atm_id} at {atm.location}")
    print(f"Cash: {atm.cash_dispenser}")

    # Create accounts and card
    savings = Account("SAV-1001", AccountType.SAVINGS, 5000.0, daily_limit=2000.0)
    checking = Account("CHK-1001", AccountType.CHECKING, 3000.0, daily_limit=1500.0)
    card = Card("1234567890123456", "1234", "National Bank", [savings, checking])

    # Another account for transfer
    other_savings = Account("SAV-2002", AccountType.SAVINGS, 1000.0)

    # ---- Scenario 1: Full withdrawal flow ----
    print("\n" + "=" * 60)
    print("SCENARIO 1: Insert Card -> Authenticate -> Withdraw $270")
    print("=" * 60)

    print(f"\n>> {atm.insert_card(card)}")
    print(f">> {atm.enter_pin('1234')}")
    print(f">> {atm.check_balance()}")
    print(f"\n>> Withdraw $270:")
    print(atm.withdraw(270))

    # ---- Scenario 2: Deposit ----
    print("\n" + "=" * 60)
    print("SCENARIO 2: Deposit $500")
    print("=" * 60)
    print(f">> {atm.deposit(500.0)}")

    # ---- Scenario 3: Transfer ----
    print("\n" + "=" * 60)
    print("SCENARIO 3: Transfer $200 to another account")
    print("=" * 60)
    print(f">> {atm.transfer(other_savings, 200.0)}")

    # ---- Eject card ----
    print(f"\n>> {atm.eject_card()}")

    # ---- Scenario 4: Wrong PIN attempts ----
    print("\n" + "=" * 60)
    print("SCENARIO 4: Failed PIN - Card Retention")
    print("=" * 60)

    card2 = Card("9876543210987654", "5678", "City Bank",
                 [Account("SAV-3001", AccountType.SAVINGS, 2000.0)])

    print(f">> {atm.insert_card(card2)}")
    print(f">> {atm.enter_pin('0000')}")  # Wrong
    print(f">> {atm.enter_pin('1111')}")  # Wrong
    print(f">> {atm.enter_pin('2222')}")  # Wrong - card retained

    # ---- Scenario 5: Edge cases ----
    print("\n" + "=" * 60)
    print("SCENARIO 5: Edge Cases")
    print("=" * 60)

    print(f"\n>> Try to withdraw without card: {atm.withdraw(100)}")
    print(f">> {atm.insert_card(card)}")
    print(f">> {atm.enter_pin('1234')}")
    print(f">> Withdraw $35 (not multiple of 10): {atm.withdraw(35)}")
    print(f">> Withdraw $50000: {atm.withdraw(50000)}")

    print(f"\n>> {atm.eject_card()}")

    # ---- Final inventory ----
    print("\n" + "=" * 60)
    print("FINAL STATE")
    print("=" * 60)
    print(f"ATM {atm.cash_dispenser}")
    print(f"Total transactions processed: {len(atm.transactions)}")
    for txn in atm.transactions:
        print(f"  - {txn.transaction_type.value}: ${txn.amount:.2f} ({txn.status.value})")


if __name__ == "__main__":
    main()
