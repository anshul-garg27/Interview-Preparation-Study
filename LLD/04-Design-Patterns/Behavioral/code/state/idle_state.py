"""IdleState - waiting for money."""

from state import VendingMachineState


class IdleState(VendingMachineState):
    def insert_money(self, machine, amount: float) -> str:
        machine.balance = amount
        from has_money_state import HasMoneyState
        machine.set_state(HasMoneyState())
        return f"Inserted ${amount:.2f}"

    def select_item(self, machine, item: str) -> str:
        return "Please insert money first"

    def dispense(self, machine) -> str:
        return "Please insert money first"
