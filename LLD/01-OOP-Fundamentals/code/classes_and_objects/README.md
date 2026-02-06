# Classes and Objects

## What Are They?
- **Class**: A blueprint/template that defines attributes (data) and methods (behavior)
- **Object**: An instance of a class — a concrete entity created from the blueprint
- Every object has its own **state** (attribute values) and **identity** (memory address)

## Memory Model
```
Class (Person)          Object (alice)          Object (bob)
┌────────────────┐     ┌──────────────┐       ┌──────────────┐
│ species = ...  │     │ name = Alice │       │ name = Bob   │
│ __init__()     │     │ age = 30     │       │ age = 17     │
│ greet()        │     └──────┬───────┘       └──────┬───────┘
└────────────────┘            │                      │
        ▲                     └──── share methods ───┘
        └─────────────── type reference ─────────────┘
```

## Key Concepts
- **Class attributes**: Shared by all instances (defined at class level)
- **Instance attributes**: Unique per object (defined in `__init__`)
- **`self`**: Reference to the current instance
- **`@classmethod`**: Alternative constructors (factory methods)

## When to Use
- Model real-world entities (User, Product, Order)
- Group related data and behavior together
- When you need multiple instances with the same interface

## Interview Tip
> "A class defines the contract, an object fulfills it. Always explain with a
> concrete example — Person, BankAccount, or whatever the problem domain is."

## Files in This Folder
| File | Concept |
|------|---------|
| `basic_class.py` | Simple class, attributes, methods |
| `constructors.py` | `__init__`, defaults, `@classmethod` factories |
| `magic_methods.py` | `__str__`, `__eq__`, `__hash__`, `__lt__`, `__len__` |
| `dataclasses_demo.py` | `@dataclass`, frozen, field defaults |
