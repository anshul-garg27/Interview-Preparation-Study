# Abstraction

## What Is It?
Hiding complex implementation details and exposing only the **essential interface**.
Users of a class only need to know **what** it does, not **how**.

## Abstract Class vs Interface (Python)
| Feature | ABC (Abstract Class) | Protocol (Interface) |
|---------|---------------------|---------------------|
| Keyword | `class X(ABC)` | `class X(Protocol)` |
| Enforcement | Explicit inheritance required | Structural (duck typing) |
| Can have concrete methods | Yes | Yes (but defeats purpose) |
| Can have state | Yes | Not typical |
| Multiple inheritance | Supported | Supported |

## Key Tools in Python
- **`ABC` + `@abstractmethod`**: Forces subclasses to implement methods
- **`Protocol`**: Structural subtyping (no inheritance needed)
- **Abstract properties**: `@property` + `@abstractmethod`

## Real-World Analogy
A car's steering wheel is an abstraction. You turn it left/right without
knowing the rack-and-pinion mechanism underneath.

## When to Use
- When you have **multiple implementations** of the same concept
- When you want to **program to an interface**, not an implementation
- When client code should not depend on concrete details

## Interview Tip
> "Use ABC when you want a contract with shared behavior (template method).
> Use Protocol when you want duck-typing with type safety."

## Files in This Folder
| File | Concept |
|------|---------|
| `abstract_class.py` | ABC, `@abstractmethod`, abstract properties |
| `interface_example.py` | Protocol, structural subtyping, `@runtime_checkable` |
| `payment_processor.py` | Real-world abstract PaymentProcessor |
