"""
LRU Cache using HashMap + Doubly Linked List.
O(1) get and put operations with least-recently-used eviction.
"""

from node import Node
from doubly_linked_list import DoublyLinkedList


class LRUCache:
    """
    Least Recently Used Cache.
    - get(key): O(1) - returns value or -1 on miss
    - put(key, value): O(1) - inserts/updates, evicts LRU if at capacity
    """

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._cache: dict[int, Node] = {}
        self._dll = DoublyLinkedList()
        self._trace: bool = True

    @property
    def size(self) -> int:
        return self._dll.size

    def _print_state(self, operation: str) -> None:
        if self._trace:
            items = self._dll.to_list()
            print(f"    {operation:30s} -> Cache: [{', '.join(items)}] (size={self._dll.size})")

    def get(self, key: int) -> int:
        """Get value by key. Returns -1 if not found."""
        if key in self._cache:
            node = self._cache[key]
            self._dll.move_to_front(node)
            self._print_state(f"GET({key}) = {node.value}")
            return node.value
        self._print_state(f"GET({key}) = -1 (miss)")
        return -1

    def put(self, key: int, value: int) -> None:
        """Insert or update a key-value pair. Evicts LRU if at capacity."""
        if key in self._cache:
            node = self._cache[key]
            old_val = node.value
            node.value = value
            self._dll.move_to_front(node)
            self._print_state(f"PUT({key},{value}) updated from {old_val}")
        else:
            evicted = None
            if self._dll.size >= self._capacity:
                lru = self._dll.remove_from_back()
                evicted = lru.key
                del self._cache[lru.key]
            node = Node(key, value)
            self._dll.add_to_front(node)
            self._cache[key] = node
            if evicted is not None:
                self._print_state(f"PUT({key},{value}) evicted key={evicted}")
            else:
                self._print_state(f"PUT({key},{value}) inserted")
