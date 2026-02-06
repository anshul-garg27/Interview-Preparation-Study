"""DIP Violation - High-level module directly depends on low-level module."""


class GmailClient:
    """Low-level module: specific email implementation."""

    def send_gmail(self, to: str, subject: str, body: str) -> str:
        return f"Gmail sent to {to}: {subject}"


class NotificationService:
    """BAD: High-level module DIRECTLY creates and depends on GmailClient.
    Cannot switch to SendGrid, Mailgun, or use a mock for testing."""

    def __init__(self):
        self.gmail = GmailClient()  # Tightly coupled!

    def send_notification(self, user_email: str, message: str) -> str:
        return self.gmail.send_gmail(user_email, "Notification", message)


class OrderService:
    """BAD: Also tightly coupled to NotificationService and its Gmail dependency."""

    def __init__(self):
        self.notification = NotificationService()  # Can't mock this!

    def place_order(self, user_email: str, item: str) -> str:
        result = self.notification.send_notification(
            user_email, f"Order placed: {item}"
        )
        return f"Order placed for {item}. {result}"


if __name__ == "__main__":
    print("BAD DESIGN: Dependency Inversion Violation\n")

    service = OrderService()
    print(service.place_order("alice@mail.com", "Laptop"))

    print("\nPROBLEMS:")
    print("  1. NotificationService CREATES GmailClient internally")
    print("  2. Cannot switch email provider without modifying code")
    print("  3. Cannot mock GmailClient for testing")
    print("  4. OrderService is also tightly coupled to NotificationService")
    print("  5. Testing requires an actual Gmail connection")
