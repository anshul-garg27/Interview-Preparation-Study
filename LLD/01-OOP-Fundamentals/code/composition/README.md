# Composition

## What Is It?
A class contains objects of other classes as parts. The contained objects are
**owned** by the container and don't exist independently.

## HAS-A vs IS-A
```
Inheritance (IS-A):    Dog IS-A Animal
Composition (HAS-A):   Car HAS-A Engine
```

## Composition vs Aggregation
| Aspect | Composition | Aggregation |
|--------|------------|-------------|
| Ownership | Strong (part dies with whole) | Weak (part survives) |
| Lifecycle | Same as container | Independent |
| Example | Car-Engine | Department-Employee |
| UML | Filled diamond | Empty diamond |

## Why Prefer Composition Over Inheritance
1. **Flexibility** - swap behaviors at runtime
2. **No fragile base class** - changes to parent don't break children
3. **Mix and match** - combine any abilities without class explosion
4. **Testability** - inject mock parts easily

## When to Use
- When relationship is truly "has-a" (Car has Engine)
- When you need to **combine** multiple behaviors
- When behaviors might change at runtime

## Interview Tip
> "Favor composition over inheritance. Use inheritance for genuine IS-A
> relationships. Use composition to assemble behaviors. If you're
> inheriting just to reuse code, that's a code smell."

## Files in This Folder
| File | Concept |
|------|---------|
| `composition_example.py` | Car HAS-A Engine, Wheels, GPS |
| `vs_inheritance.py` | Robot abilities: inheritance vs composition |
