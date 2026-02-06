"""
EmailChannel - Sends notifications via email.
"""

import random

from notification import Notification
from channel import NotificationChannel


class EmailChannel(NotificationChannel):
    """Email notification channel with configurable failure rate for testing."""

    def __init__(self, fail_rate: float = 0.0):
        """
        Args:
            fail_rate: Probability of send failure (0.0 to 1.0) for demo purposes.
        """
        self._fail_rate = fail_rate

    def send(self, notification: Notification) -> bool:
        formatted = self.format_message(notification)
        if random.random() < self._fail_rate:
            print(f"    [EMAIL] FAILED to send to {notification.recipient}")
            return False
        print(f"    [EMAIL] Sent to {notification.recipient}: {formatted}")
        return True

    def format_message(self, notification: Notification) -> str:
        return f"Subject: {notification.subject} | Body: {notification.content}"
