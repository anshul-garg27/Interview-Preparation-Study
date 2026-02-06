"""
DoublyLinkedList Node for cache implementations.
Stores a key-value pair and pointers to previous/next nodes.
"""


class Node:
    """Node in a doubly linked list storing a key-value pair."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: int = 0, value: int = 0) -> None:
        self.key: int = key
        self.value: int = value
        self.prev: "Node | None" = None
        self.next: "Node | None" = None

    def __repr__(self) -> str:
        return f"({self.key}:{self.value})"
