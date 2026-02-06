"""Chess Game demo - Scholar's Mate (4-move checkmate)."""

from game import Game


def main():
    print("=" * 60)
    print("  CHESS GAME - LLD Demo")
    print("=" * 60)

    # Scholar's Mate (4-move checkmate)
    print("\n[Demo: Scholar's Mate - 4 Move Checkmate]")
    print("  White mates Black in just 4 moves!\n")

    game = Game("Alice", "Bob")
    game.board.display()

    # Move 1: e2-e4, e7-e5
    game.make_move("e2", "e4")
    game.make_move("e7", "e5")

    # Move 2: Bf1-c4, Nb8-c6
    game.make_move("f1", "c4")
    game.make_move("b8", "c6")

    # Move 3: Qd1-h5, Ng8-f6 (Black blunders)
    game.make_move("d1", "h5")
    game.make_move("g8", "f6")

    game.board.display()
    print("  White Queen on h5 targets f7. Black Knight can't save f7.\n")

    # Move 4: Qh5xf7# (Checkmate!)
    game.make_move("h5", "f7")
    game.board.display()

    # Print move history
    print("  Move History:")
    for i, move in enumerate(game.move_history, 1):
        print(f"    {i}. {move}")

    print(f"\n  Winner: {game.winner}")

    # Invalid move demo
    print(f"\n{'=' * 60}")
    print("[Demo: Invalid Move Handling]")
    game2 = Game()
    print("\n  Trying invalid moves:")
    game2.make_move("e2", "e5")  # Pawn can't jump 3
    game2.make_move("b1", "b3")  # Knight can't go to b3
    game2.make_move("e7", "e5")  # Not black's turn

    print("\n  Valid opening moves:")
    game2.make_move("e2", "e4")
    game2.make_move("d7", "d5")
    game2.make_move("e4", "d5")  # Pawn captures
    game2.board.display()

    print("Demo complete!")


if __name__ == "__main__":
    main()
