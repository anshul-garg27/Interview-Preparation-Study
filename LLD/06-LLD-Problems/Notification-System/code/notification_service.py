"""
NotificationService - Orchestrates the notification pipeline.
Pipeline: validate -> rate-limit -> preferences -> format -> send/retry -> log.
"""

from datetime import datetime

from notification import Notification
from channel import NotificationChannel
from template import NotificationTemplate
from rate_limiter import RateLimiter
from retry_handler import RetryHandler
from user_preferences import UserPreferences
from enums import Priority, NotificationStatus


class NotificationService:
    """
    Central service that processes notifications through a pipeline:
    validation -> rate limiting -> user preferences -> template formatting -> send with retry -> logging.
    """

    def __init__(self):
        self.channels: dict[str, NotificationChannel] = {}
        self.templates: dict[str, NotificationTemplate] = {}
        self.user_prefs: dict[str, UserPreferences] = {}
        self.rate_limiter = RateLimiter()
        self.retry_handler = RetryHandler(base_delay=0.1)
        self.logs: list[str] = []

    def register_channel(self, name: str, channel: NotificationChannel) -> None:
        """Register a notification channel by name."""
        self.channels[name] = channel

    def register_template(self, template: NotificationTemplate) -> None:
        """Register a notification template."""
        self.templates[template.template_id] = template

    def set_user_preferences(self, prefs: UserPreferences) -> None:
        """Set preferences for a user."""
        self.user_prefs[prefs.user_id] = prefs

    def send(self, notification: Notification) -> bool:
        """
        Process a single notification through the full pipeline.

        Returns:
            True if sent successfully, False otherwise.
        """
        print(f"\n  Processing: {notification}")

        # Step 1: Validate
        if not self._validate(notification):
            self._log(notification)
            return False

        # Step 2: Rate limit
        if not self._check_rate_limit(notification):
            self._log(notification)
            return False

        # Step 3: User preferences
        if not self._check_preferences(notification):
            self._log(notification)
            return False

        # Step 4: Format (apply template if specified)
        self._format(notification)

        # Step 5: Send with retry
        channel = self.channels[notification.channel]
        success = self.retry_handler.send_with_retry(notification, channel)

        # Step 6: Log
        self._log(notification)
        return success

    def send_batch(self, notifications: list[Notification]) -> dict[str, int]:
        """
        Send a batch of notifications.

        Returns:
            Dict with counts: {sent, failed, skipped, rate_limited}.
        """
        print(f"\n  --- Batch: {len(notifications)} notifications ---")
        results = {"sent": 0, "failed": 0, "skipped": 0, "rate_limited": 0}
        for n in notifications:
            self.send(n)
            if n.status == NotificationStatus.SENT:
                results["sent"] += 1
            elif n.status == NotificationStatus.FAILED:
                results["failed"] += 1
            elif n.status == NotificationStatus.SKIPPED:
                results["skipped"] += 1
            elif n.status == NotificationStatus.RATE_LIMITED:
                results["rate_limited"] += 1
        print(f"\n  Batch results: {results}")
        return results

    def _validate(self, notification: Notification) -> bool:
        """Validate required fields and channel existence."""
        if not notification.recipient:
            notification.status = NotificationStatus.FAILED
            notification.error = "Missing recipient"
            print(f"    [VALIDATE] FAILED: Missing recipient")
            return False
        if not notification.channel:
            notification.status = NotificationStatus.FAILED
            notification.error = "Missing channel"
            print(f"    [VALIDATE] FAILED: Missing channel")
            return False
        if notification.channel not in self.channels:
            notification.status = NotificationStatus.FAILED
            notification.error = f"Unknown channel: {notification.channel}"
            print(f"    [VALIDATE] FAILED: Unknown channel '{notification.channel}'")
            return False
        print(f"    [VALIDATE] OK - {notification.recipient} via {notification.channel}")
        return True

    def _check_rate_limit(self, notification: Notification) -> bool:
        """Check and enforce rate limits."""
        if not self.rate_limiter.is_allowed(notification):
            notification.status = NotificationStatus.RATE_LIMITED
            notification.error = "Rate limit exceeded"
            print(f"    [RATE-LIMIT] BLOCKED: {notification.recipient} exceeded limit "
                  f"for {notification.channel}")
            return False
        self.rate_limiter.record(notification)
        print(f"    [RATE-LIMIT] OK - within limits")
        return True

    def _check_preferences(self, notification: Notification) -> bool:
        """Check user preferences (opt-in/out). Critical bypasses preferences."""
        prefs = self.user_prefs.get(notification.recipient)
        if prefs and notification.priority != Priority.CRITICAL:
            if not prefs.is_channel_enabled(notification.channel):
                notification.status = NotificationStatus.SKIPPED
                notification.error = f"User opted out of {notification.channel}"
                print(f"    [PREF] SKIPPED: {notification.recipient} opted out of "
                      f"{notification.channel}")
                return False
        print(f"    [PREF] OK - channel enabled for user")
        return True

    def _format(self, notification: Notification) -> None:
        """Apply template formatting if a template is specified."""
        if notification.template_id and notification.template_id in self.templates:
            template = self.templates[notification.template_id]
            subject, body = template.render(notification.template_vars)
            notification.subject = subject
            notification.content = body
            print(f"    [FORMAT] Applied template '{notification.template_id}'")
        else:
            print(f"    [FORMAT] Using direct subject/body")

    def _log(self, notification: Notification) -> None:
        """Log the notification result."""
        entry = (f"[{datetime.now().strftime('%H:%M:%S')}] "
                 f"{notification.id} | {notification.recipient} | "
                 f"{notification.channel} | {notification.priority.name} | "
                 f"{notification.status.value}")
        self.logs.append(entry)
        print(f"    [LOG] {entry}")

    def get_logs(self) -> list[str]:
        """Return all logged entries."""
        return self.logs
