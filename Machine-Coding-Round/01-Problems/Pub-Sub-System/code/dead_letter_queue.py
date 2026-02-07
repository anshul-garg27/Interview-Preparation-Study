"""Dead Letter Queue for storing and retrying failed message deliveries."""

import threading
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass, field

from message import Message
from subscriber import Subscriber


@dataclass
class DLQEntry:
    """An entry in the Dead Letter Queue.

    Attributes:
        message: The failed message.
        subscriber: The subscriber that failed to process it.
        reason: The failure reason.
        timestamp: When the failure occurred.
        retry_count: Number of retry attempts made.
    """
    message: Message
    subscriber: Subscriber
    reason: str
    timestamp: datetime = field(default_factory=datetime.now)
    retry_count: int = 0


class DeadLetterQueue:
    """Stores failed message deliveries for later retry.

    When a subscriber fails to process a message, it is moved here
    along with the failure reason. Messages can be retried later.

    Attributes:
        max_retries: Maximum number of retry attempts per message.
    """

    def __init__(self, max_retries: int = 3) -> None:
        """Initialize the Dead Letter Queue.

        Args:
            max_retries: Maximum retry attempts (default 3).
        """
        self.max_retries = max_retries
        self._entries: List[DLQEntry] = []
        self._lock = threading.Lock()

    def add(self, message: Message, subscriber: Subscriber, reason: str) -> None:
        """Add a failed message delivery to the DLQ.

        Args:
            message: The message that failed.
            subscriber: The subscriber that failed.
            reason: Description of the failure.
        """
        with self._lock:
            entry = DLQEntry(message=message, subscriber=subscriber, reason=reason)
            self._entries.append(entry)

    def retry_all(self) -> List[DLQEntry]:
        """Retry all messages in the DLQ.

        Returns:
            List of entries that still failed after retry.
        """
        still_failed: List[DLQEntry] = []

        with self._lock:
            entries_to_retry = list(self._entries)
            self._entries.clear()

        for entry in entries_to_retry:
            if entry.retry_count >= self.max_retries:
                still_failed.append(entry)
                continue

            entry.retry_count += 1
            try:
                success = entry.subscriber.on_message(entry.message)
                if not success:
                    still_failed.append(entry)
            except Exception:
                still_failed.append(entry)

        with self._lock:
            self._entries.extend(still_failed)

        return still_failed

    def get_entries(self) -> List[DLQEntry]:
        """Get all entries in the DLQ."""
        with self._lock:
            return list(self._entries)

    def size(self) -> int:
        """Return the number of entries in the DLQ."""
        with self._lock:
            return len(self._entries)

    def clear(self) -> None:
        """Clear all entries from the DLQ."""
        with self._lock:
            self._entries.clear()

    def __str__(self) -> str:
        return f"DeadLetterQueue(entries={self.size()})"
