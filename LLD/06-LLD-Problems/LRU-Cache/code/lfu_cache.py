"""
LFU (Least Frequently Used) Cache variation.
Evicts the key with the lowest access frequency; ties broken by LRU order.
"""

from collections import defaultdict

from node import Node
from doubly_linked_list import DoublyLinkedList


class LFUCache:
    """
    Least Frequently Used Cache.
    - get(key): O(1)
    - put(key, value): O(1)
    Evicts the least frequently used key; ties broken by LRU.
    """

    def __init__(self, capacity: int) -> None:
        self._capacity = capacity
        self._cache: dict[int, Node] = {}
        self._freq: dict[int, int] = {}               # key -> frequency
        self._freq_lists: dict[int, DoublyLinkedList] = defaultdict(DoublyLinkedList)
        self._min_freq: int = 0
        self._trace: bool = True

    def _print_state(self, operation: str) -> None:
        if self._trace:
            items = [f"{k}:{self._cache[k].value}(f={self._freq[k]})" for k in self._cache]
            print(f"    {operation:35s} -> [{', '.join(items)}] min_freq={self._min_freq}")

    def _update_freq(self, key: int) -> None:
        """Increment frequency of a key and move it to the new frequency list."""
        freq = self._freq[key]
        node = self._cache[key]
        self._freq_lists[freq].remove_node(node)
        if self._freq_lists[freq].size == 0 and freq == self._min_freq:
            self._min_freq += 1
        self._freq[key] = freq + 1
        self._freq_lists[freq + 1].add_to_front(node)

    def get(self, key: int) -> int:
        """Get value by key. Returns -1 if not found."""
        if key not in self._cache:
            self._print_state(f"GET({key}) = -1 (miss)")
            return -1
        self._update_freq(key)
        val = self._cache[key].value
        self._print_state(f"GET({key}) = {val}")
        return val

    def put(self, key: int, value: int) -> None:
        """Insert or update a key-value pair. Evicts LFU on capacity overflow."""
        if self._capacity <= 0:
            return
        if key in self._cache:
            self._cache[key].value = value
            self._update_freq(key)
            self._print_state(f"PUT({key},{value}) updated")
            return
        if len(self._cache) >= self._capacity:
            # Evict least frequently used (LRU among ties)
            lfu_list = self._freq_lists[self._min_freq]
            evicted = lfu_list.remove_from_back()
            del self._cache[evicted.key]
            del self._freq[evicted.key]
            self._print_state(f"PUT({key},{value}) evicted key={evicted.key}")
        node = Node(key, value)
        self._cache[key] = node
        self._freq[key] = 1
        self._freq_lists[1].add_to_front(node)
        self._min_freq = 1
        if len(self._cache) <= self._capacity:
            self._print_state(f"PUT({key},{value}) inserted")
