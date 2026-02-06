# LLD Interview Cheat Sheet — The Ultimate Interview Day Reference

> The one document to review before walking into your LLD interview.

---

## The 7-Step Framework (45-Minute Interview)

| Step | What To Do                      | Time     | Deliverable                    |
|------|---------------------------------|----------|--------------------------------|
| 1    | **Clarify Requirements**        | 5 min    | List of functional requirements|
| 2    | **Identify Core Objects**       | 5 min    | List of 5-8 main classes       |
| 3    | **Define Relationships**        | 5 min    | UML class diagram              |
| 4    | **Detail Class Interfaces**     | 5 min    | Methods + attributes per class |
| 5    | **Apply Design Patterns**       | 5 min    | Pattern choices with reasoning |
| 6    | **Write Code**                  | 15 min   | Core classes implemented       |
| 7    | **Discuss & Extend**            | 5 min    | Handle follow-ups              |

---

## Step 1: Requirement Gathering Templates

### Functional Requirements Questions

```
"Before I start, let me clarify a few things..."

1. SCOPE:   "What are the core features we need to support?"
2. ACTORS:  "Who are the users of this system?"
3. ACTIONS: "What are the main actions each actor performs?"
4. RULES:   "Are there any business rules or constraints?"
5. SCALE:   "How many [items/users/requests] should we support?"
6. EDGE:    "What happens when [error scenario]?"
```

### Non-Functional Requirements to Mention

- **Concurrency:** "Should this be thread-safe?"
- **Extensibility:** "How likely is it that new [types/features] will be added?"
- **Performance:** "Any latency or throughput requirements?"

### Template Sentences

| Situation                  | Say This                                                    |
|---------------------------|-------------------------------------------------------------|
| Starting out              | "Let me understand the requirements first."                 |
| Unclear scope             | "Should I focus on [X] or include [Y] as well?"            |
| Making assumptions        | "I'll assume [X] for now — is that reasonable?"            |
| Before coding             | "Let me walk you through my design before coding."         |
| Narrowing scope           | "Given the time, I'll focus on [core features] first."     |

---

## Step 2: Class Identification Checklist

### How to Find Classes

Look for **nouns** in the requirements:

| Source                   | Classes Found                          |
|--------------------------|----------------------------------------|
| Actors / Users           | User, Admin, Driver, Customer          |
| Physical entities        | Vehicle, Room, Book, Product           |
| Concepts                 | Order, Payment, Reservation, Ticket    |
| Transactions / Events    | Transaction, Notification, Log         |
| Collections / Containers | ParkingLot, Library, Inventory, Cart   |
| Enums / Types            | VehicleType, OrderStatus, PaymentMode  |

### Class Identification Quick Questions

- [ ] Who are the actors? (Each may be a class)
- [ ] What are the main entities? (Nouns = classes)
- [ ] What are the actions? (Verbs = methods)
- [ ] Are there types/categories? (Enums or subclasses)
- [ ] Is there a central manager/coordinator? (Service or Facade)
- [ ] Are there any transactions or events? (Command or Event classes)

---

## Step 3: Relationship Identification Checklist

For every pair of core classes, ask:

| Question                                  | Relationship      | UML Symbol |
|-------------------------------------------|--------------------|------------|
| Is B a type/kind of A?                    | Inheritance        | `<\|--`    |
| Does A own B (B dies with A)?             | Composition        | `*--`      |
| Does A have a collection of B?            | Aggregation        | `o--`      |
| Does A use B to do something?             | Association        | `-->`      |
| Does A temporarily need B in a method?    | Dependency         | `..>`      |
| Does A implement the contract of B?       | Realization        | `<\|..`    |

---

## Step 4: Pattern Matching Quick Guide

### "If You See This, Use This Pattern"

| Scenario                                       | Pattern to Use             |
|------------------------------------------------|----------------------------|
| Only one instance (config, pool, cache)        | **Singleton**              |
| Create objects without specifying exact type    | **Factory Method**         |
| Families of related objects                     | **Abstract Factory**       |
| Build complex object step-by-step              | **Builder**                |
| Notify multiple objects of changes              | **Observer**               |
| Swap algorithms at runtime                      | **Strategy**               |
| Object behavior changes with state              | **State**                  |
| Undo/redo, command queuing                      | **Command**                |
| Simplify complex subsystem                      | **Facade**                 |
| Add behavior without modifying class            | **Decorator**              |
| Process request through handlers                | **Chain of Responsibility**|
| Adapt incompatible interface                    | **Adapter**                |
| Tree/hierarchy (files, menus, org chart)        | **Composite**              |

### Most Used Patterns in LLD Interviews

**Tier 1 — Almost every interview:**
- Strategy, Observer, Factory, Singleton

**Tier 2 — Frequently needed:**
- State, Command, Decorator, Facade

**Tier 3 — Specialized:**
- Builder, Adapter, Composite, Chain of Responsibility

---

## Step 5: Code Quality Checklist (10 Points)

Before submitting your code, verify:

| # | Checkpoint                                      | Status |
|---|--------------------------------------------------|--------|
| 1 | Classes follow SRP (single reason to change)     | [ ]    |
| 2 | Used interfaces/abstract classes for extensibility| [ ]    |
| 3 | No hardcoded values — use enums or constants      | [ ]    |
| 4 | Meaningful variable/method/class names             | [ ]    |
| 5 | Applied at least one design pattern with reason   | [ ]    |
| 6 | Encapsulation — private fields, public methods    | [ ]    |
| 7 | Composition over inheritance where appropriate    | [ ]    |
| 8 | Error handling for edge cases                     | [ ]    |
| 9 | Thread safety addressed (if concurrent)           | [ ]    |
| 10| Open for extension (can add new types easily)    | [ ]    |

---

## Step 6: Common Follow-Up Questions & How to Handle Them

| Follow-Up Question                              | How to Handle                               |
|-------------------------------------------------|---------------------------------------------|
| "How would you add a new [type]?"               | Show OCP — add new class, no modification   |
| "What if we need to support [X] too?"           | Show extensibility through Strategy/Factory  |
| "How would you make this thread-safe?"          | Mutex/locks on shared state, concurrent collections |
| "What about scalability?"                       | Mention sharding, caching, load balancing   |
| "Can you add undo functionality?"               | Command + Memento pattern                   |
| "What if requirements change frequently?"       | Strategy pattern, dependency injection      |
| "How would you test this?"                      | DIP for mocking, interface-based testing    |
| "What's the time/space complexity?"             | Analyze core operations                     |
| "Any trade-offs in your design?"                | Discuss flexibility vs complexity           |
| "What design patterns did you use and why?"     | Name pattern, explain the problem it solves |

---

## Step 7: "If Stuck" Recovery Strategies

### Stuck on Requirements
- Ask: "What's the simplest version of this system?"
- Start with the happy path, add complexity later
- List 3 core use cases and design for those only

### Stuck on Class Design
- Write out the user story: "As a [user], I want to [action]"
- Find nouns (classes) and verbs (methods) in the story
- Start with the most obvious class and build outward

### Stuck on Relationships
- Ask "Does A HAVE a B, or IS A a B?"
- Default to composition (safest choice)
- Draw a simple diagram, refine it as you go

### Stuck on Patterns
- Don't force a pattern — simple code is better than wrong pattern
- Ask: "What changes frequently?" (that tells you where to use Strategy/Factory)
- Ask: "What needs to be notified?" (Observer)
- Ask: "What varies independently?" (Bridge/Strategy)

### Stuck on Code
- Write pseudocode first, then convert
- Start with the data model (fields/attributes)
- Then add constructors and core methods
- Don't worry about perfection — get structure right first

### General Recovery Phrases

```
"Let me step back and think about this differently..."
"Let me start with the core use case and iterate..."
"I'll simplify this and we can extend it later..."
"Let me think about what changes most frequently here..."
```

---

## Interview Anti-Patterns (Things to AVOID)

| Anti-Pattern                        | What Interviewers Think                  |
|-------------------------------------|------------------------------------------|
| Jumping to code immediately         | "Doesn't think before coding"            |
| Not asking clarifying questions     | "Makes too many assumptions"             |
| Over-engineering (50 classes)       | "Doesn't know when to stop"             |
| Under-engineering (1 God class)     | "Doesn't know OOP"                      |
| Not explaining design decisions     | "Just memorized solutions"               |
| Ignoring edge cases                 | "Not production-ready thinking"          |
| Using patterns without explaining   | "Pattern tourist, doesn't understand why"|
| Not drawing diagrams                | "Can't communicate design visually"      |
| Being silent for too long           | "Hard to work with"                      |
| Arguing with interviewer feedback   | "Not coachable"                          |

---

## Quick Problem-to-Pattern Mapping

| LLD Problem           | Key Patterns                              |
|-----------------------|-------------------------------------------|
| Parking Lot           | Strategy, Factory, Observer, Singleton    |
| Elevator System       | State, Strategy, Observer, Command        |
| LRU Cache             | Strategy, Observer (eviction)             |
| Chess                 | Strategy, Factory, Command, Observer      |
| BookMyShow            | Observer, Strategy, Factory, Singleton    |
| Library Management    | Observer, Strategy, Factory               |
| Vending Machine       | State, Strategy, Factory                  |
| Cab Booking (Uber)    | Strategy, Observer, Factory, State        |
| Snake and Ladder      | Strategy, Factory, State                  |
| Online Shopping       | Strategy, Observer, Factory, Decorator    |
| ATM Machine           | State, Chain of Responsibility, Strategy  |
| Hotel Booking         | Strategy, Observer, Factory               |
| Tic-Tac-Toe          | Strategy, Factory                         |
| File System           | Composite, Iterator, Visitor              |
| Social Media Feed     | Observer, Strategy, Decorator, Iterator   |

---

## Time Management Tips

| If you have... | Focus on...                                          |
|----------------|------------------------------------------------------|
| 30 minutes     | Requirements (3m) + Classes (3m) + Core code (20m) + Discussion (4m) |
| 45 minutes     | Full 7-step framework as described above              |
| 60 minutes     | Add detailed UML + more code + extensibility discussion |

**Golden rules:**
- Spend 30% of time on design, 50% on code, 20% on discussion
- Never spend more than 5 minutes on requirements
- Always have something on the board within first 10 minutes
- Code the most important class first, extend outward

---

*Last updated: 2026-02-06 | Interview-ready cheat sheet*
