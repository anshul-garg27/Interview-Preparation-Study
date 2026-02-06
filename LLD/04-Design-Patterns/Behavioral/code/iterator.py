"""
Iterator Pattern - Provides a way to access elements of a collection
sequentially without exposing its underlying representation.

Examples:
1. Custom LinkedList with iterator
2. BinaryTree with DFS and BFS iterators
3. Social Network friends iterator (breadth-first)
"""
from collections import deque


# --- LinkedList Iterator ---
class Node:
    def __init__(self, data, next_node=None):
        self.data = data
        self.next = next_node


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        if not self.head:
            self.head = Node(data)
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = Node(data)
        return self

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next


# --- Binary Tree with DFS/BFS ---
class TreeNode:
    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class BinaryTree:
    def __init__(self, root: TreeNode):
        self.root = root

    def dfs_inorder(self):
        """In-order: Left, Root, Right."""
        def _traverse(node):
            if node:
                yield from _traverse(node.left)
                yield node.val
                yield from _traverse(node.right)
        return _traverse(self.root)

    def dfs_preorder(self):
        """Pre-order: Root, Left, Right."""
        def _traverse(node):
            if node:
                yield node.val
                yield from _traverse(node.left)
                yield from _traverse(node.right)
        return _traverse(self.root)

    def bfs(self):
        """Breadth-first (level order)."""
        if not self.root:
            return
        queue = deque([self.root])
        while queue:
            node = queue.popleft()
            yield node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)


# --- Social Network ---
class SocialUser:
    def __init__(self, name: str):
        self.name = name
        self.friends: list['SocialUser'] = []

    def add_friend(self, user: 'SocialUser'):
        self.friends.append(user)
        return self


class FriendsIterator:
    """BFS iterator to discover friends-of-friends."""
    def __init__(self, user: SocialUser, max_depth: int = 2):
        self.start = user
        self.max_depth = max_depth

    def __iter__(self):
        visited = {self.start.name}
        queue = deque([(friend, 1) for friend in self.start.friends])
        for friend in self.start.friends:
            visited.add(friend.name)

        while queue:
            user, depth = queue.popleft()
            yield user, depth
            if depth < self.max_depth:
                for friend in user.friends:
                    if friend.name not in visited:
                        visited.add(friend.name)
                        queue.append((friend, depth + 1))


if __name__ == "__main__":
    print("=" * 60)
    print("ITERATOR PATTERN DEMO")
    print("=" * 60)

    # LinkedList
    print("\n--- LinkedList Iterator ---")
    ll = LinkedList()
    ll.append(10).append(20).append(30).append(40)
    print(f"  Forward: {' -> '.join(str(x) for x in ll)}")
    print(f"  Sum: {sum(ll)}")

    # Binary Tree
    print("\n--- Binary Tree Iterators ---")
    #       4
    #      / \
    #     2   6
    #    / \ / \
    #   1  3 5  7
    tree = BinaryTree(
        TreeNode(4,
            TreeNode(2, TreeNode(1), TreeNode(3)),
            TreeNode(6, TreeNode(5), TreeNode(7)))
    )
    print(f"  In-order (DFS):  {list(tree.dfs_inorder())}")
    print(f"  Pre-order (DFS): {list(tree.dfs_preorder())}")
    print(f"  BFS (level):     {list(tree.bfs())}")

    # Social Network
    print("\n--- Social Network Friends Iterator ---")
    alice = SocialUser("Alice")
    bob = SocialUser("Bob")
    charlie = SocialUser("Charlie")
    diana = SocialUser("Diana")
    eve = SocialUser("Eve")
    frank = SocialUser("Frank")

    alice.add_friend(bob).add_friend(charlie)
    bob.add_friend(diana).add_friend(eve)
    charlie.add_friend(frank)

    print(f"  Friends network starting from Alice:")
    for user, depth in FriendsIterator(alice, max_depth=2):
        indent = "    " * depth
        label = "friend" if depth == 1 else "friend-of-friend"
        print(f"  {indent}{user.name} (depth {depth}, {label})")
