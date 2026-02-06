"""
Board for Snake and Ladder game.
Manages snakes, ladders, and position resolution.
"""

from typing import Optional

from snake import Snake
from ladder import Ladder


class Board:
    """Game board with snakes and ladders."""

    def __init__(self, size: int = 100):
        """
        Args:
            size: Total number of squares on the board.
        """
        self.size = size
        self.snakes: dict[int, Snake] = {}    # head_position -> Snake
        self.ladders: dict[int, Ladder] = {}  # bottom_position -> Ladder

    def add_snake(self, snake: Snake) -> None:
        """Add a snake to the board."""
        self.snakes[snake.head] = snake

    def add_ladder(self, ladder: Ladder) -> None:
        """Add a ladder to the board."""
        self.ladders[ladder.start] = ladder

    def get_new_position(self, position: int) -> tuple[int, Optional[str]]:
        """
        Check for snake/ladder at the given position.

        Returns:
            Tuple of (final_position, event_message_or_None).
        """
        if position in self.snakes:
            snake = self.snakes[position]
            return snake.tail, f"SNAKE! Slid from {snake.head} to {snake.tail}"
        if position in self.ladders:
            ladder = self.ladders[position]
            return ladder.end, f"LADDER! Climbed from {ladder.start} to {ladder.end}"
        return position, None

    def display(self) -> None:
        """Print a visual representation of the board."""
        print(f"\n    Board ({self.size} squares)")
        print(f"    Snakes  (head->tail): ", end="")
        for s in self.snakes.values():
            print(f"{s.head}->{s.tail}  ", end="")
        print()
        print(f"    Ladders (bottom->top): ", end="")
        for l in self.ladders.values():
            print(f"{l.start}->{l.end}  ", end="")
        print()

        # Visual board (10x10 grid, bottom-to-top, snake-style numbering)
        print()
        cols = 10
        rows = self.size // cols
        for row in range(rows, 0, -1):
            start = (row - 1) * cols + 1
            end = row * cols
            cells = list(range(start, end + 1))
            if row % 2 == 0:
                cells = list(reversed(cells))

            row_str = "    "
            for cell in cells:
                marker = "  "
                if cell in self.snakes:
                    marker = "S "
                elif cell in self.ladders:
                    marker = "L "
                row_str += f"|{cell:3d}{marker}"
            row_str += "|"
            print(row_str)
        print()
