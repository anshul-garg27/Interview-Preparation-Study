"""Publisher class that publishes messages to topics via the broker."""

import uuid
from typing import TYPE_CHECKING

from enums import Priority
from message import Message

if TYPE_CHECKING:
    from message_broker import MessageBroker


class Publisher:
    """Represents a message publisher in the Pub-Sub system.

    Publishers create messages and send them to the broker for
    delivery to subscribers of the specified topic.

    Attributes:
        publisher_id: Unique identifier.
        name: Human-readable name.
    """

    def __init__(self, name: str) -> None:
        """Initialize a Publisher.

        Args:
            name: Name of the publisher.

        Raises:
            ValueError: If name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Publisher name cannot be empty.")
        self.publisher_id: str = str(uuid.uuid4())[:8]
        self.name = name

    def publish(
        self,
        broker: "MessageBroker",
        topic_name: str,
        content: str,
        priority: Priority = Priority.MEDIUM,
    ) -> Message:
        """Publish a message to a topic via the broker.

        Args:
            broker: The message broker to publish through.
            topic_name: Name of the topic to publish to.
            content: Message content.
            priority: Message priority (default MEDIUM).

        Returns:
            The published Message object.
        """
        message = Message(topic_name, content, priority)
        broker.publish(topic_name, message)
        return message

    def __str__(self) -> str:
        return f"Publisher({self.name})"

    def __repr__(self) -> str:
        return f"Publisher(id={self.publisher_id}, name={self.name})"
