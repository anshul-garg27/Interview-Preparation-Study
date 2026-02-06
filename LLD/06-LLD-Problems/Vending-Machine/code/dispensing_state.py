"""Dispensing state - product being dispensed with change calculation."""

from state import VendingMachineState
from change_calculator import ChangeCalculator


class DispensingState(VendingMachineState):
    """Product is being dispensed."""

    def insert_coin(self, machine: "VendingMachine", value: int) -> None:
        print("    [Error] Dispensing in progress. Please wait.")

    def select_product(self, machine: "VendingMachine", code: str) -> None:
        print("    [Error] Dispensing in progress. Please wait.")

    def dispense(self, machine: "VendingMachine") -> None:
        product = machine.selected_product
        change_amount = round(machine.current_balance - product.price)

        if change_amount > 0:
            change = ChangeCalculator.make_change(change_amount)
            if change:
                change_str = ", ".join(
                    f"${v}x{c}" for v, c in change.items()
                )
                print(f"    [Change] Returning ${change_amount} ({change_str})")
            else:
                print(f"    [Change] Returning ${change_amount}")
        else:
            print("    [Change] No change needed (exact amount).")

        machine.inventory.dispense(product.code)
        print(f"    [Dispense] '{product.name}' dispensed! Enjoy!")
        machine.total_sales += product.price

        machine.current_balance = 0
        machine.selected_product = None
        from idle_state import IdleState
        machine.set_state(IdleState())

    def cancel(self, machine: "VendingMachine") -> None:
        print("    [Error] Cannot cancel during dispensing.")

    def name(self) -> str:
        return "DISPENSING"
