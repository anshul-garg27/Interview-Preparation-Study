# Encapsulation

## What Is It?
Bundling data (attributes) and methods that operate on that data into a single
unit (class), while **restricting direct access** to internal state.

## Python Access Levels
| Convention | Syntax | Meaning |
|-----------|--------|---------|
| Public | `self.name` | Anyone can access |
| Protected | `self._name` | "Internal use" (convention only) |
| Private | `self.__name` | Name-mangled to `_ClassName__name` |

## Key Tools
- **`@property`**: Read-only or validated access to private data
- **Setter with validation**: Enforce business rules on attribute changes
- **Private methods** (`__method`): Internal helpers hidden from outside

## Benefits
1. **Data integrity** - Invalid states are impossible (no negative balance)
2. **Flexibility** - Change internals without breaking external code
3. **Debugging** - All mutations go through controlled entry points

## When to Use
- Any class with state that has **business rules** (BankAccount, User, Order)
- When you want to **validate** before allowing changes
- When internal implementation may change but the interface should stay stable

## Interview Tip
> "Python uses conventions, not enforcement. `_protected` means 'please don't
> touch', `__private` uses name mangling but can still be bypassed. The real
> encapsulation is in using `@property` with validation."

## Files in This Folder
| File | Concept |
|------|---------|
| `private_attributes.py` | `_protected`, `__private`, `@property`, validation |
| `bank_account.py` | Real-world encapsulation with BankAccount |
