"""
UserPreferences - Per-user notification preferences.
Supports channel opt-in/out and quiet hours.
"""

from datetime import datetime
from typing import Optional


class UserPreferences:
    """Manages notification preferences for a single user."""

    def __init__(self, user_id: str, enabled_channels: set[str] | None = None):
        """
        Args:
            user_id: The user's identifier.
            enabled_channels: Set of channel names the user has opted into.
                              Defaults to all channels enabled.
        """
        self.user_id = user_id
        self.enabled_channels: set[str] = enabled_channels or {
            "email", "sms", "push", "slack"
        }
        self.quiet_start: Optional[int] = None  # hour (e.g., 22)
        self.quiet_end: Optional[int] = None    # hour (e.g., 7)

    def is_channel_enabled(self, channel: str) -> bool:
        """Check if the user has opted into the given channel."""
        return channel in self.enabled_channels

    def set_quiet_hours(self, start: int, end: int) -> None:
        """
        Set quiet hours during which non-critical notifications are suppressed.

        Args:
            start: Start hour (0-23).
            end: End hour (0-23).
        """
        self.quiet_start = start
        self.quiet_end = end

    def is_quiet_hours(self) -> bool:
        """Check if the current time falls within quiet hours."""
        if self.quiet_start is None:
            return False
        hour = datetime.now().hour
        if self.quiet_start < self.quiet_end:
            return self.quiet_start <= hour < self.quiet_end
        else:  # wraps midnight (e.g., 22 to 7)
            return hour >= self.quiet_start or hour < self.quiet_end
