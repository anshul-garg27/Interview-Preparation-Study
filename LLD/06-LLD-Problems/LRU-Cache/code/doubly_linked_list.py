"""
DoublyLinkedList with sentinel head/tail for O(1) operations.
Used as the underlying data structure for LRU Cache.
"""

from node import Node


class DoublyLinkedList:
    """
    Doubly linked list with sentinel nodes.
    Most recently used at head, least recently used at tail.
    """

    def __init__(self) -> None:
        self._head = Node()  # sentinel head
        self._tail = Node()  # sentinel tail
        self._head.next = self._tail
        self._tail.prev = self._head
        self.size: int = 0

    def add_to_front(self, node: Node) -> None:
        """Add node right after the head sentinel (most recently used)."""
        node.prev = self._head
        node.next = self._head.next
        self._head.next.prev = node
        self._head.next = node
        self.size += 1

    def remove_node(self, node: Node) -> None:
        """Remove a node from its current position."""
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        self.size -= 1

    def remove_from_back(self) -> Node | None:
        """Remove and return the node before tail sentinel (LRU)."""
        if self.size == 0:
            return None
        lru = self._tail.prev
        self.remove_node(lru)
        return lru

    def move_to_front(self, node: Node) -> None:
        """Move existing node to front (mark as most recently used)."""
        self.remove_node(node)
        self.add_to_front(node)

    def to_list(self) -> list[str]:
        """Return list representation from MRU to LRU."""
        result: list[str] = []
        curr = self._head.next
        while curr != self._tail:
            result.append(f"{curr.key}:{curr.value}")
            curr = curr.next
        return result
