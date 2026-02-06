"""
RateLimiter - Token bucket rate limiter per user per channel.
Different limits for each priority level.
"""

from datetime import datetime, timedelta
from collections import defaultdict

from notification import Notification
from enums import Priority


class RateLimiter:
    """
    Token-bucket style rate limiter.
    Limits notifications per (user, channel) within a time window,
    with different thresholds per priority level.
    """

    def __init__(self):
        # (user:channel) -> list of send timestamps
        self._records: dict[str, list[datetime]] = defaultdict(list)
        # Priority -> (max_count, window_seconds)
        self._limits: dict[Priority, tuple[int, int]] = {
            Priority.CRITICAL: (999999, 3600),  # effectively unlimited
            Priority.HIGH: (20, 3600),           # 20 per hour
            Priority.MEDIUM: (10, 3600),         # 10 per hour
            Priority.LOW: (5, 3600),             # 5 per hour
        }

    def is_allowed(self, notification: Notification) -> bool:
        """
        Check if the notification is within rate limits.

        Returns:
            True if allowed, False if rate-limited.
        """
        key = f"{notification.recipient}:{notification.channel}"
        max_count, window = self._limits.get(notification.priority, (10, 3600))

        now = datetime.now()
        cutoff = now - timedelta(seconds=window)

        # Clean old records
        self._records[key] = [t for t in self._records[key] if t > cutoff]

        return len(self._records[key]) < max_count

    def record(self, notification: Notification) -> None:
        """Record that a notification was sent (for rate tracking)."""
        key = f"{notification.recipient}:{notification.channel}"
        self._records[key].append(datetime.now())
