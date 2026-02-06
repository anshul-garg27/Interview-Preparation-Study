"""
Dice module for Snake and Ladder game.
Provides configurable dice with strategy pattern support.
"""

import random
from abc import ABC, abstractmethod


class DiceStrategy(ABC):
    """Abstract base for dice rolling strategies."""

    @abstractmethod
    def roll(self) -> int:
        """Roll the dice and return the result."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return a human-readable name for this dice strategy."""
        pass


class SingleDice(DiceStrategy):
    """Single six-sided die."""

    def roll(self) -> int:
        return random.randint(1, 6)

    def name(self) -> str:
        return "Single Die (1d6)"


class DoubleDice(DiceStrategy):
    """Two six-sided dice."""

    def roll(self) -> int:
        return random.randint(1, 6) + random.randint(1, 6)

    def name(self) -> str:
        return "Double Dice (2d6)"


class Dice:
    """Configurable dice supporting N dice of M sides each."""

    def __init__(self, num_dice: int = 1, sides: int = 6):
        """
        Args:
            num_dice: Number of dice to roll.
            sides: Number of sides per die.
        """
        if num_dice < 1 or sides < 1:
            raise ValueError("num_dice and sides must be positive integers")
        self.num_dice = num_dice
        self.sides = sides

    def roll(self) -> int:
        """Roll all dice and return the total."""
        return sum(random.randint(1, self.sides) for _ in range(self.num_dice))

    def name(self) -> str:
        return f"{self.num_dice}d{self.sides}"


class LoadedDice(DiceStrategy):
    """Deterministic dice for testing (cycles through given values)."""

    def __init__(self, values: list[int]):
        self.values = values
        self.index = 0

    def roll(self) -> int:
        val = self.values[self.index % len(self.values)]
        self.index += 1
        return val

    def name(self) -> str:
        return "Loaded Dice (deterministic)"
