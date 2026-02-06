"""
Abstract NotificationChannel interface.
All notification channels must implement send() and format_message().
"""

from abc import ABC, abstractmethod

from notification import Notification


class NotificationChannel(ABC):
    """Abstract interface for notification delivery channels."""

    @abstractmethod
    def send(self, notification: Notification) -> bool:
        """
        Send a notification.

        Returns:
            True on success, False on failure.
        """
        pass

    @abstractmethod
    def format_message(self, notification: Notification) -> str:
        """Format the notification for this channel."""
        pass
