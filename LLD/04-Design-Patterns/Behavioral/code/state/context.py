"""VendingMachine context that delegates to current state."""

from idle_state import IdleState


class VendingMachine:
    """Context that changes behavior based on its current state."""

    def __init__(self):
        self._state = IdleState()
        self.balance = 0.0
        self.selected_item = None
        self._items = {"Cola": 1.50, "Chips": 1.00, "Water": 0.75}

    def set_state(self, state):
        self._state = state

    def get_price(self, item: str):
        return self._items.get(item)

    def insert_money(self, amount: float) -> str:
        return self._state.insert_money(self, amount)

    def select_item(self, item: str) -> str:
        return self._state.select_item(self, item)

    def dispense(self) -> str:
        return self._state.dispense(self)

    @property
    def state_name(self):
        return type(self._state).__name__
