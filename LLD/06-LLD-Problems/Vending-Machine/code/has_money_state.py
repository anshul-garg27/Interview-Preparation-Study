"""HasMoney state - money inserted, waiting for product selection."""

from state import VendingMachineState


class HasMoneyState(VendingMachineState):
    """Money has been inserted, awaiting product selection."""

    def insert_coin(self, machine: "VendingMachine", value: int) -> None:
        machine.current_balance += value
        print(f"    [Insert] ${value} | Balance: ${machine.current_balance:.2f}")

    def select_product(self, machine: "VendingMachine", code: str) -> None:
        product = machine.inventory.get_product(code)
        if not product:
            print(f"    [Error] Invalid product code: {code}")
            return
        if not machine.inventory.is_available(code):
            print(f"    [Error] '{product.name}' is out of stock!")
            return
        if machine.current_balance < product.price:
            deficit = product.price - machine.current_balance
            print(f"    [Error] Insufficient funds. Need ${deficit:.2f} more.")
            return

        machine.selected_product = product
        print(f"    [Select] '{product.name}' selected (${product.price:.2f})")
        from dispensing_state import DispensingState
        machine.set_state(DispensingState())
        machine.state.dispense(machine)

    def dispense(self, machine: "VendingMachine") -> None:
        print("    [Error] Please select a product first.")

    def cancel(self, machine: "VendingMachine") -> None:
        print(f"    [Cancel] Refunding ${machine.current_balance:.2f}")
        machine._refund()
        from idle_state import IdleState
        machine.set_state(IdleState())

    def name(self) -> str:
        return "HAS_MONEY"
