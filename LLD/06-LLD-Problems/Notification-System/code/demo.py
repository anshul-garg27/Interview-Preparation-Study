"""
Notification System - Demo
============================
Send via all channels, show rate limiting, retry with exponential backoff.
Design Patterns: Strategy (channels), Chain of Responsibility (pipeline),
                 Builder, Observer, Template Method
"""

import random

from enums import Priority
from notification import Notification
from template import NotificationTemplate
from email_channel import EmailChannel
from sms_channel import SMSChannel
from push_channel import PushChannel
from slack_channel import SlackChannel
from user_preferences import UserPreferences
from notification_service import NotificationService


def main():
    random.seed(42)

    print("=" * 65)
    print("       NOTIFICATION SYSTEM - LOW LEVEL DESIGN DEMO")
    print("=" * 65)

    # Setup service
    service = NotificationService()

    # Register channels
    service.register_channel("email", EmailChannel(fail_rate=0.3))
    service.register_channel("sms", SMSChannel())
    service.register_channel("push", PushChannel())
    service.register_channel("slack", SlackChannel())

    # Register templates
    service.register_template(NotificationTemplate(
        "order_shipped",
        "Order {{order_id}} Shipped!",
        "Hi {{user_name}}, your order #{{order_id}} has been shipped. "
        "Track at: {{tracking_url}}"
    ))
    service.register_template(NotificationTemplate(
        "welcome",
        "Welcome to Our Platform, {{user_name}}!",
        "Hi {{user_name}}, thanks for joining! Get started at {{start_url}}"
    ))

    # User preferences
    alice_prefs = UserPreferences("alice", {"email", "push"})  # No SMS, no Slack
    bob_prefs = UserPreferences("bob", {"email", "sms", "push", "slack"})
    service.set_user_preferences(alice_prefs)
    service.set_user_preferences(bob_prefs)

    # ---- Scenario 1: Send via all channels to bob ----
    print("\n" + "=" * 65)
    print("SCENARIO 1: Send notification via different channels")
    print("=" * 65)

    for channel in ["email", "sms", "push", "slack"]:
        n = Notification(
            recipient="bob",
            content="Platform maintenance scheduled for tonight.",
            channel=channel,
            priority=Priority.MEDIUM,
            subject="System Update"
        )
        service.send(n)

    # ---- Scenario 2: Template-based notification ----
    print("\n" + "=" * 65)
    print("SCENARIO 2: Template-based notification")
    print("=" * 65)

    n = Notification(recipient="alice", content="", channel="email",
                     priority=Priority.HIGH)
    n.template_id = "order_shipped"
    n.template_vars = {
        "user_name": "Alice",
        "order_id": "ORD-9876",
        "tracking_url": "https://track.example.com/9876"
    }
    service.send(n)

    # ---- Scenario 3: User preference opt-out ----
    print("\n" + "=" * 65)
    print("SCENARIO 3: User opted out of SMS (Alice)")
    print("=" * 65)

    n = Notification(recipient="alice", content="50% off today only!",
                     channel="sms", priority=Priority.LOW, subject="Promo")
    service.send(n)

    # ---- Scenario 4: Critical bypasses preferences ----
    print("\n" + "=" * 65)
    print("SCENARIO 4: CRITICAL notification bypasses opt-out")
    print("=" * 65)

    n = Notification(recipient="alice",
                     content="Suspicious login detected on your account!",
                     channel="sms", priority=Priority.CRITICAL,
                     subject="SECURITY ALERT")
    service.send(n)

    # ---- Scenario 5: Rate limiting ----
    print("\n" + "=" * 65)
    print("SCENARIO 5: Rate limiting (LOW priority: 5/hour)")
    print("=" * 65)

    for i in range(7):
        n = Notification(
            recipient="bob",
            content=f"Low priority update number {i + 1}",
            channel="push",
            priority=Priority.LOW,
            subject=f"Update #{i + 1}"
        )
        service.send(n)

    # ---- Scenario 6: Retry on failure ----
    print("\n" + "=" * 65)
    print("SCENARIO 6: Retry with exponential backoff (email may fail)")
    print("=" * 65)

    n = Notification(recipient="bob", content="Your monthly report is ready.",
                     channel="email", priority=Priority.HIGH,
                     subject="Important Report")
    n.max_retries = 3
    service.send(n)

    # ---- Scenario 7: Batch notifications ----
    print("\n" + "=" * 65)
    print("SCENARIO 7: Batch notifications")
    print("=" * 65)

    batch = []
    for user in ["alice", "bob"]:
        n = Notification(recipient=user, content="", channel="push",
                         priority=Priority.MEDIUM)
        n.template_id = "welcome"
        n.template_vars = {
            "user_name": user.capitalize(),
            "start_url": "https://platform.example.com/start"
        }
        batch.append(n)
    service.send_batch(batch)

    # ---- Audit Log ----
    print("\n" + "=" * 65)
    print("AUDIT LOG")
    print("=" * 65)
    for entry in service.get_logs():
        print(f"  {entry}")


if __name__ == "__main__":
    main()
