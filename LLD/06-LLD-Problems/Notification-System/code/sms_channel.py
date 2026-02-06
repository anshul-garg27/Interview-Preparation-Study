"""
SMSChannel - Sends notifications via SMS.
Truncates messages to 160 characters.
"""

import random

from notification import Notification
from channel import NotificationChannel


class SMSChannel(NotificationChannel):
    """SMS notification channel with 160-character limit."""

    def __init__(self, fail_rate: float = 0.0):
        """
        Args:
            fail_rate: Probability of send failure (0.0 to 1.0) for demo purposes.
        """
        self._fail_rate = fail_rate

    def send(self, notification: Notification) -> bool:
        formatted = self.format_message(notification)
        if random.random() < self._fail_rate:
            print(f"    [SMS] FAILED to send to {notification.recipient}")
            return False
        print(f"    [SMS] Sent to {notification.recipient}: {formatted}")
        return True

    def format_message(self, notification: Notification) -> str:
        msg = f"{notification.subject}: {notification.content}"
        return msg[:160]
