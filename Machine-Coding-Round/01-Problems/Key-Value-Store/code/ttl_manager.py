"""TTL (Time-to-Live) manager for the Key-Value Store."""

import time


class TTLManager:
    """Manages expiration times for keys in the store."""

    def __init__(self):
        self._expiry = {}  # key -> expiry_timestamp (Unix time)

    def set_ttl(self, key, seconds):
        """Set a TTL for a key. The key will expire after `seconds` seconds."""
        if seconds <= 0:
            print(f"[ERROR] TTL must be positive, got {seconds}")
            return False
        self._expiry[key] = time.time() + seconds
        return True

    def is_expired(self, key):
        """Check if a key has expired."""
        if key not in self._expiry:
            return False
        return time.time() > self._expiry[key]

    def get_ttl(self, key):
        """
        Get remaining TTL for a key.
        Returns:
            Remaining seconds (int) if TTL is set and not expired
            -1 if key exists but has no TTL
            -2 if key's TTL has expired
        """
        if key not in self._expiry:
            return -1
        remaining = self._expiry[key] - time.time()
        if remaining <= 0:
            return -2
        return int(remaining)

    def remove_ttl(self, key):
        """Remove TTL for a key (make it persistent)."""
        self._expiry.pop(key, None)

    def cleanup_expired(self, data):
        """Remove all expired keys from the data dict. Returns list of removed keys."""
        expired_keys = [k for k in list(self._expiry.keys()) if self.is_expired(k)]
        for key in expired_keys:
            data.pop(key, None)
            del self._expiry[key]
        return expired_keys

    def get_snapshot(self):
        """Get a copy of the TTL data for snapshots."""
        return dict(self._expiry)

    def restore_snapshot(self, expiry_data):
        """Restore TTL data from a snapshot."""
        self._expiry = dict(expiry_data)
