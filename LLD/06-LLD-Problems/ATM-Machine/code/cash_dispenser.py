"""
CashDispenser using Chain of Responsibility pattern.
Denomination chain: $100 -> $50 -> $20 -> $10.
"""

from __future__ import annotations

from typing import Optional
from abc import ABC


class DenominationDispenser(ABC):
    """Base class for denomination handlers in the chain."""

    def __init__(self, denomination: int):
        self.denomination = denomination
        self._next: Optional[DenominationDispenser] = None

    def set_next(self, dispenser: DenominationDispenser) -> DenominationDispenser:
        """Set the next handler in the chain."""
        self._next = dispenser
        return dispenser

    def dispense(self, amount: int, inventory: dict[int, int],
                 result: dict[int, int]) -> int:
        """
        Dispense as much as possible at this denomination, then pass remaining
        to the next handler in the chain.

        Returns:
            Remaining amount that could not be dispensed.
        """
        if amount >= self.denomination and inventory.get(self.denomination, 0) > 0:
            num_notes = min(amount // self.denomination, inventory[self.denomination])
            if num_notes > 0:
                result[self.denomination] = num_notes
                inventory[self.denomination] -= num_notes
                amount -= num_notes * self.denomination

        if amount > 0 and self._next:
            return self._next.dispense(amount, inventory, result)
        return amount


class HundredDispenser(DenominationDispenser):
    def __init__(self):
        super().__init__(100)


class FiftyDispenser(DenominationDispenser):
    def __init__(self):
        super().__init__(50)


class TwentyDispenser(DenominationDispenser):
    def __init__(self):
        super().__init__(20)


class TenDispenser(DenominationDispenser):
    def __init__(self):
        super().__init__(10)


class CashDispenser:
    """
    Manages cash inventory and uses a chain of denomination dispensers
    to fulfil withdrawal requests ($100 -> $50 -> $20 -> $10).
    """

    def __init__(self):
        self.denominations: dict[int, int] = {100: 10, 50: 10, 20: 10, 10: 10}
        self._build_chain()

    def _build_chain(self) -> None:
        """Build the Chain of Responsibility: $100 -> $50 -> $20 -> $10."""
        self._chain = HundredDispenser()
        fifty = FiftyDispenser()
        twenty = TwentyDispenser()
        ten = TenDispenser()
        self._chain.set_next(fifty)
        fifty.set_next(twenty)
        twenty.set_next(ten)

    def dispense(self, amount: int) -> Optional[dict[int, int]]:
        """
        Attempt to dispense the exact amount.

        Returns:
            Dict of {denomination: count} on success, None if not possible.
        """
        if amount <= 0 or amount % 10 != 0:
            return None
        if amount > self.total_cash():
            return None

        # Work on a copy to avoid partial dispensing
        inventory_copy = dict(self.denominations)
        result: dict[int, int] = {}
        remainder = self._chain.dispense(amount, inventory_copy, result)

        if remainder > 0:
            return None  # Cannot dispense exact amount

        # Commit the inventory change
        self.denominations = inventory_copy
        return result

    def add_cash(self, denomination: int, count: int) -> None:
        """Add notes to the inventory."""
        if denomination in self.denominations:
            self.denominations[denomination] += count

    def total_cash(self) -> int:
        """Return total cash available in the ATM."""
        return sum(d * c for d, c in self.denominations.items())

    def __str__(self) -> str:
        parts = [f"${d}x{c}" for d, c in sorted(self.denominations.items(), reverse=True)]
        return f"Inventory: {', '.join(parts)} (Total: ${self.total_cash()})"
