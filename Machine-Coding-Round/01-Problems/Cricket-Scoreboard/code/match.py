"""Match class representing a full cricket match."""

from typing import Optional

from enums import MatchResult, InningsStatus
from team import Team
from innings import Innings


class Match:
    """Represents a cricket match between two teams.

    Attributes:
        team1: First team (bats first).
        team2: Second team (chases).
        max_overs: Maximum overs per innings.
        innings1: First innings (team1 batting).
        innings2: Second innings (team2 batting).
        current_innings: Currently active innings.
        result: Match result.
    """

    def __init__(self, team1: Team, team2: Team, max_overs: int) -> None:
        """Initialize a Match.

        Args:
            team1: First team.
            team2: Second team.
            max_overs: Maximum overs per innings.
        """
        self.team1 = team1
        self.team2 = team2
        self.max_overs = max_overs
        self.innings1: Optional[Innings] = None
        self.innings2: Optional[Innings] = None
        self.current_innings: Optional[Innings] = None
        self.result: MatchResult = MatchResult.IN_PROGRESS

    def start_first_innings(self) -> Innings:
        """Start the first innings (team1 batting).

        Returns:
            The first Innings object.
        """
        self.innings1 = Innings(self.team1, self.team2, self.max_overs)
        self.innings1.start()
        self.current_innings = self.innings1
        return self.innings1

    def start_second_innings(self) -> Innings:
        """Start the second innings (team2 chasing team1's score).

        Returns:
            The second Innings object.

        Raises:
            ValueError: If first innings not completed.
        """
        if self.innings1 is None or self.innings1.status != InningsStatus.COMPLETED:
            raise ValueError("First innings must be completed before starting second.")

        target = self.innings1.total_runs + 1
        self.innings2 = Innings(
            self.team2, self.team1, self.max_overs, target=target
        )
        self.innings2.start()
        self.current_innings = self.innings2
        return self.innings2

    def end_current_innings(self) -> None:
        """End the current innings and determine if match is over."""
        if self.current_innings:
            self.current_innings.status = InningsStatus.COMPLETED

        if self.innings2 and self.innings2.status == InningsStatus.COMPLETED:
            self._determine_result()

    def _determine_result(self) -> None:
        """Determine the match result after both innings."""
        if self.innings1 is None or self.innings2 is None:
            return

        score1 = self.innings1.total_runs
        score2 = self.innings2.total_runs

        if score1 > score2:
            self.result = MatchResult.TEAM1_WIN
        elif score2 > score1:
            self.result = MatchResult.TEAM2_WIN
        else:
            self.result = MatchResult.TIE

    def get_result_text(self) -> str:
        """Get a human-readable match result."""
        if self.result == MatchResult.IN_PROGRESS:
            return "Match in progress"
        if self.innings1 is None or self.innings2 is None:
            return "Match in progress"

        score1 = self.innings1.total_runs
        score2 = self.innings2.total_runs

        if self.result == MatchResult.TEAM1_WIN:
            return f"{self.team1.name} wins by {score1 - score2} runs!"
        elif self.result == MatchResult.TEAM2_WIN:
            wickets_left = len(self.team2.players) - 1 - self.innings2.wickets
            return f"{self.team2.name} wins by {wickets_left} wickets!"
        else:
            return "Match tied!"

    def __str__(self) -> str:
        return f"Match: {self.team1.name} vs {self.team2.name} ({self.max_overs} overs)"
