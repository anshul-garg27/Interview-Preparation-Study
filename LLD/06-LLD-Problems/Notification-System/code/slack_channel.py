"""
SlackChannel - Sends notifications via Slack.
Adds priority indicators to messages.
"""

from notification import Notification
from channel import NotificationChannel
from enums import Priority


class SlackChannel(NotificationChannel):
    """Slack notification channel with priority indicators."""

    def send(self, notification: Notification) -> bool:
        formatted = self.format_message(notification)
        print(f"    [SLACK] Sent to #{notification.recipient}: {formatted}")
        return True

    def format_message(self, notification: Notification) -> str:
        priority_indicator = {
            Priority.CRITICAL: "!!!",
            Priority.HIGH: "!!",
            Priority.MEDIUM: "!",
            Priority.LOW: ""
        }
        prefix = priority_indicator.get(notification.priority, "")
        return f"{prefix} {notification.subject}: {notification.content}"
