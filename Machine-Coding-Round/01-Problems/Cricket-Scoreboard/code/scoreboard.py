"""Scoreboard display for formatted cricket match output."""

from innings import Innings
from match import Match


class Scoreboard:
    """Displays formatted cricket scoreboard with batting/bowling cards.

    Provides methods to render batting card, bowling card, and
    complete match summary in a tabular format.
    """

    SEPARATOR = "+" + "-" * 60 + "+"
    HEADER_SEP = "+" + "=" * 60 + "+"

    @staticmethod
    def display_batting_card(innings: Innings) -> None:
        """Display the formatted batting card.

        Args:
            innings: The innings to display batting stats for.
        """
        print(Scoreboard.SEPARATOR)
        print(f"| {'BATTING':<58} |")
        print(Scoreboard.SEPARATOR)
        print(f"| {'Batsman':<15} {'Status':<20} {'R':>4} {'B':>4} {'4s':>3} {'6s':>3} {'SR':>8} |")
        print(Scoreboard.SEPARATOR)

        for stats in innings.batting_card:
            marker = ""
            if not stats.is_out:
                if innings.striker and stats.player == innings.striker.player:
                    marker = " *"
                elif innings.non_striker and stats.player == innings.non_striker.player:
                    marker = ""
            name = stats.player.name + marker
            status = stats.dismissal_info
            print(
                f"| {name:<15} {status:<20} "
                f"{stats.runs:>4} {stats.balls_faced:>4} "
                f"{stats.fours:>3} {stats.sixes:>3} "
                f"{stats.strike_rate:>7.2f} |"
            )

        print(Scoreboard.SEPARATOR)

        # Extras
        extras_parts = []
        for key, val in innings.extras.items():
            if val > 0:
                extras_parts.append(f"{key}: {val}")
        extras_str = ", ".join(extras_parts) if extras_parts else "0"
        print(f"| {'Extras: ' + extras_str:<58} |")

        # Total
        total_str = (
            f"Total: {innings.total_runs}/{innings.wickets} "
            f"in {innings.overs_display} overs (RR: {innings.run_rate:.2f})"
        )
        print(f"| {total_str:<58} |")
        print(Scoreboard.SEPARATOR)

    @staticmethod
    def display_bowling_card(innings: Innings) -> None:
        """Display the formatted bowling card.

        Args:
            innings: The innings to display bowling stats for.
        """
        print(Scoreboard.SEPARATOR)
        print(f"| {'BOWLING':<58} |")
        print(Scoreboard.SEPARATOR)
        print(f"| {'Bowler':<15} {'O':>5} {'M':>3} {'R':>4} {'W':>3} {'ECON':>7}          |")
        print(Scoreboard.SEPARATOR)

        for stats in innings.bowling_card:
            print(
                f"| {stats.player.name:<15} "
                f"{stats.overs_display:>5} {stats.maidens:>3} "
                f"{stats.runs_given:>4} {stats.wickets:>3} "
                f"{stats.economy:>7.2f}          |"
            )

        print(Scoreboard.SEPARATOR)

    @staticmethod
    def display_innings_summary(innings: Innings) -> None:
        """Display complete innings summary (batting + bowling cards).

        Args:
            innings: The innings to display.
        """
        title = f"{innings.batting_team.name} INNINGS - {innings.total_runs}/{innings.wickets} ({innings.overs_display} ov)"
        print(Scoreboard.HEADER_SEP)
        print(f"| {title:^58} |")
        print(Scoreboard.HEADER_SEP)
        Scoreboard.display_batting_card(innings)
        Scoreboard.display_bowling_card(innings)

    @staticmethod
    def display_match_summary(match: Match) -> None:
        """Display the final match summary.

        Args:
            match: The match to display result for.
        """
        print()
        print(Scoreboard.HEADER_SEP)
        print(f"| {'MATCH RESULT':^58} |")
        print(Scoreboard.HEADER_SEP)
        if match.innings1:
            print(f"|   {match.team1.name}: {match.innings1.total_runs}/{match.innings1.wickets} in {match.innings1.overs_display} overs{' ' * 30}|")
        if match.innings2:
            print(f"|   {match.team2.name}: {match.innings2.total_runs}/{match.innings2.wickets} in {match.innings2.overs_display} overs{' ' * 28}|")
        print(f"|   {match.get_result_text():<57}|")
        print(Scoreboard.HEADER_SEP)
