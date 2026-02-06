# Logging Framework - Low Level Design

## Problem Statement
Design a flexible logging framework similar to Log4j / Python's logging module. The system should support multiple log levels, output handlers, formatters, filtering, and a logger hierarchy. This problem is a **design pattern showcase** -- it naturally uses 5+ patterns.

---

## Functional Requirements
1. **Log Levels** - DEBUG, INFO, WARN, ERROR, FATAL (with level filtering)
2. **Multiple Handlers** - Console, File, Database (pluggable)
3. **Log Formatting** - Customizable templates (timestamp, level, message, thread)
4. **Logger Hierarchy** - Root logger with child loggers that inherit config
5. **Filtering** - Filter by level, keyword, or custom predicate
6. **Thread-Safe** - Safe for concurrent logging

## Non-Functional Requirements
- Minimal performance overhead when logging is disabled
- No log message loss under high concurrency
- Lazy message formatting (don't format if level is filtered out)

---

## Design Patterns Used (5+)

This problem is a **pattern showcase** -- one of the richest pattern-dense designs:

| Pattern | Where Used | Why |
|---------|-----------|-----|
| **Chain of Responsibility** | Log level filtering through logger hierarchy | Pass log record up the chain until handled |
| **Strategy** | Output handlers (Console, File, Database) | Different output destinations, same interface |
| **Singleton** | Root logger | Single global entry point |
| **Observer** | Handler notification on log events | Decouple log generation from output |
| **Decorator** | Adding timestamp, thread-id, formatting layers | Enhance log records without modifying core |
| **Template Method** | Handler base class with format/write/flush template | Common algorithm, customizable steps |

### Chain of Responsibility -- Logger Hierarchy
```
RootLogger (WARN) → AppLogger (INFO) → DBLogger (DEBUG)
```
A log record flows from child to parent. Each logger checks its level threshold and passes to its handlers if appropriate, then delegates to its parent.

### Strategy -- Output Handlers
Each handler (Console, File, Database) implements the same interface but writes to different destinations. You can attach any combination of handlers to any logger.

### Decorator -- Log Enhancement
Decorators wrap a formatter to add layers: timestamp, thread name, stack trace, etc. Each decorator adds one piece of information without knowing about others.

---

## Class Diagram

```mermaid
classDiagram
    class LogLevel {
        <<enumeration>>
        DEBUG = 10
        INFO = 20
        WARN = 30
        ERROR = 40
        FATAL = 50
    }

    class LogRecord {
        -LogLevel level
        -String message
        -datetime timestamp
        -String logger_name
        -String thread_name
        +format() String
    }

    class LogFilter {
        <<interface>>
        +should_log(record) bool
    }

    class LevelFilter {
        -LogLevel min_level
        +should_log(record) bool
    }

    class KeywordFilter {
        -String keyword
        +should_log(record) bool
    }

    class Formatter {
        <<interface>>
        +format(record) String
    }

    class SimpleFormatter {
        -String pattern
        +format(record) String
    }

    class TimestampDecorator {
        -Formatter wrapped
        +format(record) String
    }

    class ThreadInfoDecorator {
        -Formatter wrapped
        +format(record) String
    }

    class LogHandler {
        <<abstract>>
        -Formatter formatter
        -LogLevel level
        -List~LogFilter~ filters
        +handle(record)*
        +set_formatter(formatter)
        +add_filter(filter)
        #can_handle(record) bool
    }

    class ConsoleHandler {
        +handle(record)
    }

    class FileHandler {
        -String file_path
        +handle(record)
    }

    class DatabaseHandler {
        -List~LogRecord~ records
        +handle(record)
    }

    class Logger {
        -String name
        -LogLevel level
        -Logger parent
        -List~LogHandler~ handlers
        -bool propagate
        +debug(message)
        +info(message)
        +warn(message)
        +error(message)
        +fatal(message)
        +log(level, message)
        +add_handler(handler)
        +set_level(level)
    }

    class LogManager {
        -Map~String, Logger~ loggers
        -Logger root_logger
        +get_logger(name) Logger
        +get_root_logger() Logger
    }

    LogFilter <|.. LevelFilter
    LogFilter <|.. KeywordFilter
    Formatter <|.. SimpleFormatter
    Formatter <|.. TimestampDecorator
    Formatter <|.. ThreadInfoDecorator
    TimestampDecorator --> Formatter : wraps
    ThreadInfoDecorator --> Formatter : wraps
    LogHandler <|-- ConsoleHandler
    LogHandler <|-- FileHandler
    LogHandler <|-- DatabaseHandler
    LogHandler --> Formatter
    LogHandler --> LogFilter
    Logger --> LogHandler
    Logger --> Logger : parent
    LogManager --> Logger
```

---

## Sequence Diagram - Logging a Message

```mermaid
sequenceDiagram
    participant App as Application
    participant L as Logger ("app.db")
    participant P as Parent Logger ("app")
    participant R as Root Logger
    participant H1 as ConsoleHandler
    participant H2 as FileHandler
    participant F as Formatter

    App->>L: logger.error("Connection failed")
    L->>L: Create LogRecord(ERROR, msg)
    L->>L: Check level >= Logger.level?
    L->>H1: handle(record) [logger's own handler]
    H1->>H1: Check level >= Handler.level?
    H1->>H1: Apply filters
    H1->>F: format(record)
    F-->>H1: "[ERROR] 2024-01-15 10:30:00 - Connection failed"
    H1->>H1: Write to console

    Note over L,P: propagate=True → pass to parent
    L->>P: log(record)
    P->>H2: handle(record) [parent's handler]
    H2->>F: format(record)
    H2->>H2: Write to file

    P->>R: log(record) [propagate to root]
    R->>R: Handle with root handlers
```

## Sequence Diagram - Logger Hierarchy Resolution

```mermaid
sequenceDiagram
    participant C as Client
    participant LM as LogManager
    participant RL as Root Logger
    participant AL as "app" Logger
    participant DL as "app.db" Logger

    C->>LM: get_logger("app.db")
    LM->>LM: Check cache
    alt Not cached
        LM->>DL: Create Logger("app.db")
        LM->>LM: Find parent: "app"
        LM->>AL: get_or_create Logger("app")
        LM->>AL: Set parent = Root
        LM->>DL: Set parent = "app" Logger
    end
    LM-->>C: Logger("app.db")
    Note over DL: Inherits level from parent<br/>if not explicitly set
```

---

## Edge Cases
1. **Circular logger hierarchy** - Prevent parent cycles
2. **Handler exceptions** - Handler failure shouldn't crash the app
3. **Lazy formatting** - Don't format message if level is filtered out
4. **Null handler** - Logger with no handlers (discard silently)
5. **File rotation** - Handle log files growing too large
6. **Thread name in logs** - Include thread context for debugging
7. **Log during shutdown** - Flush all handlers on application exit
8. **Performance** - Logging in hot paths; use level checks before formatting

## Extensions
- Structured logging (JSON format)
- Log rotation (size-based, time-based)
- Remote log shipping (to ELK, Splunk)
- Async logging (background thread for I/O)
- MDC (Mapped Diagnostic Context) per-thread
- Log sampling (log 1% of DEBUG in production)
- Log correlation IDs for distributed tracing

---

## Interview Tips

1. **Emphasize patterns** - This question is about demonstrating pattern knowledge; name every pattern you use
2. **Draw the logger hierarchy** - Root → app → app.db shows Chain of Responsibility
3. **Explain Decorator for formatting** - Stack formatters: base → timestamp → thread → stack trace
4. **Mention Singleton for root** - Single entry point to the logging subsystem
5. **Discuss lazy evaluation** - `logger.debug(f"Expensive: {compute()}")` should NOT call compute() if DEBUG is disabled; show how to use `logger.isEnabledFor(level)` or lambda-based messages
6. **Compare with real frameworks** - Reference Log4j, Python logging, SLF4J
7. **Common follow-up**: "How to handle logging in microservices?" - Structured logging + correlation IDs + centralized aggregation
