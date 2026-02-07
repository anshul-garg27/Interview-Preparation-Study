"""Scorecard display for formatted bowling game output."""

from typing import List, Optional

from game import Game


class Scorecard:
    """Displays formatted bowling scorecards.

    Renders a tabular scorecard with frame numbers, roll details,
    and running cumulative scores.
    """

    @staticmethod
    def display_scorecard(game: Game) -> None:
        """Display a formatted scorecard for a single game.

        Args:
            game: The game to display.
        """
        name = game.player.name.upper()
        scores = game.get_frame_scores()

        # Header
        top_border = "+" + "-" * 62 + "+"
        print(top_border)
        print(f"|  {name}'s SCORECARD{' ' * (43 - len(name))}|")

        # Frame numbers row
        frame_nums = "|"
        for i in range(1, 11):
            frame_nums += f" {i:^5}|"
        print("+" + "+".join(["-----"] * 9) + "+-------+")
        print(frame_nums)

        # Rolls row
        rolls_row = "|"
        for i, frame in enumerate(game.frames):
            display = frame.display_rolls()
            if i == 9:  # 10th frame is wider
                rolls_row += f" {display:<5} |"
            else:
                rolls_row += f" {display:<3} |"
        print(rolls_row)

        # Scores row
        scores_row = "|"
        for i, score in enumerate(scores):
            score_str = str(score) if score is not None else ""
            if i == 9:
                scores_row += f" {score_str:^5} |"
            else:
                scores_row += f" {score_str:^3} |"
        print(scores_row)

        # Bottom border
        print("+" + "+".join(["-----"] * 9) + "+-------+")

        # Final score
        final_score = game.get_score()
        print(f"|  FINAL SCORE: {final_score}{' ' * (47 - len(str(final_score)))}|")
        print(top_border)

    @staticmethod
    def display_multi_player(games: List[Game]) -> None:
        """Display scorecards for multiple players.

        Args:
            games: List of games (one per player).
        """
        for game in games:
            Scorecard.display_scorecard(game)
            print()

        # Leaderboard
        print("+" + "-" * 40 + "+")
        print(f"|  {'LEADERBOARD':<38} |")
        print("+" + "-" * 40 + "+")
        sorted_games = sorted(games, key=lambda g: g.get_score(), reverse=True)
        for rank, game in enumerate(sorted_games, 1):
            line = f"{rank}. {game.player.name}: {game.get_score()}"
            print(f"|  {line:<38} |")
        print("+" + "-" * 40 + "+")
