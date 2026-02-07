"""Message class representing a single message in the Pub-Sub system."""

import uuid
from datetime import datetime

from enums import Priority, MessageStatus


class Message:
    """Represents a message published to a topic.

    Attributes:
        message_id: Unique identifier for the message.
        topic_name: Name of the topic this message belongs to.
        content: The message payload/content.
        priority: Priority level of the message.
        timestamp: When the message was created.
        status: Current delivery status.
    """

    def __init__(
        self, topic_name: str, content: str, priority: Priority = Priority.MEDIUM
    ) -> None:
        """Initialize a Message.

        Args:
            topic_name: Name of the topic.
            content: Message content.
            priority: Message priority (default MEDIUM).

        Raises:
            ValueError: If content is empty.
        """
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty.")
        self.message_id: str = str(uuid.uuid4())[:8]
        self.topic_name = topic_name
        self.content = content
        self.priority = priority
        self.timestamp: datetime = datetime.now()
        self.status: MessageStatus = MessageStatus.PENDING

    def mark_delivered(self) -> None:
        """Mark this message as delivered."""
        self.status = MessageStatus.DELIVERED

    def mark_acknowledged(self) -> None:
        """Mark this message as acknowledged."""
        self.status = MessageStatus.ACKNOWLEDGED

    def mark_failed(self) -> None:
        """Mark this message as failed."""
        self.status = MessageStatus.FAILED

    def __str__(self) -> str:
        return (
            f"Message({self.message_id}) [{self.priority.name}] "
            f"on '{self.topic_name}': {self.content}"
        )

    def __repr__(self) -> str:
        return f"Message(id={self.message_id}, topic={self.topic_name})"
