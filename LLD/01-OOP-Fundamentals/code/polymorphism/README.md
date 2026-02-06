# Polymorphism

## What Is It?
"Many forms" - the ability of different objects to respond to the **same
method call** in different ways.

## Types in Python
| Type | Mechanism | Example |
|------|-----------|---------|
| Runtime (subtype) | Method overriding | `Shape.area()` -> `Circle.area()` |
| Duck typing | Structural | Any object with `.draw()` works |
| Operator | `__add__`, `__eq__`, etc. | `v1 + v2` for Vector class |

> Python does NOT have compile-time polymorphism (method overloading) like
> Java. Use default parameters or `*args` instead.

## How It Works
```python
shapes = [Circle(5), Rectangle(4, 6)]
for s in shapes:
    print(s.area())  # Each calls its OWN area() implementation
```
No `if isinstance(s, Circle)` needed! The object itself decides what to do.

## When to Use
- When you have a **common interface** with varying implementations
- To eliminate `if/elif` type-checking chains
- To make code **extensible** (add new types without changing existing code)

## Interview Tip
> "In Python, polymorphism is everywhere thanks to duck typing. You don't need
> explicit interfaces. If an object has the right methods, it works. This is
> why Python favors 'ask forgiveness not permission' (EAFP)."

## Files in This Folder
| File | Concept |
|------|---------|
| `method_overriding.py` | Shape.area() - runtime polymorphism |
| `duck_typing.py` | "If it quacks like a duck..." |
| `operator_overloading.py` | Vector with `+`, `*`, `==`, `abs()` |
