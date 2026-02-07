"""Full simulation demonstrating the Cricket Scoreboard system.

Simulates a 5-over match between India and Australia ball-by-ball.
Run: cd code/ && python demo.py
"""

from enums import BallType, WicketType
from player import Player
from team import Team
from match import Match
from scoring_engine import ScoringEngine
from scoreboard import Scoreboard


def print_separator(title: str = "") -> None:
    """Print a formatted section separator."""
    print()
    if title:
        print(f"{'=' * 62}")
        print(f"  {title}")
        print(f"{'=' * 62}")
    else:
        print("-" * 62)


def simulate_first_innings(engine: ScoringEngine, match: Match) -> None:
    """Simulate India's batting innings (5 overs)."""
    innings = match.start_first_innings()

    # Get bowlers
    aus = match.team2
    starc = aus.get_player("Starc")
    cummins = aus.get_player("Cummins")
    zampa = aus.get_player("Zampa")
    hazlewood = aus.get_player("Hazlewood")
    maxwell = aus.get_player("Maxwell")

    # ---- Over 1: Starc ----
    print("\n--- Over 1 (Bowler: Starc) ---")
    engine.change_bowler(starc)
    balls = [
        (BallType.NORMAL, 4, False, None, None),       # FOUR
        (BallType.NORMAL, 1, False, None, None),        # single
        (BallType.NORMAL, 0, False, None, None),        # dot
        (BallType.WIDE, 0, False, None, None),          # wide
        (BallType.NORMAL, 2, False, None, None),        # two
        (BallType.NORMAL, 6, False, None, None),        # SIX
        (BallType.NORMAL, 1, False, None, None),        # single
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    print("\n--- Scoreboard after Over 1 ---")
    Scoreboard.display_innings_summary(innings)

    # ---- Over 2: Cummins ----
    print("\n--- Over 2 (Bowler: Cummins) ---")
    engine.change_bowler(cummins)
    balls = [
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 4, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.CAUGHT, "Smith"),  # WICKET!
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 2, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    print("\n--- Scoreboard after Over 2 ---")
    Scoreboard.display_innings_summary(innings)

    # ---- Over 3: Zampa ----
    print("\n--- Over 3 (Bowler: Zampa) ---")
    engine.change_bowler(zampa)
    balls = [
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 6, False, None, None),
        (BallType.NO_BALL, 1, False, None, None),       # no-ball
        (BallType.NORMAL, 2, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 4, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    # ---- Over 4: Hazlewood ----
    print("\n--- Over 4 (Bowler: Hazlewood) ---")
    engine.change_bowler(hazlewood)
    balls = [
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.BOWLED, None),  # WICKET!
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.LEG_BYE, 2, False, None, None),
        (BallType.NORMAL, 4, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    # ---- Over 5: Maxwell ----
    print("\n--- Over 5 (Bowler: Maxwell) ---")
    engine.change_bowler(maxwell)
    balls = [
        (BallType.NORMAL, 6, False, None, None),
        (BallType.NORMAL, 2, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.LBW, None),  # WICKET!
        (BallType.NORMAL, 4, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    match.end_current_innings()
    print("\n--- FIRST INNINGS COMPLETE ---")
    Scoreboard.display_innings_summary(innings)


def simulate_second_innings(engine: ScoringEngine, match: Match) -> None:
    """Simulate Australia's chase."""
    innings = match.start_second_innings()
    target = innings.target
    print(f"\n  Target: {target} runs")

    ind = match.team1
    bumrah = ind.get_player("Bumrah")
    ashwin = ind.get_player("Ashwin")
    siraj = ind.get_player("Siraj")
    jadeja = ind.get_player("Jadeja")
    shami = ind.get_player("Shami")

    # Over 1: Bumrah
    print("\n--- Over 1 (Bowler: Bumrah) ---")
    engine.change_bowler(bumrah)
    balls = [
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 4, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.BOWLED, None),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    # Over 2: Ashwin
    print("\n--- Over 2 (Bowler: Ashwin) ---")
    engine.change_bowler(ashwin)
    balls = [
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 6, False, None, None),
        (BallType.NORMAL, 2, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.STUMPED, "Pant"),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 4, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    # Over 3: Siraj
    print("\n--- Over 3 (Bowler: Siraj) ---")
    engine.change_bowler(siraj)
    balls = [
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.WIDE, 0, False, None, None),
        (BallType.NORMAL, 4, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.CAUGHT, "Kohli"),
        (BallType.NORMAL, 2, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    # Over 4: Jadeja
    print("\n--- Over 4 (Bowler: Jadeja) ---")
    engine.change_bowler(jadeja)
    balls = [
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 6, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 2, False, None, None),
        (BallType.NORMAL, 0, True, WicketType.RUN_OUT, "Jadeja"),
    ]
    for bt, r, w, wt, f in balls:
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    # Over 5: Shami
    print("\n--- Over 5 (Bowler: Shami) ---")
    engine.change_bowler(shami)
    balls = [
        (BallType.NORMAL, 4, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
        (BallType.NORMAL, 2, False, None, None),
        (BallType.NORMAL, 1, False, None, None),
        (BallType.NORMAL, 0, False, None, None),
    ]
    for bt, r, w, wt, f in balls:
        if innings.status.value == "COMPLETED":
            break
        desc = engine.process_ball(bt, r, w, wt, f)
        print(f"  {desc}")

    match.end_current_innings()
    print("\n--- SECOND INNINGS COMPLETE ---")
    Scoreboard.display_innings_summary(innings)


def main() -> None:
    """Run the cricket scoreboard simulation."""
    print_separator("CRICKET SCOREBOARD SIMULATION")

    # Create India team
    india_players = [
        Player("Rohit", True, False),
        Player("Kohli", True, False),
        Player("Pant", True, False),
        Player("Hardik", True, True),
        Player("Jadeja", True, True),
        Player("Ashwin", True, True),
        Player("Bumrah", False, True),
        Player("Siraj", False, True),
        Player("Shami", False, True),
        Player("Chahal", False, True),
        Player("Gill", True, False),
    ]
    india = Team("India", india_players)

    # Create Australia team
    aus_players = [
        Player("Warner", True, False),
        Player("Smith", True, False),
        Player("Labuschagne", True, False),
        Player("Head", True, False),
        Player("Maxwell", True, True),
        Player("Carey", True, False),
        Player("Starc", False, True),
        Player("Cummins", False, True),
        Player("Hazlewood", False, True),
        Player("Zampa", False, True),
        Player("Lyon", False, True),
    ]
    australia = Team("Australia", aus_players)

    # Create match (5 overs per side for demo)
    match = Match(india, australia, max_overs=5)
    engine = ScoringEngine(match)

    print(f"\n  {match}")
    print(f"\n=== INNINGS 1: {india.name} Batting ===")

    # Simulate first innings
    simulate_first_innings(engine, match)

    print(f"\n=== INNINGS 2: {australia.name} Batting (Chase) ===")

    # Simulate second innings
    simulate_second_innings(engine, match)

    # Final match result
    Scoreboard.display_match_summary(match)

    print_separator("SIMULATION COMPLETE")
    print()


if __name__ == "__main__":
    main()
