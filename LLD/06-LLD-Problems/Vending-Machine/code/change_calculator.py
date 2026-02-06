"""Greedy change calculator for the vending machine."""

from enums import Coin


class ChangeCalculator:
    """Calculate change using fewest coins (greedy algorithm)."""

    DENOMINATIONS = sorted([c.value for c in Coin], reverse=True)

    @staticmethod
    def make_change(amount: int) -> dict[int, int] | None:
        """
        Return change as {denomination_value: count} using fewest coins.
        Returns None if exact change cannot be made.
        """
        remaining = amount
        change: dict[int, int] = {}

        for denom in ChangeCalculator.DENOMINATIONS:
            if remaining <= 0:
                break
            count = remaining // denom
            if count > 0:
                change[denom] = count
                remaining -= count * denom

        if remaining > 0:
            return None
        return change
