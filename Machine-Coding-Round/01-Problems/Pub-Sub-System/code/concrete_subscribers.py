"""Concrete subscriber implementations: Console, File, Email."""

from typing import Optional, List

from message import Message
from message_filter import MessageFilter
from subscriber import Subscriber


class ConsoleSubscriber(Subscriber):
    """Subscriber that prints messages to the console.

    Useful for debugging and real-time monitoring of topics.
    """

    def __init__(
        self, name: str, message_filter: Optional[MessageFilter] = None
    ) -> None:
        super().__init__(name, message_filter)
        self.received_messages: List[Message] = []

    def on_message(self, message: Message) -> bool:
        """Print the message to console.

        Args:
            message: The message to display.

        Returns:
            True always (console output rarely fails).
        """
        print(
            f"    [{self.name}] Received on '{message.topic_name}': "
            f"\"{message.content}\" ({message.priority.name})"
        )
        self.received_messages.append(message)
        return True


class FileSubscriber(Subscriber):
    """Subscriber that writes messages to a file.

    In production this would write to an actual file. For this demo,
    it simulates file writing and tracks messages in memory.
    """

    def __init__(
        self,
        name: str,
        file_path: str,
        message_filter: Optional[MessageFilter] = None,
    ) -> None:
        """Initialize a FileSubscriber.

        Args:
            name: Subscriber name.
            file_path: Path to the output file.
            message_filter: Optional message filter.
        """
        super().__init__(name, message_filter)
        self.file_path = file_path
        self.written_messages: List[str] = []

    def on_message(self, message: Message) -> bool:
        """Write the message to file (simulated).

        Args:
            message: The message to write.

        Returns:
            True if write was successful.
        """
        log_line = (
            f"[{message.timestamp.strftime('%H:%M:%S')}] "
            f"[{message.priority.name}] {message.topic_name}: {message.content}"
        )
        self.written_messages.append(log_line)
        print(
            f"    [{self.name}] Written to file '{self.file_path}': "
            f"\"{message.content}\""
        )
        return True


class EmailSubscriber(Subscriber):
    """Subscriber that sends messages as emails (simulated).

    In production this would send actual emails via SMTP.
    For this demo, it prints the email action and tracks messages.
    """

    def __init__(
        self,
        name: str,
        email_address: str,
        message_filter: Optional[MessageFilter] = None,
    ) -> None:
        """Initialize an EmailSubscriber.

        Args:
            name: Subscriber name.
            email_address: Target email address.
            message_filter: Optional message filter.
        """
        super().__init__(name, message_filter)
        self.email_address = email_address
        self.sent_emails: List[Message] = []

    def on_message(self, message: Message) -> bool:
        """Send the message as an email (simulated).

        Args:
            message: The message to send.

        Returns:
            True if email was sent successfully.
        """
        print(
            f"    [{self.name}] Email sent to {self.email_address}: "
            f"\"{message.content}\" ({message.priority.name})"
        )
        self.sent_emails.append(message)
        return True
