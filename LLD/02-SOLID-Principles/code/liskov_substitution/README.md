# Liskov Substitution Principle (LSP)

> "Subtypes must be substitutable for their base types without altering
> the correctness of the program."

## The Idea
If `B` extends `A`, any code using `A` should work correctly when given
a `B` instead. No exceptions, no surprises, no broken contracts.

## Real-World Analogy
**Replacement employee.** If you hire a replacement for a role, they must
be able to do everything the original could. A "driver" replacement who
can't drive breaks the contract.

## How to Spot Violations
- Subclass **raises exceptions** for inherited methods (`NotImplementedError`)
- Subclass **changes behavior** in unexpected ways (Square's setter)
- `isinstance` checks to handle subtypes differently
- Subclass methods return different types than parent

## Classic Examples
| Violation | Problem | Fix |
|-----------|---------|-----|
| Square extends Rectangle | Setter side effects | Both extend Shape |
| Penguin extends Bird.fly() | Raises exception | Separate FlyingBird / NonFlyingBird |
| ReadOnlyList extends List | push() throws error | Separate interfaces |

## LSP Rules
1. **Preconditions** cannot be strengthened in subtype
2. **Postconditions** cannot be weakened in subtype
3. **Invariants** of base type must be preserved

## Interview Tip
> "LSP is about behavioral compatibility. A Square IS-A Rectangle in math,
> but NOT in code if Rectangle has mutable width/height. Fix it by making
> them siblings under a common abstraction."

## Files in This Folder
| File | Shows |
|------|-------|
| `violation.py` | Rectangle/Square broken area calculation |
| `fixed.py` | Both as siblings under Shape |
| `bird_example.py` | Bird/Penguin - can't-fly violation + fix |
