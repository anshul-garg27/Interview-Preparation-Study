"""Main Key-Value Store with GET, SET, DELETE, EXISTS operations."""

from transaction import TransactionManager
from ttl_manager import TTLManager
from snapshot import SnapshotManager


class KeyValueStore:
    """
    In-memory key-value store with transaction, TTL, and snapshot support.
    """

    def __init__(self):
        self._data = {}
        self._txn_mgr = TransactionManager()
        self._ttl_mgr = TTLManager()
        self._snap_mgr = SnapshotManager()

    # ── Basic Operations ────────────────────────────────────────────────

    def set(self, key, value, ttl=None):
        """Set a key to a value, optionally with TTL in seconds."""
        self._data[key] = value
        if ttl is not None:
            self._ttl_mgr.set_ttl(key, ttl)
            print(f"OK (expires in {ttl} seconds)")
        else:
            self._ttl_mgr.remove_ttl(key)
            print("OK")

    def get(self, key):
        """Get the value for a key. Returns NULL if not found or expired."""
        if key in self._data:
            if self._ttl_mgr.is_expired(key):
                # Clean up expired key
                del self._data[key]
                self._ttl_mgr.remove_ttl(key)
                print("NULL (expired)")
                return None
            value = self._data[key]
            print(value)
            return value
        print("NULL")
        return None

    def delete(self, key):
        """Delete a key from the store."""
        if key in self._data:
            del self._data[key]
            self._ttl_mgr.remove_ttl(key)
            print("OK")
            return True
        print(f"[ERROR] Key '{key}' not found")
        return False

    def exists(self, key):
        """Check if a key exists (and is not expired)."""
        if key in self._data:
            if self._ttl_mgr.is_expired(key):
                del self._data[key]
                self._ttl_mgr.remove_ttl(key)
                print("FALSE (expired)")
                return False
            print("TRUE")
            return True
        print("FALSE")
        return False

    def keys(self):
        """List all keys and their values."""
        # Clean up expired keys first
        self._ttl_mgr.cleanup_expired(self._data)

        if not self._data:
            print("(empty)")
            return []

        for key in sorted(self._data.keys()):
            ttl = self._ttl_mgr.get_ttl(key)
            ttl_str = f" (TTL: {ttl}s)" if ttl > 0 else ""
            print(f"  {key}: {self._data[key]}{ttl_str}")

        return sorted(self._data.keys())

    def count(self):
        """Return the number of active keys."""
        self._ttl_mgr.cleanup_expired(self._data)
        cnt = len(self._data)
        print(f"{cnt}")
        return cnt

    # ── TTL Operations ──────────────────────────────────────────────────

    def ttl(self, key):
        """Show remaining TTL for a key."""
        if key not in self._data or self._ttl_mgr.is_expired(key):
            print("-2 (not found or expired)")
            return -2

        remaining = self._ttl_mgr.get_ttl(key)
        if remaining == -1:
            print("-1 (no TTL set)")
        else:
            print(f"{remaining}")
        return remaining

    # ── Transaction Operations ──────────────────────────────────────────

    def begin(self):
        """Start a new transaction."""
        self._txn_mgr.begin(self._data)

    def commit(self):
        """Commit the current transaction."""
        success, data = self._txn_mgr.commit(self._data)
        if success:
            self._data = data

    def rollback(self):
        """Rollback the current transaction."""
        success, data = self._txn_mgr.rollback(self._data)
        if success:
            self._data = data

    # ── Snapshot Operations ─────────────────────────────────────────────

    def snapshot(self):
        """Take a point-in-time snapshot."""
        self._ttl_mgr.cleanup_expired(self._data)
        return self._snap_mgr.take_snapshot(self._data, self._ttl_mgr.get_snapshot())

    def restore(self, snapshot_id):
        """Restore from a snapshot."""
        data, ttl_data = self._snap_mgr.restore_snapshot(snapshot_id)
        if data is not None:
            self._data = data
            self._ttl_mgr.restore_snapshot(ttl_data)

    def list_snapshots(self):
        """List all available snapshots."""
        self._snap_mgr.list_snapshots()
