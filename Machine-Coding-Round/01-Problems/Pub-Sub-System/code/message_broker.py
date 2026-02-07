"""Central Message Broker orchestrating the Pub-Sub system."""

import threading
from typing import Dict, List, Optional

from enums import MessageStatus
from message import Message
from topic import Topic
from subscriber import Subscriber
from message_queue import MessageQueue
from dead_letter_queue import DeadLetterQueue


class MessageBroker:
    """Central broker that manages topics, subscriptions, and message delivery.

    Handles topic creation, subscriber management, message routing,
    and async delivery via background threads.

    Attributes:
        topics: Dictionary of topic name to Topic objects.
        queues: Dictionary of topic name to MessageQueue objects.
        dlq: Dead letter queue for failed deliveries.
    """

    def __init__(self) -> None:
        """Initialize the MessageBroker."""
        self._topics: Dict[str, Topic] = {}
        self._queues: Dict[str, MessageQueue] = {}
        self._dlq = DeadLetterQueue()
        self._lock = threading.Lock()
        self._delivery_log: List[str] = []

    def create_topic(self, name: str) -> Topic:
        """Create a new topic.

        Args:
            name: Name of the topic.

        Returns:
            The created Topic object.

        Raises:
            ValueError: If topic already exists.
        """
        with self._lock:
            if name in self._topics:
                raise ValueError(f"Topic '{name}' already exists.")
            topic = Topic(name)
            self._topics[name] = topic
            self._queues[name] = MessageQueue(name)
            return topic

    def get_topic(self, name: str) -> Optional[Topic]:
        """Get a topic by name.

        Args:
            name: Topic name.

        Returns:
            The Topic, or None if not found.
        """
        return self._topics.get(name)

    def list_topics(self) -> List[Topic]:
        """List all topics."""
        return list(self._topics.values())

    def subscribe(self, topic_name: str, subscriber: Subscriber) -> bool:
        """Subscribe to a topic.

        Args:
            topic_name: Name of the topic.
            subscriber: The subscriber to add.

        Returns:
            True if subscription was successful.

        Raises:
            ValueError: If topic does not exist.
        """
        topic = self._topics.get(topic_name)
        if topic is None:
            raise ValueError(f"Topic '{topic_name}' does not exist.")
        return topic.subscribe(subscriber)

    def unsubscribe(self, topic_name: str, subscriber: Subscriber) -> bool:
        """Unsubscribe from a topic.

        Args:
            topic_name: Name of the topic.
            subscriber: The subscriber to remove.

        Returns:
            True if unsubscription was successful.

        Raises:
            ValueError: If topic does not exist.
        """
        topic = self._topics.get(topic_name)
        if topic is None:
            raise ValueError(f"Topic '{topic_name}' does not exist.")
        return topic.unsubscribe(subscriber)

    def publish(self, topic_name: str, message: Message) -> None:
        """Publish a message to a topic and deliver to subscribers.

        Messages are queued and then delivered to all subscribers.
        Failed deliveries are sent to the dead letter queue.

        Args:
            topic_name: Name of the topic.
            message: The message to publish.

        Raises:
            ValueError: If topic does not exist.
        """
        topic = self._topics.get(topic_name)
        if topic is None:
            raise ValueError(f"Topic '{topic_name}' does not exist.")

        queue = self._queues[topic_name]
        queue.enqueue(message)

        # Deliver via a background thread
        thread = threading.Thread(
            target=self._deliver_messages, args=(topic, queue), daemon=True
        )
        thread.start()
        thread.join(timeout=5)  # Wait for delivery in demo context

    def _deliver_messages(self, topic: Topic, queue: MessageQueue) -> None:
        """Deliver queued messages to all subscribers of a topic.

        Args:
            topic: The topic to deliver for.
            queue: The message queue to drain.
        """
        while not queue.is_empty():
            message = queue.dequeue()
            if message is None:
                break

            subscribers = topic.subscribers
            if not subscribers:
                continue

            for subscriber in subscribers:
                # Check filter
                if not subscriber.should_receive(message):
                    self._delivery_log.append(
                        f"FILTERED: {subscriber.name} | {message.content}"
                    )
                    continue

                # Attempt delivery
                try:
                    success = subscriber.on_message(message)
                    if success:
                        message.mark_delivered()
                    else:
                        message.mark_failed()
                        self._dlq.add(message, subscriber, "Delivery returned False")
                except Exception as e:
                    message.mark_failed()
                    self._dlq.add(message, subscriber, str(e))

    @property
    def dead_letter_queue(self) -> DeadLetterQueue:
        """Access the dead letter queue."""
        return self._dlq

    def get_queue_stats(self) -> Dict[str, int]:
        """Get processed message counts per topic."""
        return {
            name: q.processed_count for name, q in self._queues.items()
        }

    def __str__(self) -> str:
        return f"MessageBroker(topics={len(self._topics)}, dlq={self._dlq.size()})"
