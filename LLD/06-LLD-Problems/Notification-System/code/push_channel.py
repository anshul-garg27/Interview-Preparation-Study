"""
PushChannel - Sends push notifications to mobile devices.
"""

from notification import Notification
from channel import NotificationChannel


class PushChannel(NotificationChannel):
    """Push notification channel for mobile devices."""

    def send(self, notification: Notification) -> bool:
        formatted = self.format_message(notification)
        print(f"    [PUSH] Sent to {notification.recipient}: {formatted}")
        return True

    def format_message(self, notification: Notification) -> str:
        return f"{notification.subject} - {notification.content[:100]}"
