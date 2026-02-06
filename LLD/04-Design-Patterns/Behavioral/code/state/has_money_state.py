"""HasMoneyState - money inserted, waiting for selection."""

from state import VendingMachineState


class HasMoneyState(VendingMachineState):
    def insert_money(self, machine, amount: float) -> str:
        machine.balance += amount
        return f"Added ${amount:.2f}. Balance: ${machine.balance:.2f}"

    def select_item(self, machine, item: str) -> str:
        price = machine.get_price(item)
        if price is None:
            return f"Item '{item}' not available"
        if machine.balance < price:
            return f"Not enough money. Need ${price:.2f}, have ${machine.balance:.2f}"
        machine.selected_item = item
        from dispensing_state import DispensingState
        machine.set_state(DispensingState())
        return f"Selected '{item}' (${price:.2f})"

    def dispense(self, machine) -> str:
        return "Please select an item first"
