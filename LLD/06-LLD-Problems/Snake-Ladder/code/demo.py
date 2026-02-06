"""
Snake and Ladder Game - Demo
=============================
Runs a 3-player game to completion on a standard 10x10 board.
Design Patterns: Strategy (dice rolling)
"""

import random

from dice import SingleDice, DoubleDice, LoadedDice
from snake import Snake
from ladder import Ladder
from player import Player
from board import Board
from game import Game


def create_standard_board() -> Board:
    """Create a standard 10x10 board with snakes and ladders."""
    board = Board(100)

    # Snakes (head -> tail)
    snakes = [(99, 54), (70, 55), (52, 42), (25, 2), (95, 72), (47, 19)]
    for head, tail in snakes:
        board.add_snake(Snake(head, tail))

    # Ladders (bottom -> top)
    ladders = [(6, 25), (11, 40), (20, 59), (46, 74), (60, 83), (63, 81)]
    for bottom, top in ladders:
        board.add_ladder(Ladder(bottom, top))

    return board


if __name__ == "__main__":
    print("=" * 75)
    print("  SNAKE AND LADDER GAME - LLD Demo")
    print("=" * 75)

    random.seed(42)  # For reproducible demo output

    # -- Game 1: 3-player game with single die --
    print("\n[Game 1: 3-Player Game - Single Die]")
    board = create_standard_board()
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]
    game = Game(board, players, SingleDice())
    game.play(max_turns=200)

    # -- Game 2: 2-player game with double dice --
    print(f"\n{'='*75}")
    print("\n[Game 2: 2-Player Game - Double Dice]")
    random.seed(123)
    board2 = create_standard_board()
    players2 = [Player("Dave"), Player("Eve")]
    game2 = Game(board2, players2, DoubleDice())
    game2.play(max_turns=200)

    # -- Game 3: Deterministic game for testing --
    print(f"\n{'='*75}")
    print("\n[Game 3: Deterministic Game - Loaded Dice (Testing)]")
    board3 = Board(20)
    board3.add_snake(Snake(17, 7))
    board3.add_ladder(Ladder(3, 15))
    loaded = LoadedDice([3, 4, 5])
    players3 = [Player("Test-P1"), Player("Test-P2")]
    game3 = Game(board3, players3, loaded)
    game3.play()

    print("\nDemo complete!")
