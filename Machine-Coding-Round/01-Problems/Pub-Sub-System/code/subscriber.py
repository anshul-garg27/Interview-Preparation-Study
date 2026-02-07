"""Abstract Subscriber interface for the Pub-Sub system."""

import uuid
from abc import ABC, abstractmethod
from typing import Optional

from message import Message
from message_filter import MessageFilter


class Subscriber(ABC):
    """Abstract base class for all subscribers.

    Subscribers receive messages from topics they are subscribed to.
    Each subscriber can optionally have a filter to control which
    messages they process.

    Attributes:
        subscriber_id: Unique identifier.
        name: Human-readable name.
        message_filter: Optional filter for incoming messages.
    """

    def __init__(
        self, name: str, message_filter: Optional[MessageFilter] = None
    ) -> None:
        """Initialize a Subscriber.

        Args:
            name: Name of the subscriber.
            message_filter: Optional message filter.

        Raises:
            ValueError: If name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Subscriber name cannot be empty.")
        self.subscriber_id: str = str(uuid.uuid4())[:8]
        self.name = name
        self.message_filter = message_filter

    def should_receive(self, message: Message) -> bool:
        """Check if this subscriber should receive a message.

        Args:
            message: The message to check.

        Returns:
            True if no filter or message passes filter.
        """
        if self.message_filter is None:
            return True
        return self.message_filter.matches(message)

    @abstractmethod
    def on_message(self, message: Message) -> bool:
        """Handle an incoming message.

        Args:
            message: The message to process.

        Returns:
            True if message was processed successfully.
        """
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Subscriber):
            return False
        return self.subscriber_id == other.subscriber_id

    def __hash__(self) -> int:
        return hash(self.subscriber_id)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.name})"
