"""Batsman statistics tracking for a cricket innings."""

from typing import Optional

from player import Player
from enums import WicketType


class BatsmanStats:
    """Tracks batting statistics for a single batsman in an innings.

    Attributes:
        player: The batsman.
        runs: Total runs scored.
        balls_faced: Number of balls faced.
        fours: Number of boundaries (4 runs).
        sixes: Number of sixes (6 runs).
        is_out: Whether the batsman has been dismissed.
        dismissal_info: Description of how they got out.
    """

    def __init__(self, player: Player) -> None:
        """Initialize BatsmanStats.

        Args:
            player: The batsman player.
        """
        self.player = player
        self.runs: int = 0
        self.balls_faced: int = 0
        self.fours: int = 0
        self.sixes: int = 0
        self.is_out: bool = False
        self.dismissal_info: str = "not out"

    @property
    def strike_rate(self) -> float:
        """Calculate strike rate: (runs / balls) * 100."""
        if self.balls_faced == 0:
            return 0.0
        return round((self.runs / self.balls_faced) * 100, 2)

    def add_runs(self, runs: int) -> None:
        """Add runs scored by this batsman.

        Args:
            runs: Number of runs scored.
        """
        self.runs += runs
        if runs == 4:
            self.fours += 1
        elif runs == 6:
            self.sixes += 1

    def face_ball(self) -> None:
        """Record that the batsman faced a legal delivery."""
        self.balls_faced += 1

    def dismiss(
        self,
        wicket_type: WicketType,
        bowler_name: str,
        fielder_name: Optional[str] = None,
    ) -> None:
        """Record the batsman's dismissal.

        Args:
            wicket_type: Type of dismissal.
            bowler_name: Name of the bowler.
            fielder_name: Name of the fielder (for catches/stumpings).
        """
        self.is_out = True
        if wicket_type == WicketType.CAUGHT and fielder_name:
            self.dismissal_info = f"c {fielder_name} b {bowler_name}"
        elif wicket_type == WicketType.BOWLED:
            self.dismissal_info = f"b {bowler_name}"
        elif wicket_type == WicketType.LBW:
            self.dismissal_info = f"lbw b {bowler_name}"
        elif wicket_type == WicketType.STUMPED and fielder_name:
            self.dismissal_info = f"st {fielder_name} b {bowler_name}"
        elif wicket_type == WicketType.RUN_OUT and fielder_name:
            self.dismissal_info = f"run out ({fielder_name})"
        else:
            self.dismissal_info = f"{wicket_type.value} b {bowler_name}"

    def __str__(self) -> str:
        status = self.dismissal_info
        return (
            f"{self.player.name:<15} {status:<25} "
            f"{self.runs:>3}  {self.balls_faced:>3}  "
            f"{self.fours:>2}  {self.sixes:>2}  {self.strike_rate:>7.2f}"
        )
