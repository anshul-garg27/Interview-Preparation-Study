"""
Notification entity for the Notification System.
Represents a single notification with all its metadata.
"""

from datetime import datetime
from typing import Optional
import uuid

from enums import Priority, NotificationStatus


class Notification:
    """Represents a notification to be sent to a recipient."""

    def __init__(self, recipient: str, content: str, channel: str,
                 priority: Priority = Priority.MEDIUM,
                 subject: str = ""):
        """
        Args:
            recipient: User ID or address of the recipient.
            content: Body/message of the notification.
            channel: Channel name (email, sms, push, slack).
            priority: Priority level.
            subject: Optional subject line.
        """
        self.id: str = str(uuid.uuid4())[:8]
        self.recipient = recipient
        self.content = content
        self.channel = channel
        self.priority = priority
        self.subject = subject
        self.status: NotificationStatus = NotificationStatus.PENDING
        self.template_id: Optional[str] = None
        self.template_vars: dict[str, str] = {}
        self.attempts: int = 0
        self.max_retries: int = 3
        self.created_at: datetime = datetime.now()
        self.sent_at: Optional[datetime] = None
        self.error: Optional[str] = None

    def __str__(self) -> str:
        return (f"[{self.id}] To: {self.recipient} | "
                f"Channel: {self.channel} | Priority: {self.priority.name} | "
                f"Status: {self.status.value} | Attempts: {self.attempts}")
