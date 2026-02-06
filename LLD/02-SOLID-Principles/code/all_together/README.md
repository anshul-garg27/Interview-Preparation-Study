# All 5 SOLID Principles Together

## How They Work as a Team
SOLID principles are not independent checkboxes. They **reinforce** each other:

```
  S (Single Responsibility)
  │  Each class does one thing
  │
  O (Open/Closed) ←── Uses abstractions to extend without modifying
  │
  L (Liskov) ←──────── Subtypes honor the contract
  │
  I (Interface Segregation) ── Small interfaces, no forced methods
  │
  D (Dependency Inversion) ── High-level depends on abstractions
```

## E-Commerce Example Summary
```
OrderService (high-level policy)
    ├── PaymentProcessor (interface)
    │      ├── StripePayment
    │      └── PayPalPayment
    ├── NotificationSender (interface)
    │      ├── EmailNotifier
    │      └── SMSNotifier
    └── OrderRepository (interface)
           └── InMemoryOrderRepo
```

## Which Principle Solves What?
| Problem | Principle | Solution |
|---------|-----------|----------|
| God class doing everything | **SRP** | Split into focused classes |
| if/elif chain for types | **OCP** | Abstract class + polymorphism |
| Subtype breaks parent contract | **LSP** | Proper abstraction hierarchy |
| Class forced to implement unused methods | **ISP** | Small, focused interfaces |
| Cannot test / swap implementations | **DIP** | Depend on interfaces, inject deps |

## Interview Tip
> "In practice, these principles overlap. When you create an abstract interface
> (OCP), you naturally get DIP (depend on abstraction) and ISP (keep it small).
> Start with SRP and the rest often follow."

## Files in This Folder
| File | Shows |
|------|-------|
| `ecommerce_example.py` | Complete OrderService using all 5 principles |
