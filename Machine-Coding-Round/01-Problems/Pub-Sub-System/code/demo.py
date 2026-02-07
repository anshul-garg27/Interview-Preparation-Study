"""Full simulation demonstrating the Pub-Sub messaging system.

Run: cd code/ && python demo.py
"""

from enums import Priority
from message import Message
from message_filter import MessageFilter
from publisher import Publisher
from concrete_subscribers import ConsoleSubscriber, FileSubscriber, EmailSubscriber
from message_broker import MessageBroker


def print_separator(title: str = "") -> None:
    """Print a formatted section separator."""
    print()
    if title:
        print(f"{'=' * 60}")
        print(f"  {title}")
        print(f"{'=' * 60}")
    else:
        print("-" * 60)


def main() -> None:
    """Run the Pub-Sub system simulation."""
    broker = MessageBroker()

    print_separator("PUB-SUB MESSAGING SYSTEM SIMULATION")

    # ---- Create Topics ----
    print("\n--- Creating Topics ---")
    for topic_name in ["sports", "technology", "finance"]:
        topic = broker.create_topic(topic_name)
        print(f"  [+] Topic created: \"{topic.name}\"")

    # ---- Create Subscribers ----
    print("\n--- Registering Subscribers ---")

    alice = ConsoleSubscriber("Alice")
    print(f"  [+] ConsoleSubscriber \"{alice.name}\" created")

    bob = ConsoleSubscriber("Bob")
    print(f"  [+] ConsoleSubscriber \"{bob.name}\" created")

    file_logger = FileSubscriber("FileLogger", "/tmp/pubsub.log")
    print(f"  [+] FileSubscriber \"{file_logger.name}\" created -> {file_logger.file_path}")

    # Email subscriber with HIGH priority filter
    high_filter = MessageFilter(min_priority=Priority.HIGH)
    email_alert = EmailSubscriber("EmailAlert", "admin@example.com", high_filter)
    print(f"  [+] EmailSubscriber \"{email_alert.name}\" created -> {email_alert.email_address}")

    # ---- Subscribe to Topics ----
    print("\n--- Subscribing to Topics ---")

    broker.subscribe("sports", alice)
    print(f"  [+] Alice subscribed to \"sports\"")

    broker.subscribe("technology", alice)
    print(f"  [+] Alice subscribed to \"technology\"")

    broker.subscribe("sports", bob)
    print(f"  [+] Bob subscribed to \"sports\"")

    broker.subscribe("technology", file_logger)
    print(f"  [+] FileLogger subscribed to \"technology\"")

    broker.subscribe("finance", email_alert)
    print(f"  [+] EmailAlert subscribed to \"finance\" (filter: HIGH priority only)")

    # Create publishers
    pub_sports = Publisher("SportsDesk")
    pub_tech = Publisher("TechBlog")
    pub_finance = Publisher("FinanceWire")

    # ---- Publish Messages ----
    print("\n--- Publishing Messages ---")

    print(f"\n  [>] Publishing to \"sports\": \"India wins the World Cup!\" (HIGH)")
    pub_sports.publish(broker, "sports", "India wins the World Cup!", Priority.HIGH)

    print(f"\n  [>] Publishing to \"technology\": \"New Python 4.0 released\" (MEDIUM)")
    pub_tech.publish(broker, "technology", "New Python 4.0 released", Priority.MEDIUM)

    print(f"\n  [>] Publishing to \"finance\": \"Market hits all-time high\" (HIGH)")
    pub_finance.publish(broker, "finance", "Market hits all-time high", Priority.HIGH)

    print(f"\n  [>] Publishing to \"finance\": \"Quarterly results announced\" (LOW)")
    print("    (EmailAlert has HIGH priority filter - this should be filtered)")
    pub_finance.publish(broker, "finance", "Quarterly results announced", Priority.LOW)

    # ---- Unsubscribe Demo ----
    print_separator()
    print("--- Unsubscribe Demo ---")
    broker.unsubscribe("sports", alice)
    print(f"  [-] Alice unsubscribed from \"sports\"")

    print(f"\n  [>] Publishing to \"sports\": \"New IPL season announced\" (MEDIUM)")
    pub_sports.publish(broker, "sports", "New IPL season announced", Priority.MEDIUM)
    print(f"\n  (Alice did NOT receive the above message)")

    # ---- Keyword Filter Demo ----
    print_separator()
    print("--- Keyword Filter Demo ---")

    keyword_filter = MessageFilter(keywords=["Python", "AI"])
    charlie = ConsoleSubscriber("Charlie", keyword_filter)
    broker.subscribe("technology", charlie)
    print(f"  [+] Charlie subscribed to \"technology\" (filter: keywords=['Python', 'AI'])")

    print(f"\n  [>] Publishing: \"AI revolution in healthcare\" (HIGH)")
    pub_tech.publish(broker, "technology", "AI revolution in healthcare", Priority.HIGH)

    print(f"\n  [>] Publishing: \"New JavaScript framework released\" (LOW)")
    pub_tech.publish(broker, "technology", "New JavaScript framework released", Priority.LOW)
    print(f"  (Charlie should NOT receive 'JavaScript' message - no matching keyword)")

    # ---- Dead Letter Queue Stats ----
    print_separator()
    print("--- Dead Letter Queue ---")
    dlq = broker.dead_letter_queue
    print(f"  [!] {dlq.size()} messages in Dead Letter Queue")

    if dlq.size() > 0:
        for entry in dlq.get_entries():
            print(f"    - Msg: \"{entry.message.content}\" | Sub: {entry.subscriber.name} | Reason: {entry.reason}")

    # ---- Queue Stats ----
    print("\n--- Message Queue Stats ---")
    stats = broker.get_queue_stats()
    for topic_name, count in stats.items():
        print(f"  {topic_name}: {count} messages processed")

    # ---- Subscriber Message Counts ----
    print("\n--- Subscriber Message Counts ---")
    print(f"  Alice received: {len(alice.received_messages)} messages")
    print(f"  Bob received: {len(bob.received_messages)} messages")
    print(f"  FileLogger wrote: {len(file_logger.written_messages)} messages")
    print(f"  EmailAlert sent: {len(email_alert.sent_emails)} emails")
    print(f"  Charlie received: {len(charlie.received_messages)} messages")

    # ---- Error Handling Demo ----
    print_separator()
    print("--- Error Handling Demos ---")

    # Duplicate topic
    try:
        broker.create_topic("sports")
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Subscribe to non-existent topic
    try:
        broker.subscribe("non_existent", alice)
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Empty message content
    try:
        Message("sports", "")
    except ValueError as e:
        print(f"  [ERROR] {e}")

    # Empty publisher name
    try:
        Publisher("")
    except ValueError as e:
        print(f"  [ERROR] {e}")

    print_separator("SIMULATION COMPLETE")
    print()


if __name__ == "__main__":
    main()
