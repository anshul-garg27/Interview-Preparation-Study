"""Command parser for the Key-Value Store."""


class CommandParser:
    """Parses text commands and dispatches to the KeyValueStore."""

    def __init__(self, store):
        self._store = store

    def execute(self, line):
        """Parse and execute a single command line."""
        line = line.strip()
        if not line or line.startswith("#"):
            return

        parts = line.split()
        cmd = parts[0].upper()
        args = parts[1:]

        try:
            if cmd == "SET":
                self._handle_set(args)
            elif cmd == "GET":
                self._require_args(args, 1, "GET key")
                self._store.get(args[0])
            elif cmd == "DELETE":
                self._require_args(args, 1, "DELETE key")
                self._store.delete(args[0])
            elif cmd == "EXISTS":
                self._require_args(args, 1, "EXISTS key")
                self._store.exists(args[0])
            elif cmd == "KEYS":
                self._store.keys()
            elif cmd == "COUNT":
                self._store.count()
            elif cmd == "TTL":
                self._require_args(args, 1, "TTL key")
                self._store.ttl(args[0])
            elif cmd == "BEGIN":
                self._store.begin()
            elif cmd == "COMMIT":
                self._store.commit()
            elif cmd == "ROLLBACK":
                self._store.rollback()
            elif cmd == "SNAPSHOT":
                self._store.snapshot()
            elif cmd == "RESTORE":
                self._require_args(args, 1, "RESTORE snapshot_id")
                self._store.restore(args[0])
            elif cmd == "SNAPSHOTS":
                self._store.list_snapshots()
            else:
                print(f"[ERROR] Unknown command: {cmd}")
        except Exception as e:
            print(f"[ERROR] {e}")

    def _handle_set(self, args):
        """Handle SET key value [TTL seconds]."""
        if len(args) < 2:
            print("[ERROR] Usage: SET key value [TTL seconds]")
            return

        key = args[0]
        value = args[1]
        ttl = None

        if len(args) >= 4 and args[2].upper() == "TTL":
            try:
                ttl = int(args[3])
            except ValueError:
                print(f"[ERROR] TTL must be an integer, got '{args[3]}'")
                return

        self._store.set(key, value, ttl)

    def _require_args(self, args, count, usage):
        if len(args) < count:
            raise ValueError(f"Usage: {usage}")

    def process_commands(self, commands):
        """Process a list of command strings."""
        for cmd in commands:
            print(f"\n> {cmd}")
            self.execute(cmd)
