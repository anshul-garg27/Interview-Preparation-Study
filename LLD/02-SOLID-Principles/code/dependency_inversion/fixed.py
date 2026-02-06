"""DIP Fixed - Both high and low-level modules depend on abstractions."""

from abc import ABC, abstractmethod


# === ABSTRACTION (interface) ===

class EmailClient(ABC):
    """Abstract interface - the contract both sides agree on."""

    @abstractmethod
    def send(self, to: str, subject: str, body: str) -> str:
        pass


# === LOW-LEVEL MODULES (implementations) ===

class GmailClient(EmailClient):
    def send(self, to: str, subject: str, body: str) -> str:
        return f"[Gmail] Sent to {to}: {subject}"


class SendGridClient(EmailClient):
    def send(self, to: str, subject: str, body: str) -> str:
        return f"[SendGrid] Sent to {to}: {subject}"


class MockEmailClient(EmailClient):
    """For testing - no actual emails sent."""

    def __init__(self):
        self.sent: list[dict] = []

    def send(self, to: str, subject: str, body: str) -> str:
        self.sent.append({"to": to, "subject": subject})
        return f"[Mock] Recorded email to {to}"


# === HIGH-LEVEL MODULE (depends on abstraction, not concrete) ===

class NotificationService:
    """Depends on EmailClient INTERFACE, not Gmail/SendGrid directly."""

    def __init__(self, email_client: EmailClient):
        self._client = email_client  # Injected, not created

    def notify(self, user_email: str, message: str) -> str:
        return self._client.send(user_email, "Notification", message)


if __name__ == "__main__":
    print("GOOD DESIGN: Dependency Inversion Principle\n")

    # Production: use Gmail
    gmail_service = NotificationService(GmailClient())
    print(gmail_service.notify("alice@mail.com", "Order shipped"))

    # Switch to SendGrid - ZERO changes to NotificationService
    sg_service = NotificationService(SendGridClient())
    print(sg_service.notify("bob@mail.com", "Payment received"))

    # Testing: use mock
    mock = MockEmailClient()
    test_service = NotificationService(mock)
    test_service.notify("test@test.com", "Test message")
    print(f"\nMock recorded: {mock.sent}")

    print("\nBENEFITS:")
    print("  1. NotificationService depends on EmailClient interface")
    print("  2. Swap providers without changing NotificationService")
    print("  3. Easy to test with MockEmailClient")
    print("  4. New providers = new class, zero existing code changes")
