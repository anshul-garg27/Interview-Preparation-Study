"""
Game engine for Snake and Ladder.
Manages turns, win detection, and the game loop.
"""

from typing import Optional

from board import Board
from player import Player
from dice import DiceStrategy, Dice


class Game:
    """Orchestrates the Snake and Ladder game."""

    def __init__(self, board: Board, players: list[Player],
                 dice: DiceStrategy | Dice):
        """
        Args:
            board: The game board.
            players: List of players.
            dice: Dice strategy or configurable Dice instance.
        """
        self.board = board
        self.players = players
        self.dice = dice
        self.current_player_index: int = 0
        self.is_over: bool = False
        self.winner: Optional[Player] = None
        self.turn_count: int = 0

    def play_turn(self) -> bool:
        """
        Play one turn for the current player.

        Returns:
            True if the game should continue, False if over.
        """
        if self.is_over:
            return False

        player = self.players[self.current_player_index]
        roll = self.dice.roll()
        self.turn_count += 1

        new_pos = player.position + roll

        # Cannot exceed the board size (must land exactly)
        if new_pos > self.board.size:
            print(f"    Turn {self.turn_count:3d}: {player.name:10s} at {player.position:3d} "
                  f"| Rolled {roll:2d} | Bounce! (would go to {new_pos}) | "
                  f"Stays at {player.position}")
            self._next_player()
            return True

        # Check for snake/ladder
        final_pos, event = self.board.get_new_position(new_pos)
        event_str = f" | {event}" if event else ""

        player.position = final_pos

        # Check win condition
        if player.position == self.board.size:
            player.has_won = True
            self.is_over = True
            self.winner = player
            print(f"    Turn {self.turn_count:3d}: {player.name:10s} "
                  f"| Rolled {roll:2d} | Reached {self.board.size}!")
            return False

        print(f"    Turn {self.turn_count:3d}: {player.name:10s} at "
              f"{player.position - roll if player.position == new_pos else '':>3} "
              f"| Rolled {roll:2d} -> {new_pos:3d}{event_str} | Now at {player.position}")

        self._next_player()
        return True

    def _next_player(self) -> None:
        """Advance to the next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def play(self, max_turns: int = 500) -> None:
        """
        Run the full game loop until a player wins or max_turns is reached.

        Args:
            max_turns: Safety limit to prevent infinite games.
        """
        print(f"\n    Using: {self.dice.name()}")
        print(f"    Players: {', '.join(p.name for p in self.players)}")
        self.board.display()

        print(f"    {'='*70}")
        print(f"    Game begins!\n")

        while not self.is_over and self.turn_count < max_turns:
            self.play_turn()

        print(f"\n    {'='*70}")
        if self.winner:
            print(f"    WINNER: {self.winner.name} in {self.turn_count} turns!")
        else:
            print(f"    Game ended after {max_turns} turns (no winner).")

        # Final standings
        print(f"\n    Final Positions:")
        sorted_players = sorted(self.players, key=lambda p: p.position, reverse=True)
        for i, p in enumerate(sorted_players, 1):
            status = "WINNER" if p.has_won else f"pos {p.position}"
            print(f"      {i}. {p.name:10s} - {status}")
