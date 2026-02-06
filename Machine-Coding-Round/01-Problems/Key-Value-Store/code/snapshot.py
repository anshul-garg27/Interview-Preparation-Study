"""Snapshot manager for the Key-Value Store."""

import copy


class Snapshot:
    """Represents a point-in-time snapshot of the store."""

    _counter = 0

    def __init__(self, data, ttl_data):
        Snapshot._counter += 1
        self.id = f"S-{Snapshot._counter:03d}"
        self.data = copy.deepcopy(data)
        self.ttl_data = copy.deepcopy(ttl_data)
        self.key_count = len(data)

    def __str__(self):
        return f"Snapshot {self.id} ({self.key_count} keys)"


class SnapshotManager:
    """Manages point-in-time snapshots of the store."""

    def __init__(self):
        self._snapshots = {}  # snapshot_id -> Snapshot

    def take_snapshot(self, data, ttl_data):
        """Take a snapshot of the current store state."""
        snapshot = Snapshot(data, ttl_data)
        self._snapshots[snapshot.id] = snapshot
        print(f"Snapshot {snapshot.id} created ({snapshot.key_count} keys)")
        return snapshot

    def restore_snapshot(self, snapshot_id):
        """
        Restore a snapshot. Returns (data, ttl_data) or (None, None) if not found.
        """
        snapshot = self._snapshots.get(snapshot_id)
        if not snapshot:
            print(f"[ERROR] Snapshot '{snapshot_id}' not found")
            return None, None

        data = copy.deepcopy(snapshot.data)
        ttl_data = copy.deepcopy(snapshot.ttl_data)
        print(f"Restored from {snapshot}")
        return data, ttl_data

    def list_snapshots(self):
        """List all available snapshots."""
        if not self._snapshots:
            print("  (no snapshots)")
            return []
        print(f"\n  Available Snapshots:")
        print(f"  {'-' * 35}")
        for snap in self._snapshots.values():
            print(f"  {snap}")
        print(f"  {'-' * 35}")
        return list(self._snapshots.values())
