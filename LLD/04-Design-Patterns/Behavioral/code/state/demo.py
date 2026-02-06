"""Demo: State pattern - vending machine simulation."""

from context import VendingMachine


def main():
    print("=" * 50)
    print("STATE PATTERN")
    print("=" * 50)

    vm = VendingMachine()

    # Try without money
    print(f"\n--- State: {vm.state_name} ---")
    print(f"  {vm.select_item('Cola')}")

    # Insert money and buy
    print(f"\n--- Insert Money ---")
    print(f"  {vm.insert_money(2.00)}")
    print(f"  State: {vm.state_name}")

    print(f"\n--- Select Item ---")
    print(f"  {vm.select_item('Cola')}")
    print(f"  State: {vm.state_name}")

    print(f"\n--- Dispense ---")
    print(f"  {vm.dispense()}")
    print(f"  State: {vm.state_name}")

    # Not enough money
    print(f"\n--- Insufficient Funds ---")
    print(f"  {vm.insert_money(0.50)}")
    print(f"  {vm.select_item('Cola')}")


if __name__ == "__main__":
    main()
