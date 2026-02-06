"""
RetryHandler - Retry logic with exponential backoff.
Retries failed notification sends up to a configurable maximum.
"""

import time
from datetime import datetime

from notification import Notification
from enums import NotificationStatus
from channel import NotificationChannel


class RetryHandler:
    """Handles retries with exponential backoff for failed sends."""

    def __init__(self, base_delay: float = 0.1):
        """
        Args:
            base_delay: Base delay in seconds (multiplied by 2^attempt).
                        Default 0.1s for demo; use 1.0+ in production.
        """
        self.base_delay = base_delay

    def send_with_retry(self, notification: Notification,
                        channel: NotificationChannel) -> bool:
        """
        Attempt to send a notification, retrying on failure with
        exponential backoff.

        Args:
            notification: The notification to send.
            channel: The channel to send through.

        Returns:
            True if eventually sent, False if all retries exhausted.
        """
        notification.attempts += 1
        success = channel.send(notification)

        if success:
            notification.status = NotificationStatus.SENT
            notification.sent_at = datetime.now()
            return True

        # Retry with exponential backoff
        while notification.attempts < notification.max_retries:
            delay = self.base_delay * (2 ** (notification.attempts - 1))
            print(f"    [RETRY] Attempt {notification.attempts + 1}/{notification.max_retries} "
                  f"after {delay:.1f}s backoff")
            time.sleep(delay)
            notification.attempts += 1
            success = channel.send(notification)
            if success:
                notification.status = NotificationStatus.SENT
                notification.sent_at = datetime.now()
                return True

        notification.status = NotificationStatus.FAILED
        notification.error = f"Failed after {notification.attempts} attempts"
        print(f"    [RETRY] EXHAUSTED: All {notification.max_retries} retries failed")
        return False
