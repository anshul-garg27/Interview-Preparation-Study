# Inheritance

## What Is It?
A mechanism where a child class **inherits** attributes and methods from a
parent class, enabling code reuse and hierarchical relationships.

## Types of Inheritance
```
Single:       Animal -> Dog
Multilevel:   Animal -> Mammal -> Dog
Hierarchical: Shape -> Circle, Rectangle, Triangle
Multiple:     Loggable, Serializable -> User
Diamond:         A
                / \
               B   C
                \ /
                 D
```

## Diamond Problem & MRO
Python resolves the diamond problem using **C3 Linearization**:
- `super()` follows the MRO, not just the immediate parent
- Check MRO: `ClassName.__mro__` or `ClassName.mro()`
- Rule: children before parents, left before right

## When to Use Inheritance
- **IS-A** relationship (Dog IS-A Animal)
- When subclasses share significant behavior
- When you need polymorphism (treat Dog as Animal)

## When to AVOID Inheritance
- When you only need a few methods (use composition)
- When the hierarchy is deeper than 2-3 levels
- When child classes override most parent methods

## Interview Tip
> "Prefer composition over inheritance. Use inheritance for true IS-A
> relationships, but if you're just reusing code, composition is cleaner.
> Always be ready to explain MRO and the diamond problem."

## Files in This Folder
| File | Concept |
|------|---------|
| `single_inheritance.py` | Animal -> Dog, Cat |
| `multilevel_inheritance.py` | Animal -> Mammal -> Dog chain |
| `hierarchical_inheritance.py` | Shape -> Circle, Rectangle, Triangle |
| `diamond_problem.py` | Multiple inheritance, MRO, C3 linearization |
| `method_overriding.py` | Override, super() calls, extend vs replace |
