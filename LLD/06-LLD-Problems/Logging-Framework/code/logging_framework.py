"""
Logging Framework - Low Level Design
Run: python logging_framework.py

DESIGN PATTERN SHOWCASE - Uses 5+ patterns:
  1. Chain of Responsibility (logger hierarchy)
  2. Strategy (output handlers)
  3. Singleton (root logger)
  4. Observer (handler notification)
  5. Decorator (formatter enhancement)
  6. Template Method (handler base)
"""
from abc import ABC, abstractmethod
from datetime import datetime
from enum import IntEnum
import threading
import io


# ─── Log Levels ──────────────────────────────────────────────────────
class LogLevel(IntEnum):
    DEBUG = 10
    INFO = 20
    WARN = 30
    ERROR = 40
    FATAL = 50


# ─── Log Record ──────────────────────────────────────────────────────
class LogRecord:
    def __init__(self, level: LogLevel, message: str, logger_name: str):
        self.level = level
        self.message = message
        self.logger_name = logger_name
        self.timestamp = datetime.now()
        self.thread_name = threading.current_thread().name


# ─── Filters ─────────────────────────────────────────────────────────
class LogFilter(ABC):
    @abstractmethod
    def should_log(self, record: LogRecord) -> bool:
        pass


class LevelFilter(LogFilter):
    def __init__(self, min_level: LogLevel):
        self.min_level = min_level

    def should_log(self, record: LogRecord) -> bool:
        return record.level >= self.min_level


class KeywordFilter(LogFilter):
    """Only log messages containing a specific keyword."""
    def __init__(self, keyword: str, exclude: bool = False):
        self.keyword = keyword
        self.exclude = exclude

    def should_log(self, record: LogRecord) -> bool:
        contains = self.keyword.lower() in record.message.lower()
        return not contains if self.exclude else contains


# ─── Decorator Pattern: Formatters ───────────────────────────────────
class Formatter(ABC):
    @abstractmethod
    def format(self, record: LogRecord) -> str:
        pass


class SimpleFormatter(Formatter):
    """Base formatter: [LEVEL] message"""
    def format(self, record: LogRecord) -> str:
        return f"[{record.level.name:5s}] {record.message}"


class TimestampDecorator(Formatter):
    """Decorator: adds timestamp prefix."""
    def __init__(self, wrapped: Formatter):
        self._wrapped = wrapped

    def format(self, record: LogRecord) -> str:
        base = self._wrapped.format(record)
        ts = record.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"{ts} {base}"


class ThreadInfoDecorator(Formatter):
    """Decorator: adds thread name."""
    def __init__(self, wrapped: Formatter):
        self._wrapped = wrapped

    def format(self, record: LogRecord) -> str:
        base = self._wrapped.format(record)
        return f"[{record.thread_name}] {base}"


class LoggerNameDecorator(Formatter):
    """Decorator: adds logger name."""
    def __init__(self, wrapped: Formatter):
        self._wrapped = wrapped

    def format(self, record: LogRecord) -> str:
        base = self._wrapped.format(record)
        return f"({record.logger_name}) {base}"


# ─── Strategy / Template Method: Handlers ────────────────────────────
class LogHandler(ABC):
    def __init__(self, level: LogLevel = LogLevel.DEBUG,
                 formatter: Formatter = None):
        self.level = level
        self.formatter = formatter or SimpleFormatter()
        self.filters: list[LogFilter] = []
        self._lock = threading.Lock()

    def add_filter(self, f: LogFilter):
        self.filters.append(f)

    def can_handle(self, record: LogRecord) -> bool:
        if record.level < self.level:
            return False
        return all(f.should_log(record) for f in self.filters)

    def handle(self, record: LogRecord):
        if not self.can_handle(record):
            return
        with self._lock:
            formatted = self.formatter.format(record)
            self.emit(formatted, record)

    @abstractmethod
    def emit(self, formatted_msg: str, record: LogRecord):
        pass


class ConsoleHandler(LogHandler):
    def emit(self, formatted_msg: str, record: LogRecord):
        print(formatted_msg)


class StringHandler(LogHandler):
    """Writes to a StringIO buffer (for testing/demo instead of real file)."""
    def __init__(self, buffer: io.StringIO, **kwargs):
        super().__init__(**kwargs)
        self.buffer = buffer

    def emit(self, formatted_msg: str, record: LogRecord):
        self.buffer.write(formatted_msg + "\n")


class InMemoryDatabaseHandler(LogHandler):
    """Simulates writing to a database by storing records in a list."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.records: list[dict] = []

    def emit(self, formatted_msg: str, record: LogRecord):
        self.records.append({
            "level": record.level.name,
            "message": record.message,
            "logger": record.logger_name,
            "timestamp": record.timestamp.isoformat(),
            "thread": record.thread_name,
        })


# ─── Chain of Responsibility: Logger ─────────────────────────────────
class Logger:
    def __init__(self, name: str, level: LogLevel = None,
                 parent: "Logger" = None):
        self.name = name
        self._level = level
        self.parent = parent
        self.handlers: list[LogHandler] = []
        self.propagate = True  # pass records to parent?

    @property
    def effective_level(self) -> LogLevel:
        """Walk up hierarchy to find first explicitly set level."""
        if self._level is not None:
            return self._level
        if self.parent:
            return self.parent.effective_level
        return LogLevel.DEBUG  # default

    def set_level(self, level: LogLevel):
        self._level = level

    def add_handler(self, handler: LogHandler):
        self.handlers.append(handler)

    def is_enabled_for(self, level: LogLevel) -> bool:
        return level >= self.effective_level

    def log(self, level: LogLevel, message: str):
        if not self.is_enabled_for(level):
            return
        record = LogRecord(level, message, self.name)
        self._handle(record)

    def _handle(self, record: LogRecord):
        """Chain of Responsibility: handle locally, then propagate to parent."""
        for handler in self.handlers:
            handler.handle(record)
        if self.propagate and self.parent:
            self.parent._handle(record)

    # Convenience methods
    def debug(self, msg: str): self.log(LogLevel.DEBUG, msg)
    def info(self, msg: str): self.log(LogLevel.INFO, msg)
    def warn(self, msg: str): self.log(LogLevel.WARN, msg)
    def error(self, msg: str): self.log(LogLevel.ERROR, msg)
    def fatal(self, msg: str): self.log(LogLevel.FATAL, msg)


# ─── Singleton: LogManager ──────────────────────────────────────────
class LogManager:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._loggers = {}
                cls._instance._root = Logger("root", LogLevel.WARN)
            return cls._instance

    def get_root_logger(self) -> Logger:
        return self._root

    def get_logger(self, name: str) -> Logger:
        if name in self._loggers:
            return self._loggers[name]

        # Build hierarchy: "app.db" -> parent "app" -> parent "root"
        parent = self._root
        parts = name.split(".")
        for i in range(len(parts) - 1):
            parent_name = ".".join(parts[:i + 1])
            if parent_name not in self._loggers:
                self._loggers[parent_name] = Logger(parent_name, parent=parent)
            parent = self._loggers[parent_name]

        logger = Logger(name, parent=parent)
        self._loggers[name] = logger
        return logger

    @classmethod
    def reset(cls):
        """Reset for testing."""
        cls._instance = None


# ─── Demo ────────────────────────────────────────────────────────────
def main():
    LogManager.reset()
    manager = LogManager()

    # ── 1. Basic Setup: Root logger with console handler ──
    print("=" * 65)
    print("1. BASIC LOGGING (Root Logger)")
    print("=" * 65)
    root = manager.get_root_logger()
    root.set_level(LogLevel.INFO)

    # Build decorated formatter: timestamp + thread + logger + base
    fmt = SimpleFormatter()
    fmt = LoggerNameDecorator(fmt)
    fmt = ThreadInfoDecorator(fmt)
    fmt = TimestampDecorator(fmt)

    console = ConsoleHandler(level=LogLevel.DEBUG, formatter=fmt)
    root.add_handler(console)

    root.debug("This won't show (DEBUG < INFO)")
    root.info("Application started")
    root.warn("Low disk space")
    root.error("Connection timeout")

    # ── 2. Logger Hierarchy (Chain of Responsibility) ──
    print(f"\n{'=' * 65}")
    print("2. LOGGER HIERARCHY (Chain of Responsibility)")
    print("=" * 65)
    app_logger = manager.get_logger("app")
    app_logger.set_level(LogLevel.DEBUG)

    db_logger = manager.get_logger("app.db")
    # db_logger inherits DEBUG from app_logger

    print(f"  Root effective level: {root.effective_level.name}")
    print(f"  app effective level: {app_logger.effective_level.name}")
    print(f"  app.db effective level: {db_logger.effective_level.name}")
    print()

    # db_logger logs propagate up: db -> app -> root (all with root's handler)
    db_logger.debug("Query: SELECT * FROM users")
    db_logger.info("Connected to database")
    db_logger.error("Deadlock detected!")

    # ── 3. Multiple Handlers ──
    print(f"\n{'=' * 65}")
    print("3. MULTIPLE HANDLERS (Strategy Pattern)")
    print("=" * 65)
    file_buf = io.StringIO()
    file_handler = StringHandler(file_buf, level=LogLevel.WARN,
                                  formatter=fmt)
    db_handler = InMemoryDatabaseHandler(level=LogLevel.ERROR,
                                          formatter=SimpleFormatter())

    app_logger.add_handler(file_handler)
    app_logger.add_handler(db_handler)

    app_logger.debug("Debug msg - console only")
    app_logger.info("Info msg - console only")
    app_logger.warn("Warning msg - console + file")
    app_logger.error("Error msg - console + file + db")

    print(f"\n  File buffer contents:")
    for line in file_buf.getvalue().strip().split("\n"):
        print(f"    {line}")

    print(f"\n  Database records: {len(db_handler.records)}")
    for rec in db_handler.records:
        print(f"    [{rec['level']}] {rec['message']}")

    # ── 4. Filtering ──
    print(f"\n{'=' * 65}")
    print("4. KEYWORD FILTER (exclude 'password')")
    print("=" * 65)
    secure_logger = manager.get_logger("app.security")
    secure_logger.set_level(LogLevel.DEBUG)
    # Exclude messages containing 'password'
    pwd_filter = KeywordFilter("password", exclude=True)
    secure_console = ConsoleHandler(formatter=fmt)
    secure_console.add_filter(pwd_filter)
    secure_logger.add_handler(secure_console)
    secure_logger.propagate = False  # don't duplicate to root

    secure_logger.info("User login successful")
    secure_logger.info("User changed password to 'abc123'")  # filtered!
    secure_logger.warn("Failed login attempt from 10.0.0.1")

    # ── 5. Decorator Pattern Demo ──
    print(f"\n{'=' * 65}")
    print("5. FORMATTER DECORATORS (stacking)")
    print("=" * 65)
    # Show progressive decoration
    record = LogRecord(LogLevel.ERROR, "Something broke", "demo")

    f1 = SimpleFormatter()
    print(f"  Base:       {f1.format(record)}")

    f2 = TimestampDecorator(f1)
    print(f"  +Timestamp: {f2.format(record)}")

    f3 = ThreadInfoDecorator(f2)
    print(f"  +Thread:    {f3.format(record)}")

    f4 = LoggerNameDecorator(f3)
    print(f"  +Logger:    {f4.format(record)}")

    # ── 6. Thread Safety Demo ──
    print(f"\n{'=' * 65}")
    print("6. THREAD SAFETY (5 threads logging concurrently)")
    print("=" * 65)
    thread_logger = manager.get_logger("app.threads")
    thread_logger.set_level(LogLevel.INFO)
    thread_logger.propagate = False
    counter_handler = InMemoryDatabaseHandler(level=LogLevel.DEBUG)
    thread_logger.add_handler(counter_handler)

    def worker(thread_id):
        for i in range(3):
            thread_logger.info(f"Thread-{thread_id} message {i}")

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print(f"  Total records logged: {len(counter_handler.records)} (expected 15)")
    thread_names = set(r["thread"] for r in counter_handler.records)
    print(f"  Unique threads: {len(thread_names)}")

    # ── 7. Pattern Summary ──
    print(f"\n{'=' * 65}")
    print("PATTERNS USED IN THIS IMPLEMENTATION:")
    print("=" * 65)
    patterns = [
        ("Chain of Responsibility", "Logger hierarchy (db -> app -> root)"),
        ("Strategy", "Handler implementations (Console, File, Database)"),
        ("Singleton", "LogManager - single global instance"),
        ("Observer", "Handlers notified of log events"),
        ("Decorator", "Formatter stacking (timestamp + thread + logger)"),
        ("Template Method", "LogHandler.handle() calls abstract emit()"),
    ]
    for name, usage in patterns:
        print(f"  {name:30s} -> {usage}")


if __name__ == "__main__":
    main()
