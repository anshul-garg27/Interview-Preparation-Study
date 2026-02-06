# Open/Closed Principle (OCP)

> "Software entities should be open for extension, but closed for modification."

## The Idea
Add new behavior by writing **new code** (new classes), not by changing
**existing code** that already works and is tested.

## Real-World Analogy
**Electrical outlet.** To use a new appliance, you plug it in. You don't
rewire the house. The outlet is CLOSED for modification (don't change it),
OPEN for extension (plug in anything).

## How to Spot Violations
- `if/elif/else` chains on type strings
- Adding a feature requires modifying existing methods
- Switch statements that grow over time

## How to Fix
1. Define an **abstract interface** for the varying behavior
2. Create **concrete implementations** for each variant
3. Client code uses the abstraction, not concrete types
4. New variants = new classes, zero changes to existing code

## Common Patterns That Enable OCP
- **Strategy pattern**: Swap algorithms at runtime
- **Template method**: Base class defines skeleton, subclasses fill in
- **Plugin architecture**: Register new handlers dynamically

## Interview Tip
> "OCP is about using polymorphism to avoid modification. If you see an if/elif
> chain checking types, it's an OCP violation. Replace with an abstract class
> and concrete implementations."

## Files in This Folder
| File | Shows |
|------|-------|
| `violation.py` | if/elif chain for customer discounts |
| `fixed.py` | Strategy pattern - extend by adding new class |
