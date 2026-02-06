# LLD Interview Scoring Rubric

> How LLD interviews are actually scored at top tech companies. This rubric is based on real evaluation criteria used at FAANG, top startups, and tier-1 tech companies.

---

## Overview

Most companies use a 1-5 scale across multiple dimensions. The final decision is not a simple average - certain criteria are weighted more heavily, and a score of 1 in any critical area is usually an automatic "No Hire."

---

## Evaluation Criteria

### 1. Requirements Gathering (Weight: 15%)

| Score | Description | Example Behavior |
|-------|------------|-----------------|
| **1 - Poor** | Starts coding immediately. Makes incorrect assumptions. | "I'll just build a parking lot with cars." No questions asked. |
| **2 - Below Average** | Asks 1-2 generic questions, misses important constraints. | "How many cars?" but misses vehicle types, payment, concurrency. |
| **3 - Average** | Asks reasonable questions, covers main requirements. | Asks about entities, basic constraints, and scope. Lists requirements. |
| **4 - Good** | Asks targeted questions, identifies edge cases early, defines scope clearly. | Asks about concurrency, failure modes, non-functional requirements. Summarizes and confirms. |
| **5 - Excellent** | Systematically covers actors, use cases, constraints, non-functional requirements. Explicitly states what's in/out of scope. Prioritizes requirements. | "Let me identify the actors first... Here are the use cases for each... These are out of scope but I'll design for extensibility... Here are the non-functional requirements I'm considering..." |

**Critical distinction:**
- Score 3: Lists requirements
- Score 4: Structures requirements (actors, use cases, constraints)
- Score 5: Prioritizes and negotiates scope with the interviewer

---

### 2. Object Identification (Weight: 20%)

| Score | Description | Example Behavior |
|-------|------------|-----------------|
| **1 - Poor** | Cannot identify classes. Everything in one file. | One `ParkingLot` class with all logic, no abstraction. |
| **2 - Below Average** | Identifies some objects but misses key entities. Poor naming. | Has `Car` and `Lot` but misses `Ticket`, `Payment`, `ParkingSpot`. |
| **3 - Average** | Identifies main objects. Some naming issues. Missing supporting classes. | Has all main entities but misses `DisplayBoard`, `EntryGate`, or uses vague names like `Manager`. |
| **4 - Good** | Clean object identification. Good naming. Appropriate granularity. | All entities identified, well-named, correct abstraction level. Distinguishes entities from value objects. |
| **5 - Excellent** | Objects map perfectly to domain concepts. Uses enums, value objects, and entities appropriately. Identifies abstract base classes and interfaces. | Every class has a clear domain purpose. Abstract classes identified for hierarchies. Enums for fixed values. Composition vs inheritance is correct everywhere. |

**What separates 4 from 5:**
- Score 4 identifies the classes
- Score 5 identifies the relationships, cardinality, and whether each is an entity, value object, enum, or interface

---

### 3. Class Design and Relationships (Weight: 25%)

| Score | Description | Example Behavior |
|-------|------------|-----------------|
| **1 - Poor** | No relationships defined. Classes are isolated or have circular dependencies. | Classes call each other randomly. No clear hierarchy. |
| **2 - Below Average** | Some relationships exist but are incorrect. Inheritance where composition is needed. | `ParkingLot extends ParkingFloor` or similar nonsensical hierarchies. |
| **3 - Average** | Correct inheritance hierarchy. Basic composition. Some design issues. | Vehicle hierarchy is correct. ParkingLot has floors. But missing abstraction where needed (e.g., concrete spot types without abstract base). |
| **4 - Good** | Clean hierarchy with abstract base classes. Proper composition and aggregation. Follows SOLID principles. | Abstract `Piece` base class, proper `_slide()` reuse, composition for Board-Square, Dependency Injection for strategy. |
| **5 - Excellent** | Design handles current requirements AND is extensible. Every relationship is justified. LSP is respected. Interfaces are used for dependency boundaries. | Can add new piece types without modifying existing code. Can swap scheduling algorithms at runtime. Dependencies point inward (DIP). Each class is independently testable. |

**This is the most heavily weighted criterion because it reveals true design skill.**

**Score 3 candidate (typical):**
```python
class ParkingLot:
    def __init__(self):
        self.spots = []  # Just a flat list

    def park(self, car):
        for spot in self.spots:
            if spot.size >= car.size:
                spot.car = car
                return True
        return False
```

**Score 5 candidate (strong):**
```python
class ParkingLot:
    def __init__(self, floors: list[ParkingFloor],
                 strategy: SpotSelectionStrategy):
        self._floors = floors          # Composition
        self._strategy = strategy      # Strategy pattern, DI
        self._tickets: dict[str, Ticket] = {}

    def enter(self, vehicle: Vehicle) -> Ticket | None:
        spot = self._strategy.find_spot(vehicle, self._floors)
        if spot and spot.assign_vehicle(vehicle):  # Thread-safe
            ticket = Ticket(vehicle, spot)
            self._tickets[vehicle.license_plate] = ticket
            return ticket
        return None
```

---

### 4. Design Patterns Usage (Weight: 15%)

| Score | Description | Example Behavior |
|-------|------------|-----------------|
| **1 - Poor** | No patterns. All logic in if/else chains. | 200-line method with nested conditionals. |
| **2 - Below Average** | Mentions patterns but applies them incorrectly. | "I'll use Singleton for everything." Uses Observer when a simple callback suffices. |
| **3 - Average** | Uses 1-2 patterns correctly but misses opportunities. | Uses inheritance hierarchy (polymorphism) correctly but misses Strategy where it's clearly needed. |
| **4 - Good** | Uses 2-3 patterns correctly and can explain why. | Strategy for scheduling, Observer for display, Factory for object creation. Explains trade-offs. |
| **5 - Excellent** | Uses patterns naturally where appropriate. Can explain alternatives and why they were rejected. Never forces a pattern. | "I considered Builder for complex object creation but the constructor is simple enough. I'm using Strategy for scheduling because algorithms will change. I considered State for elevator but the state transitions are simple enough for enums." |

**The key insight:** A score of 5 is NOT about using the most patterns. It's about using the RIGHT patterns and knowing when NOT to use one.

**Patterns interviewers expect to see by problem:**

| Problem | Expected Patterns |
|---------|------------------|
| Parking Lot | Strategy, Observer, Singleton (optional), Factory |
| Elevator | Strategy, State, Observer, Command |
| Chess | Template Method, Strategy (AI), Observer (UI), Memento (undo) |
| Vending Machine | State, Strategy (payment), Chain of Responsibility |
| Cab Booking | Strategy, Observer, Command, Mediator |
| Library Management | Observer, Decorator, Factory |

---

### 5. Code Quality (Weight: 15%)

| Score | Description | Example Behavior |
|-------|------------|-----------------|
| **1 - Poor** | Code doesn't work. Syntax errors. No structure. | Functions without return types, misspelled method names, broken logic. |
| **2 - Below Average** | Code works for happy path but has bugs. Poor naming. | Works for basic case, crashes on edge cases. Variables named `x`, `temp`, `data`. |
| **3 - Average** | Correct code. Reasonable naming. Some code smells. | Works correctly. Some long methods. Some duplication. Missing error handling. |
| **4 - Good** | Clean code. Good naming. Proper encapsulation. Handles edge cases. | Methods are focused, names are descriptive, private fields with properties, error handling present. |
| **5 - Excellent** | Production-quality code. Thread-safe. Type hints. Clean interfaces. Proper error handling. Testable. | Uses `@property` for encapsulation, `threading.Lock` for safety, clear method contracts, defensive programming at boundaries. |

**Code quality checklist:**
- [ ] Meaningful variable and method names
- [ ] Methods under 20 lines
- [ ] Proper encapsulation (private fields, public interface)
- [ ] Error handling at boundaries
- [ ] Type hints / annotations
- [ ] No magic numbers
- [ ] DRY - no duplicated logic
- [ ] Thread safety where needed

---

### 6. Communication (Weight: 10%)

| Score | Description | Example Behavior |
|-------|------------|-----------------|
| **1 - Poor** | Silent coding. Can't explain decisions. Defensive when questioned. | Writes code in silence. "That's just how you do it" when asked why. |
| **2 - Below Average** | Some explanation but hard to follow. Gets flustered by questions. | Jumps between topics. Loses train of thought when interrupted. |
| **3 - Average** | Explains code after writing. Answers questions adequately. | Writes first, then walks through. Gives reasonable explanations when asked. |
| **4 - Good** | Thinks aloud while designing. Structures explanation clearly. Welcomes feedback. | "I'm considering two options... I'll go with X because..." Acknowledges interviewer's points. |
| **5 - Excellent** | Treats the interview as a collaborative design session. Draws diagrams proactively. Asks for feedback. Adapts smoothly when challenged. | "Let me sketch this out... What do you think about this approach? ... Good point about X, let me adjust..." |

---

## Sample Scorecards

### Scorecard: HIRE (Strong L4 / SDE-2)

| Criteria | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Requirements Gathering | 15% | 4 | 0.60 |
| Object Identification | 20% | 5 | 1.00 |
| Class Design | 25% | 4 | 1.00 |
| Design Patterns | 15% | 4 | 0.60 |
| Code Quality | 15% | 4 | 0.60 |
| Communication | 10% | 5 | 0.50 |
| **Total** | **100%** | | **4.30** |

**Verdict: HIRE**

**Strengths:**
- Clean class hierarchy with proper use of abstract base classes
- Strategy pattern for scheduling was well-motivated
- Identified race conditions and added thread safety proactively
- Excellent communication - thought aloud the entire time
- Handled follow-up questions about scalability well

**Areas for growth:**
- Initial design missed one entity (gate system) that was added after prompting
- Could have discussed more edge cases proactively
- Code had minor issues that were caught and fixed during review

---

### Scorecard: NO HIRE (Weak L3 / SDE-1)

| Criteria | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Requirements Gathering | 15% | 2 | 0.30 |
| Object Identification | 20% | 2 | 0.40 |
| Class Design | 25% | 2 | 0.50 |
| Design Patterns | 15% | 1 | 0.15 |
| Code Quality | 15% | 3 | 0.45 |
| Communication | 10% | 2 | 0.20 |
| **Total** | **100%** | | **2.00** |

**Verdict: NO HIRE**

**Issues:**
- Jumped to coding after only 1 question ("how many floors?")
- Only 3 classes: ParkingLot, Car, ParkingSpot. No abstraction.
- No design patterns used. All logic in ParkingLot class.
- Code technically works but has no extensibility
- When asked "what if we add motorcycles?", answer was "I'd add an if-else"
- Very quiet, didn't explain thought process

---

### Scorecard: BORDERLINE (L3 / SDE-1)

| Criteria | Weight | Score | Weighted |
|----------|--------|-------|----------|
| Requirements Gathering | 15% | 3 | 0.45 |
| Object Identification | 20% | 3 | 0.60 |
| Class Design | 25% | 3 | 0.75 |
| Design Patterns | 15% | 2 | 0.30 |
| Code Quality | 15% | 3 | 0.45 |
| Communication | 10% | 3 | 0.30 |
| **Total** | **100%** | | **2.85** |

**Verdict: LEAN NO HIRE (or HIRE for L3 at some companies)**

**Why borderline:**
- Requirements were gathered but not structured
- Classes are correct but no abstract base classes
- Inheritance used correctly but design patterns were missing
- Code works but no thread safety considered
- Communication was adequate but not proactive

---

## L3 vs L4 Differentiation

| Dimension | L3 (Junior) | L4 (Mid-Senior) |
|-----------|-------------|-----------------|
| **Requirements** | Lists requirements | Structures into actors, use cases, constraints |
| **Classes** | Identifies concrete classes | Identifies abstract hierarchies and interfaces |
| **Relationships** | Uses inheritance correctly | Uses composition, aggregation, dependency injection |
| **Patterns** | Uses polymorphism | Uses 2-3 patterns with justification |
| **Concurrency** | Does not consider | Adds locks, considers race conditions |
| **Extensibility** | "We can refactor later" | Designs extension points proactively |
| **Communication** | Explains when asked | Thinks aloud continuously |
| **Edge Cases** | Handles obvious ones (null, empty) | Handles subtle ones (race conditions, crash recovery) |
| **Follow-ups** | Struggles with changes | Adapts design smoothly |

---

## L4 vs L5 Differentiation

| Dimension | L4 (Mid-Senior) | L5 (Senior/Staff) |
|-----------|-----------------|-------------------|
| **Requirements** | Identifies functional + non-functional | Negotiates trade-offs with interviewer |
| **Classes** | Clean hierarchy | Perfect abstraction boundaries |
| **Patterns** | Uses patterns correctly | Knows when NOT to use patterns |
| **Concurrency** | Adds locks where needed | Designs lock-free structures where possible |
| **Scalability** | "Add more instances" | Identifies bottleneck, proposes specific optimization |
| **Trade-offs** | Mentions them | Quantifies them (O(n) vs O(log n), memory vs speed) |
| **Testing** | "Write unit tests" | Describes test strategy with specific test cases |
| **Production** | Not discussed | Monitoring, alerting, deployment, rollback |

---

## Decision Framework

```
Score >= 4.0               -> STRONG HIRE
Score 3.5 - 3.9            -> HIRE
Score 3.0 - 3.4            -> LEAN HIRE (depends on other rounds)
Score 2.5 - 2.9            -> LEAN NO HIRE
Score < 2.5                -> NO HIRE
Any criterion score of 1   -> NO HIRE (regardless of total)
```

**Important:** These thresholds vary by company and level. At FAANG for L5+, even 3.5 might not be enough. At startups, 3.0 could be sufficient.

---

## Tips for Interviewers

1. **Don't help too much** - Guide with questions, not answers
2. **Take detailed notes** - Score immediately after, not from memory
3. **Ask "why" more than "how"** - The reasoning matters more than the code
4. **Challenge designs, not people** - "What if X changes?" not "That's wrong"
5. **Give time to recover** - One mistake shouldn't tank the entire interview
6. **Calibrate regularly** - Shadow other interviewers and compare scores
