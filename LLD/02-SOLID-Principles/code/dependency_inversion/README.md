# Dependency Inversion Principle (DIP)

> "High-level modules should not depend on low-level modules. Both should
> depend on abstractions."

## The Idea
Don't let business logic (high-level) directly depend on implementation
details (low-level). Insert an **abstraction** between them.

## Real-World Analogy
**Wall socket.** Your laptop depends on the socket interface (2-pin, 3-pin),
not the house wiring. You can change the wiring without changing the laptop.
The socket IS the abstraction.

## Before vs After
```
BEFORE (violation):   OrderService -> GmailClient
AFTER (fixed):        OrderService -> EmailClient <- GmailClient
                                      (abstraction)
```

## Dependency Injection (DI)
The practical tool for implementing DIP:
```python
# BAD: Service creates its own dependency
class Service:
    def __init__(self):
        self.db = PostgresDB()  # Tightly coupled

# GOOD: Dependency injected from outside
class Service:
    def __init__(self, db: Database):  # Abstract type
        self.db = db  # Can be Postgres, MySQL, Mock, etc.
```

## Types of Injection
| Type | How | Example |
|------|-----|---------|
| Constructor | Via `__init__` | `Service(db=PostgresDB())` |
| Method | Via method param | `service.process(parser=JSONParser())` |
| Property | Via setter | `service.logger = FileLogger()` |

## Interview Tip
> "DIP is about direction of dependency. High-level policy should NOT know
> about low-level details. Both point toward the abstraction. This is what
> makes code testable - inject mocks for the abstraction."

## Files in This Folder
| File | Shows |
|------|-------|
| `violation.py` | NotificationService creates GmailClient directly |
| `fixed.py` | Both depend on EmailClient abstraction |
| `with_di.py` | Constructor injection for full testability |
