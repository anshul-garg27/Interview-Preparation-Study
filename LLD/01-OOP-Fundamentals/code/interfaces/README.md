# Interfaces in Python

## What Are They?
An interface defines a **contract** - a set of methods that a class must
implement. Python has two approaches:

## Two Approaches
| Approach | Type | Enforcement | Inheritance Needed |
|----------|------|-------------|-------------------|
| ABC | Nominal | At instantiation | Yes (explicit) |
| Protocol | Structural | At type-check time | No (duck typing) |

## When to Use Which
```python
# ABC: When you want ENFORCED contracts + shared code
class Notifier(ABC):
    @abstractmethod
    def send(self, msg: str): ...
    def retry(self, msg: str):  # Shared concrete method
        for _ in range(3): self.send(msg)

# Protocol: When you want duck-typing + type safety
class Drawable(Protocol):
    def draw(self) -> str: ...
# Any class with draw() method satisfies this - no inheritance needed
```

## Multiple Interfaces
Python supports implementing multiple interfaces (via multiple inheritance):
```python
class Circle(Drawable, Serializable, Comparable):
    ...
```

## Interface Segregation
Keep interfaces small and focused (see SOLID - ISP):
- `Readable` with `read()`
- `Writable` with `write()`
- NOT a fat `ReadWriteDeleteCompressEncrypt` interface

## Interview Tip
> "Python doesn't have a dedicated `interface` keyword like Java. Use ABC for
> enforced contracts with shared behavior, Protocol for structural typing.
> In LLD interviews, use ABC - it's more explicit and familiar to interviewers."

## Files in This Folder
| File | Concept |
|------|---------|
| `protocol_example.py` | Protocol, structural subtyping |
| `abc_interface.py` | ABC as interface, enforced contracts |
| `real_world.py` | Drawable, Serializable, Comparable |
