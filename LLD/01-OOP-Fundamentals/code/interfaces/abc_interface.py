"""ABC as Interface - Using Abstract Base Classes to define contracts."""

from abc import ABC, abstractmethod


class Notifier(ABC):
    """Interface: defines WHAT to do, not HOW."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> str:
        pass

    @abstractmethod
    def validate(self, recipient: str) -> bool:
        pass


class EmailNotifier(Notifier):
    def send(self, recipient: str, message: str) -> str:
        return f"Email to {recipient}: {message}"

    def validate(self, recipient: str) -> bool:
        return "@" in recipient


class SMSNotifier(Notifier):
    def send(self, recipient: str, message: str) -> str:
        return f"SMS to {recipient}: {message}"

    def validate(self, recipient: str) -> bool:
        return recipient.startswith("+") and len(recipient) >= 10


class SlackNotifier(Notifier):
    def send(self, recipient: str, message: str) -> str:
        return f"Slack to #{recipient}: {message}"

    def validate(self, recipient: str) -> bool:
        return len(recipient) > 0


# Incomplete implementation - fails at instantiation
class BrokenNotifier(Notifier):
    def send(self, recipient: str, message: str) -> str:
        return "sending..."
    # Missing validate() - will raise TypeError


def notify_all(notifiers: list[Notifier], message: str) -> None:
    """Works with ANY Notifier implementation."""
    for n in notifiers:
        recipient = "test@example.com" if isinstance(n, EmailNotifier) else "#general"
        if n.validate(recipient):
            print(f"  {n.send(recipient, message)}")


if __name__ == "__main__":
    print("=== ABC as Interface ===\n")

    notifiers: list[Notifier] = [
        EmailNotifier(),
        SMSNotifier(),
        SlackNotifier(),
    ]

    notify_all(notifiers, "Server is down!")

    # Cannot instantiate incomplete implementation
    print("\n--- Incomplete Implementation ---")
    try:
        broken = BrokenNotifier()  # type: ignore
    except TypeError as e:
        print(f"  Error: {e}")
        print("  ABC enforces: implement ALL abstract methods.")
