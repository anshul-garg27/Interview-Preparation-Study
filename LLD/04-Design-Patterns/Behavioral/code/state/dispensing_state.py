"""DispensingState - dispensing the selected item."""

from state import VendingMachineState


class DispensingState(VendingMachineState):
    def insert_money(self, machine, amount: float) -> str:
        return "Please wait, dispensing in progress"

    def select_item(self, machine, item: str) -> str:
        return "Please wait, dispensing in progress"

    def dispense(self, machine) -> str:
        item = machine.selected_item
        price = machine.get_price(item)
        machine.balance -= price
        change = machine.balance
        machine.balance = 0
        machine.selected_item = None

        from idle_state import IdleState
        machine.set_state(IdleState())

        msg = f"Dispensed '{item}'"
        if change > 0:
            msg += f". Change: ${change:.2f}"
        return msg
