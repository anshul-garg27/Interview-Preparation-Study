"""Method Overriding - super() calls and cooperative inheritance."""


class Logger:
    """Base logger - writes to console."""

    def log(self, message: str) -> None:
        print(f"  [BASE] {message}")

    def error(self, message: str) -> None:
        print(f"  [ERROR] {message}")


class TimestampLogger(Logger):
    """Adds timestamp to every log message using super()."""

    def log(self, message: str) -> None:
        import datetime
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        super().log(f"[{ts}] {message}")  # Extend, don't replace

    # error() is inherited as-is from Logger


class FileLogger(Logger):
    """Logs to both console (via super) and records to a list."""

    def __init__(self):
        self.records: list[str] = []

    def log(self, message: str) -> None:
        super().log(message)              # Still log to console
        self.records.append(message)      # Also record

    def get_records(self) -> list[str]:
        return self.records


class FilteredLogger(Logger):
    """Completely overrides log() to filter short messages."""

    MIN_LENGTH = 5

    def log(self, message: str) -> None:
        if len(message) < self.MIN_LENGTH:
            return  # Skip short messages (full override, no super)
        super().log(message)


if __name__ == "__main__":
    print("=== Method Overriding ===\n")

    # Base behavior
    print("--- Base Logger ---")
    base = Logger()
    base.log("Hello world")

    # Extended with timestamp
    print("\n--- TimestampLogger (extends via super) ---")
    ts_logger = TimestampLogger()
    ts_logger.log("Server started")
    ts_logger.error("Something failed")  # Inherited, no override

    # Extended with recording
    print("\n--- FileLogger (extends + records) ---")
    file_logger = FileLogger()
    file_logger.log("Request received")
    file_logger.log("Response sent")
    print(f"  Recorded: {file_logger.get_records()}")

    # Full override with filtering
    print("\n--- FilteredLogger (full override) ---")
    filtered = FilteredLogger()
    filtered.log("Hi")                # Filtered out (too short)
    filtered.log("Hello world")       # Passes filter
    print("  ('Hi' was filtered out)")
