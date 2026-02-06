# Single Responsibility Principle (SRP)

> "A class should have only one reason to change." - Robert C. Martin

## The Idea
Each class should do **one thing well**. If a class handles user data AND
sends emails AND logs activities, it has three reasons to change.

## Real-World Analogy
**Swiss army knife vs dedicated tools.** A Swiss army knife does everything
poorly. A dedicated chef's knife, screwdriver, and bottle opener each
excel at their one job.

## How to Spot Violations
- Class has methods from **different domains** (data + email + logging)
- Class name contains "And" or "Manager" (UserAndEmailManager)
- Changing one feature requires modifying unrelated code
- Class grows endlessly as features are added

## How to Fix
1. Identify distinct responsibilities
2. Extract each into its own class
3. Use a **coordinator/service** to tie them together

## Interview Tip
> "SRP doesn't mean a class should have only one method. It means one
> REASON TO CHANGE. A `UserRepository` with save/find/delete is fine -
> they all change for the same reason (data access logic changes)."

## Files in This Folder
| File | Shows |
|------|-------|
| `violation.py` | User class doing data + email + logging |
| `fixed.py` | Separate User, EmailService, Logger classes |
