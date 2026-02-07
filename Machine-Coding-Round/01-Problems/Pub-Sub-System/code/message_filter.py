"""Message filtering by priority and keywords."""

from typing import List, Optional

from enums import Priority
from message import Message


class MessageFilter:
    """Filters messages based on priority level and/or keywords.

    A message passes the filter if it meets ALL specified criteria:
    - Priority >= min_priority (if min_priority is set)
    - Content contains at least one keyword (if keywords are set)

    Attributes:
        min_priority: Minimum priority level to accept.
        keywords: List of keywords to match in content.
    """

    def __init__(
        self,
        min_priority: Optional[Priority] = None,
        keywords: Optional[List[str]] = None,
    ) -> None:
        """Initialize a MessageFilter.

        Args:
            min_priority: Minimum priority to accept (None = accept all).
            keywords: Keywords to match in content (None = accept all).
        """
        self.min_priority = min_priority
        self.keywords = keywords or []

    def matches(self, message: Message) -> bool:
        """Check if a message passes this filter.

        Args:
            message: The message to check.

        Returns:
            True if message passes all filter criteria.
        """
        if self.min_priority and message.priority < self.min_priority:
            return False

        if self.keywords:
            content_lower = message.content.lower()
            if not any(kw.lower() in content_lower for kw in self.keywords):
                return False

        return True

    def __str__(self) -> str:
        parts = []
        if self.min_priority:
            parts.append(f"priority>={self.min_priority.name}")
        if self.keywords:
            parts.append(f"keywords={self.keywords}")
        return f"Filter({', '.join(parts) if parts else 'none'})"
