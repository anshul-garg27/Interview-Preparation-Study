"""Per-topic message queue for ordered delivery."""

import threading
from collections import deque
from typing import Optional, List

from message import Message


class MessageQueue:
    """Thread-safe ordered message queue for a single topic.

    Ensures messages are delivered in the order they were published.
    Tracks total messages processed for stats.

    Attributes:
        topic_name: Name of the associated topic.
    """

    def __init__(self, topic_name: str) -> None:
        """Initialize a MessageQueue.

        Args:
            topic_name: Name of the topic this queue serves.
        """
        self.topic_name = topic_name
        self._queue: deque = deque()
        self._lock = threading.Lock()
        self._processed_count: int = 0

    def enqueue(self, message: Message) -> None:
        """Add a message to the end of the queue.

        Args:
            message: The message to enqueue.
        """
        with self._lock:
            self._queue.append(message)

    def dequeue(self) -> Optional[Message]:
        """Remove and return the next message from the queue.

        Returns:
            The next Message, or None if queue is empty.
        """
        with self._lock:
            if self._queue:
                self._processed_count += 1
                return self._queue.popleft()
            return None

    def peek(self) -> Optional[Message]:
        """Look at the next message without removing it.

        Returns:
            The next Message, or None if queue is empty.
        """
        with self._lock:
            return self._queue[0] if self._queue else None

    def is_empty(self) -> bool:
        """Check if the queue is empty."""
        with self._lock:
            return len(self._queue) == 0

    def size(self) -> int:
        """Return the number of messages currently in the queue."""
        with self._lock:
            return len(self._queue)

    @property
    def processed_count(self) -> int:
        """Return total number of messages processed."""
        return self._processed_count

    def get_all_pending(self) -> List[Message]:
        """Get all pending messages without removing them."""
        with self._lock:
            return list(self._queue)

    def __str__(self) -> str:
        return f"MessageQueue('{self.topic_name}', pending={self.size()}, processed={self._processed_count})"
