"""Bowler statistics tracking for a cricket innings."""

from player import Player


class BowlerStats:
    """Tracks bowling statistics for a single bowler in an innings.

    Attributes:
        player: The bowler.
        overs_completed: Number of completed overs.
        balls_in_current_over: Balls bowled in the current incomplete over.
        maidens: Number of maiden overs.
        runs_given: Total runs conceded.
        wickets: Number of wickets taken.
    """

    def __init__(self, player: Player) -> None:
        """Initialize BowlerStats.

        Args:
            player: The bowler player.
        """
        self.player = player
        self.overs_completed: int = 0
        self.balls_in_current_over: int = 0
        self.maidens: int = 0
        self.runs_given: int = 0
        self.wickets: int = 0
        self._current_over_runs: int = 0

    @property
    def total_balls(self) -> int:
        """Total legal balls bowled."""
        return (self.overs_completed * 6) + self.balls_in_current_over

    @property
    def overs_display(self) -> str:
        """Display overs in standard format (e.g., '3.4')."""
        if self.balls_in_current_over == 0:
            return f"{self.overs_completed}.0"
        return f"{self.overs_completed}.{self.balls_in_current_over}"

    @property
    def economy(self) -> float:
        """Calculate economy rate: runs / overs."""
        total_overs = self.overs_completed + (self.balls_in_current_over / 6.0)
        if total_overs == 0:
            return 0.0
        return round(self.runs_given / total_overs, 2)

    def add_legal_ball(self, runs: int, is_wicket: bool = False) -> None:
        """Record a legal delivery.

        Args:
            runs: Runs conceded on this ball.
            is_wicket: Whether a wicket fell.
        """
        self.balls_in_current_over += 1
        self.runs_given += runs
        self._current_over_runs += runs

        if is_wicket:
            self.wickets += 1

        if self.balls_in_current_over == 6:
            self.overs_completed += 1
            self.balls_in_current_over = 0
            if self._current_over_runs == 0:
                self.maidens += 1
            self._current_over_runs = 0

    def add_extra_runs(self, runs: int) -> None:
        """Record extra runs (wides, no-balls) conceded.

        Args:
            runs: Extra runs to add.
        """
        self.runs_given += runs
        self._current_over_runs += runs

    def __str__(self) -> str:
        return (
            f"{self.player.name:<15} {self.overs_display:>4}  "
            f"{self.maidens:>2}  {self.runs_given:>3}  "
            f"{self.wickets:>2}  {self.economy:>6.2f}"
        )
