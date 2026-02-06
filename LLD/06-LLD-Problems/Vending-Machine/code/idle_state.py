"""Idle state - waiting for money insertion."""

from state import VendingMachineState


class IdleState(VendingMachineState):
    """Machine is idle, waiting for a customer."""

    def insert_coin(self, machine: "VendingMachine", value: int) -> None:
        machine.current_balance += value
        print(f"    [Insert] ${value} | Balance: ${machine.current_balance:.2f}")
        from has_money_state import HasMoneyState
        machine.set_state(HasMoneyState())

    def select_product(self, machine: "VendingMachine", code: str) -> None:
        print("    [Error] Please insert money first.")

    def dispense(self, machine: "VendingMachine") -> None:
        print("    [Error] No transaction in progress.")

    def cancel(self, machine: "VendingMachine") -> None:
        print("    [Info] No transaction to cancel.")

    def name(self) -> str:
        return "IDLE"
