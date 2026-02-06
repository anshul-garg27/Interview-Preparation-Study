"""Vending Machine demo - all scenarios."""

from enums import Coin, Note
from product import Product
from vending_machine import VendingMachine


def main():
    print("=" * 60)
    print("  VENDING MACHINE - LLD Demo")
    print("=" * 60)

    # Setup machine
    vm = VendingMachine("VM-001")
    vm.inventory.add_product(Product("A1", "Coca Cola", 25), 5)
    vm.inventory.add_product(Product("A2", "Pepsi", 25), 3)
    vm.inventory.add_product(Product("B1", "Chips", 30), 4)
    vm.inventory.add_product(Product("B2", "Chocolate Bar", 20), 2)
    vm.inventory.add_product(Product("C1", "Water Bottle", 15), 6)
    vm.inventory.add_product(Product("C2", "Energy Drink", 50), 1)

    vm.inventory.display()

    # Scenario 1: Exact amount
    print("\n[Scenario 1: Exact Amount - Buy Coca Cola ($25)]")
    vm.insert_coin(Coin.QUARTER)
    vm.select_product("A1")
    vm.display_status()

    # Scenario 2: With change
    print("\n[Scenario 2: With Change - Buy Water Bottle ($15)]")
    vm.insert_coin(Coin.QUARTER)
    vm.select_product("C1")
    vm.display_status()

    # Scenario 3: Insufficient funds then add more
    print("\n[Scenario 3: Insufficient Funds]")
    vm.insert_coin(Coin.DIME)
    vm.select_product("B1")  # $30, only $10
    vm.insert_coin(Coin.DIME)
    vm.insert_coin(Coin.DIME)
    vm.select_product("B1")  # Now $30
    vm.display_status()

    # Scenario 4: Cancel transaction
    print("\n[Scenario 4: Cancel Transaction]")
    vm.insert_note(Note.FIFTY)
    vm.insert_coin(Coin.QUARTER)
    print(f"    Balance before cancel: ${vm.current_balance:.2f}")
    vm.cancel()
    vm.display_status()

    # Scenario 5: Out of stock
    print("\n[Scenario 5: Out of Stock]")
    vm.insert_note(Note.FIFTY)
    vm.select_product("C2")  # Buy the only Energy Drink
    vm.insert_note(Note.FIFTY)
    vm.select_product("C2")  # Out of stock!
    vm.cancel()

    # Scenario 6: Invalid product code
    print("\n[Scenario 6: Invalid Product Code]")
    vm.insert_coin(Coin.DIME)
    vm.select_product("Z9")
    vm.cancel()

    # Scenario 7: Select without money
    print("\n[Scenario 7: Select Without Money]")
    vm.select_product("A1")

    # Final state
    print("\n--- Final Inventory ---")
    vm.inventory.display()
    vm.display_status()

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
