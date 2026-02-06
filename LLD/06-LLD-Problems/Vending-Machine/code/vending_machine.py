"""Vending Machine context class (State Pattern)."""

from inventory import Inventory
from idle_state import IdleState
from enums import Coin, Note


class VendingMachine:
    """Vending machine using the State pattern."""

    def __init__(self, machine_id: str):
        self.machine_id = machine_id
        self.inventory = Inventory()
        self.state = IdleState()
        self.current_balance: float = 0.0
        self.selected_product = None
        self.total_sales: float = 0.0

    def set_state(self, state) -> None:
        """Transition to a new state."""
        self.state = state

    def insert_coin(self, coin: Coin) -> None:
        """Insert a coin into the machine."""
        self.state.insert_coin(self, coin.value)

    def insert_note(self, note: Note) -> None:
        """Insert a note into the machine."""
        self.state.insert_coin(self, note.value)

    def select_product(self, code: str) -> None:
        """Select a product by code."""
        self.state.select_product(self, code)

    def cancel(self) -> None:
        """Cancel current transaction."""
        self.state.cancel(self)

    def _refund(self) -> None:
        """Return all inserted money."""
        self.current_balance = 0
        self.selected_product = None

    def display_status(self) -> None:
        """Print machine status."""
        print(f"\n    Machine: {self.machine_id} | "
              f"State: {self.state.name()} | "
              f"Balance: ${self.current_balance:.2f} | "
              f"Total Sales: ${self.total_sales:.2f}")
