"""Transaction manager for the Key-Value Store."""

import copy


class TransactionManager:
    """
    Manages nested transactions using a stack of change sets.

    Each BEGIN pushes a snapshot of the current data.
    COMMIT merges changes into the parent.
    ROLLBACK restores the snapshot (discards changes).
    """

    def __init__(self):
        self._stack = []  # Stack of data snapshots (copies before each BEGIN)

    def begin(self, current_data):
        """Start a new transaction. Saves a snapshot of current data."""
        snapshot = copy.deepcopy(current_data)
        self._stack.append(snapshot)
        depth = len(self._stack)
        print(f"OK (Transaction started, depth: {depth})")
        return True

    def commit(self, current_data):
        """
        Commit all transactions. Clears the transaction stack.
        The current_data already has all changes applied, so we just
        clear the stack.
        Returns True if committed, False if no transaction.
        """
        if not self._stack:
            print("[ERROR] No transaction to commit")
            return False, current_data

        self._stack.clear()
        print("OK (Transaction committed)")
        return True, current_data

    def rollback(self, current_data):
        """
        Rollback the innermost transaction.
        Restores data to the snapshot taken at the last BEGIN.
        Returns (success, restored_data).
        """
        if not self._stack:
            print("[ERROR] No transaction to rollback")
            return False, current_data

        restored = self._stack.pop()
        depth = len(self._stack)
        print(f"OK (Transaction rolled back, depth: {depth})")
        return True, restored

    def in_transaction(self):
        """Check if we are inside a transaction."""
        return len(self._stack) > 0

    def depth(self):
        """Current transaction nesting depth."""
        return len(self._stack)
