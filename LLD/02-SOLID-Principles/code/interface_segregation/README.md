# Interface Segregation Principle (ISP)

> "Clients should not be forced to depend on interfaces they do not use."

## The Idea
Many small, specific interfaces are better than one large, general interface.
A class should only implement the methods it actually needs.

## Real-World Analogy
**Restaurant menu.** A vegetarian shouldn't have to flip through pages of
meat dishes to find what they can eat. Give them a vegetarian menu instead.

## How to Spot Violations
- Classes implement methods that **raise NotImplementedError**
- Classes have methods that **return None** or do nothing
- Interface keeps **growing** as new features are added
- Some implementors only use a **fraction** of the interface

## How to Fix
1. Split fat interface into **small, cohesive** interfaces
2. Each interface represents one **role** or **capability**
3. Classes implement only the interfaces they need
4. Use **multiple inheritance** to combine interfaces

## Rule of Thumb
If you're implementing a method just to satisfy the interface, the interface
is too fat. Split it.

## Interview Tip
> "ISP prevents 'interface pollution'. In Python, use multiple small ABCs
> or Protocols. A class can inherit from several small interfaces. This
> also helps with the Single Responsibility Principle."

## Files in This Folder
| File | Shows |
|------|-------|
| `violation.py` | Fat Worker interface forcing Robot to eat/sleep |
| `fixed.py` | Separate Workable, Eatable, Sleepable interfaces |
