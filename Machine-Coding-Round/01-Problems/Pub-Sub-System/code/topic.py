"""Topic class representing a named channel for messages."""

from typing import List, TYPE_CHECKING
import threading

if TYPE_CHECKING:
    from subscriber import Subscriber


class Topic:
    """Represents a named topic that subscribers can subscribe to.

    Messages published to this topic are delivered to all subscribers.

    Attributes:
        name: Unique name of the topic.
        subscribers: List of subscribers to this topic.
    """

    def __init__(self, name: str) -> None:
        """Initialize a Topic.

        Args:
            name: Name of the topic.

        Raises:
            ValueError: If name is empty.
        """
        if not name or not name.strip():
            raise ValueError("Topic name cannot be empty.")
        self.name = name
        self._subscribers: List["Subscriber"] = []
        self._lock = threading.Lock()

    @property
    def subscribers(self) -> List["Subscriber"]:
        """Return a copy of the subscribers list."""
        with self._lock:
            return list(self._subscribers)

    def subscribe(self, subscriber: "Subscriber") -> bool:
        """Add a subscriber to this topic.

        Args:
            subscriber: The subscriber to add.

        Returns:
            True if subscriber was added, False if already subscribed.
        """
        with self._lock:
            if subscriber in self._subscribers:
                return False
            self._subscribers.append(subscriber)
            return True

    def unsubscribe(self, subscriber: "Subscriber") -> bool:
        """Remove a subscriber from this topic.

        Args:
            subscriber: The subscriber to remove.

        Returns:
            True if subscriber was removed, False if not found.
        """
        with self._lock:
            if subscriber not in self._subscribers:
                return False
            self._subscribers.remove(subscriber)
            return True

    def get_subscriber_count(self) -> int:
        """Return the number of subscribers."""
        with self._lock:
            return len(self._subscribers)

    def __str__(self) -> str:
        return f"Topic('{self.name}', subscribers={self.get_subscriber_count()})"

    def __repr__(self) -> str:
        return f"Topic(name='{self.name}')"
