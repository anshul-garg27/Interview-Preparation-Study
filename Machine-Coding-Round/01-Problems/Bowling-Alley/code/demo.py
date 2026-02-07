"""Full simulation demonstrating the Bowling Alley system.

Features a 2-player game, scorecard display, and a perfect game test (300).
Run: cd code/ && python demo.py
"""

from player import Player
from game import Game
from scorecard import Scorecard
from bowling_alley import BowlingAlley


def print_separator(title: str = "") -> None:
    """Print a formatted section separator."""
    print()
    if title:
        print(f"{'=' * 64}")
        print(f"  {title}")
        print(f"{'=' * 64}")
    else:
        print("-" * 64)


def play_two_player_game(alley: BowlingAlley) -> None:
    """Simulate a full 2-player game on a lane."""
    alice = Player("Alice")
    bob = Player("Bob")

    # Book a lane
    print("\n--- Booking Lane ---")
    booking = alley.book_lane("6:00 PM - 7:00 PM", [alice, bob], lane_id=1)
    print(f"  [+] {booking}")

    # Start game
    lane = alley.get_lane(1)
    games = alley.start_game_on_lane(lane, [alice, bob])
    game_alice = games[0]
    game_bob = games[1]

    print(f"\n--- Game Started on Lane {lane.lane_id} ---")

    # Alice's rolls (10 frames)
    alice_rolls = [
        # Frame 1: 7, 2 (Open: 9)
        (7, 2),
        # Frame 2: Strike
        (10,),
        # Frame 3: 3, 7 (Spare)
        (3, 7),
        # Frame 4: Strike
        (10,),
        # Frame 5: Strike
        (10,),
        # Frame 6: 8, 1 (Open: 9)
        (8, 1),
        # Frame 7: 6, 4 (Spare)
        (6, 4),
        # Frame 8: Strike
        (10,),
        # Frame 9: 9, 1 (Spare)
        (9, 1),
        # Frame 10: Strike, 8, 1
        (10, 8, 1),
    ]

    # Bob's rolls (10 frames)
    bob_rolls = [
        # Frame 1: Strike
        (10,),
        # Frame 2: 8, 2 (Spare)
        (8, 2),
        # Frame 3: 7, 1 (Open: 8)
        (7, 1),
        # Frame 4: Strike
        (10,),
        # Frame 5: 6, 3 (Open: 9)
        (6, 3),
        # Frame 6: Strike
        (10,),
        # Frame 7: Strike
        (10,),
        # Frame 8: 5, 4 (Open: 9)
        (5, 4),
        # Frame 9: Strike
        (10,),
        # Frame 10: 7, 3, 10 (Spare + bonus strike)
        (7, 3, 10),
    ]

    # Simulate frame by frame (players alternate)
    print("\n--- Frame by Frame ---")
    for frame_idx in range(10):
        print(f"\n  Frame {frame_idx + 1}:")

        # Alice's turn
        for pins in alice_rolls[frame_idx]:
            desc = game_alice.roll(pins)
            print(f"    {desc}")

        # Bob's turn
        for pins in bob_rolls[frame_idx]:
            desc = game_bob.roll(pins)
            print(f"    {desc}")

    # Display final scorecards
    print_separator()
    print("--- Final Scorecards ---\n")
    Scorecard.display_multi_player([game_alice, game_bob])


def test_perfect_game() -> None:
    """Test a perfect game scoring 300 points."""
    print_separator()
    print("--- Perfect Game Test (300) ---\n")

    perfect_player = Player("Perfect Player")
    game = Game(perfect_player)

    # 12 strikes for a perfect game
    for i in range(12):
        desc = game.roll(10)
        print(f"  Roll {i + 1}: {desc}")

    print(f"\n  Final Score: {game.get_score()}")
    assert game.get_score() == 300, f"Expected 300 but got {game.get_score()}"
    print("  [PASS] Perfect game scores 300!")

    print()
    Scorecard.display_scorecard(game)


def test_gutter_game() -> None:
    """Test a gutter game scoring 0 points."""
    print_separator()
    print("--- Gutter Game Test (0) ---\n")

    gutter_player = Player("Gutter Player")
    game = Game(gutter_player)

    for i in range(20):  # 20 rolls of 0
        game.roll(0)

    print(f"  Final Score: {game.get_score()}")
    assert game.get_score() == 0, f"Expected 0 but got {game.get_score()}"
    print("  [PASS] Gutter game scores 0!")

    print()
    Scorecard.display_scorecard(game)


def test_all_spares() -> None:
    """Test a game with all spares (5,5 each frame + 5 bonus)."""
    print_separator()
    print("--- All Spares Test (150) ---\n")

    spare_player = Player("Spare Master")
    game = Game(spare_player)

    # Frames 1-9: 5, 5 (spare)
    for _ in range(9):
        game.roll(5)
        game.roll(5)
    # Frame 10: 5, 5, 5
    game.roll(5)
    game.roll(5)
    game.roll(5)

    print(f"  Final Score: {game.get_score()}")
    assert game.get_score() == 150, f"Expected 150 but got {game.get_score()}"
    print("  [PASS] All spares game scores 150!")

    print()
    Scorecard.display_scorecard(game)


def test_error_handling() -> None:
    """Test error handling for invalid inputs."""
    print_separator()
    print("--- Error Handling Tests ---\n")

    player = Player("Test")
    game = Game(player)

    # Test: roll more pins than remaining
    game.roll(7)
    try:
        game.roll(5)  # Only 3 pins remaining
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Test: negative pins
    try:
        game2 = Game(Player("Test2"))
        game2.roll(-1)
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Test: pins > 10
    try:
        game3 = Game(Player("Test3"))
        game3.roll(11)
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Test: empty player name
    try:
        Player("")
    except ValueError as e:
        print(f"  [ERROR] {e}")


def main() -> None:
    """Run the bowling alley simulation."""
    print_separator("BOWLING ALLEY SIMULATION")

    # Setup alley
    print("\n--- Setting Up ---")
    alley = BowlingAlley("StrikeZone", num_lanes=4)
    print(f"  Bowling Alley: \"{alley.name}\" ({len(alley.lanes)} lanes)")

    available = alley.get_available_lanes()
    lane_names = ", ".join(str(l) for l in available)
    print(f"  Available lanes: {lane_names}")

    # Play a 2-player game
    play_two_player_game(alley)

    # Special scoring tests
    test_perfect_game()
    test_gutter_game()
    test_all_spares()
    test_error_handling()

    # Release lane
    print_separator()
    print("--- Releasing Lane ---")
    alley.release_lane(1)
    print(f"  Lane 1 released: {alley.get_lane(1)}")

    print_separator("SIMULATION COMPLETE")
    print()


if __name__ == "__main__":
    main()
