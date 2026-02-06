# 30 Questions Interviewers Actually Ask During LLD Interviews

> These are the real questions that come up in LLD rounds at FAANG, unicorns, and top tech companies. For each question: what they are testing, a good answer, a great answer, and red flags.

---

## Phase 1: Requirement Gathering (Questions 1-8)

### Question 1: "What are the core use cases?"

**What they're testing:** Can you identify the essential functionality vs nice-to-have? Do you think in terms of use cases or jump to implementation?

**Good answer:** "The core use cases are: [lists 3-5 key user actions]. Should I also consider admin operations?"

**Great answer:** "Let me think about the actors first. We have [primary actors] and [secondary actors]. For the primary actor, the key use cases are... For the secondary actor... Let me prioritize these by importance."

**Red flag:** Listing 15 features without prioritization. Starting with "We need a database..."

---

### Question 2: "Who are the actors in this system?"

**What they're testing:** Do you think about users and roles before diving into code?

**Good answer:** "The primary actors are customers and the system admin."

**Great answer:** "I see three types of actors: 1) End users who [action], 2) Operators/admins who [action], 3) External systems like [payment gateway, notification service]. Let me focus on the end user flow first."

**Red flag:** "There's just one user." Not thinking about admin, system, or external actors.

---

### Question 3: "Should we support X?" (testing if candidate asks or assumes)

**What they're testing:** Do you clarify or assume? This is a deliberate trap to see if you blindly say yes.

**Good answer:** "That's a good question. Let me think about whether X is in scope... I think we should include it because [reason]."

**Great answer:** "Before deciding, let me understand the impact. Supporting X would mean [additional complexity]. For a 45-minute interview, I'd suggest we design the core system first and make it extensible for X. Sound good?"

**Red flag:** "Sure, let's add it!" (without thinking about scope creep) OR "No, we don't need that" (dismissive without analysis).

---

### Question 4: "What are the scale requirements?"

**What they're testing:** Do you design for the right scale? Over-engineering is as bad as under-engineering.

**Good answer:** "How many concurrent users should we support? What's the expected throughput?"

**Great answer:** "Let me ask about scale on three dimensions: 1) Number of entities (e.g., how many parking spots), 2) Concurrent operations (e.g., entries per minute), 3) Data volume (e.g., how long do we keep history). This helps me choose the right data structures and patterns."

**Red flag:** "Let's use Kafka and Redis" for a system with 100 users. Or ignoring scale entirely.

---

### Question 5: "Are there any non-functional requirements?"

**What they're testing:** Do you think beyond functionality?

**Good answer:** "Should we consider thread safety? Any latency requirements?"

**Great answer:** "For non-functional requirements, I'd consider: 1) Concurrency - multiple users accessing simultaneously, 2) Consistency - what happens if two operations conflict, 3) Extensibility - how likely are requirement changes, 4) Observability - do we need logging or event tracking. Which of these are priorities?"

**Red flag:** Not knowing what non-functional requirements are. Saying "it should be fast" without specifics.

---

### Question 6: "What's out of scope?"

**What they're testing:** Can you set boundaries? A common mistake is trying to design everything.

**Good answer:** "I'll exclude [feature X] and [feature Y] to focus on the core problem."

**Great answer:** "Let me explicitly list what I'll design and what I won't. In scope: [list]. Out of scope but extensible: [list]. Completely out of scope: [list]. The second category means I'll design the interfaces so these can be added later without refactoring."

**Red flag:** No boundaries set. Or excluding everything interesting.

---

### Question 7: "How will users interact with this system?"

**What they're testing:** Can you think about the API/interface before internal design?

**Good answer:** "Users will call methods like `createOrder()`, `cancelOrder()`, etc."

**Great answer:** "Let me define the public API first. From the user's perspective: `system.doAction(params) -> result`. I think about the API contract before the internal classes, because the API is the promise we make to callers. Here are the key methods: [lists 5-7 methods with params and return types]."

**Red flag:** Starting with internal class design without thinking about how users interact with the system.

---

### Question 8: "What data do we need to store?"

**What they're testing:** Can you identify the essential data model?

**Good answer:** "We need to store [lists entities and their key attributes]."

**Great answer:** "The core entities and their relationships are: Entity A has-many Entity B, Entity C belongs-to Entity A. Key attributes: [for each entity]. I'm thinking about what's mutable vs immutable - [entity X] is write-once (like a ticket), while [entity Y] changes frequently (like availability)."

**Red flag:** Jumping to database schema design. Discussing SQL tables in an OOP interview.

---

## Phase 2: Design Phase (Questions 9-16)

### Question 9: "Why did you choose this class structure?"

**What they're testing:** Can you justify your design decisions?

**Good answer:** "I separated these classes because each has a distinct responsibility."

**Great answer:** "I made this choice based on three principles: 1) SRP - each class has one reason to change: [example], 2) The relationship between A and B is composition because B can't exist without A, 3) I used inheritance for [X hierarchy] because they share behavior, but composition for [Y] because it's a 'has-a' relationship."

**Red flag:** "That's just how I've always done it." No justification. Or justifying with buzzwords without understanding.

---

### Question 10: "What pattern are you using here and why?"

**What they're testing:** Do you know design patterns? Can you apply them correctly? Or are you forcing patterns?

**Good answer:** "I'm using the Strategy pattern because the algorithm needs to be swappable at runtime."

**Great answer:** "I'm using Strategy here because [specific reason]. I considered [alternative pattern] but rejected it because [reason]. The key benefit of Strategy in this context is that when we need a new scheduling algorithm, we implement one class without modifying existing code - that's OCP in action."

**Red flag:** "I'm using Singleton because it's a design pattern." Using patterns without understanding why. Forcing a pattern where it doesn't fit.

---

### Question 11: "How would you make this extensible?"

**What they're testing:** Can you design for change without over-engineering?

**Good answer:** "I'd use interfaces so new implementations can be added."

**Great answer:** "Extensibility depends on what's likely to change. Based on our requirements, I expect [X] to change frequently, so I've abstracted it behind an interface. But [Y] is stable, so I've kept it simple - adding abstraction there would be over-engineering. If [Y] needs to change later, the refactoring cost is low because it's isolated in one class."

**Red flag:** "Let me add 5 interfaces and 3 abstract factories." Over-engineering everything. Or: "We can refactor later" without any extensibility points.

---

### Question 12: "What happens if requirements change to X?"

**What they're testing:** Is your design brittle or flexible?

**Good answer:** "We'd need to modify [specific class]. The change is localized."

**Great answer:** "Great question. If X changes, let me trace the impact: Only [Class A] needs modification because the rest of the system interacts with it through the [Interface B] abstraction. The change is a 1-class modification, not a ripple across the system. Let me show you exactly what would change... [modifies code]."

**Red flag:** "We'd need to rewrite half the system." That means the design is tightly coupled.

---

### Question 13: "Why inheritance here instead of composition?"

**What they're testing:** Do you understand the trade-offs? This is a classic OOP question.

**Good answer:** "Because these classes share an IS-A relationship and common behavior."

**Great answer:** "I used inheritance because: 1) There's a genuine IS-A relationship - a Car IS-A Vehicle, 2) The subclasses share behavior through the base class (_slide method for chess pieces), 3) We need polymorphism - the caller uses the base type. If this were just about code reuse, I'd prefer composition. The rule I follow: inherit for polymorphism, compose for reuse."

**Red flag:** "I always use inheritance for shared code." That's the wrong reason to inherit.

---

### Question 14: "Can you draw the class diagram?"

**What they're testing:** Can you communicate visually? Do you know UML basics?

**Good answer:** Draws boxes with class names, arrows for inheritance, lines for association.

**Great answer:** Draws a clear diagram showing: Classes with key attributes and methods (not all), inheritance arrows, composition (filled diamond), aggregation (empty diamond), interfaces (dashed lines). Labels relationships with cardinality (1..*, 0..1). Explains the diagram while drawing.

**Red flag:** Can't draw any diagram. Draws only code, no visual representation. Or draws an ER diagram instead of a class diagram.

---

### Question 15: "How do these classes communicate?"

**What they're testing:** Do you understand object interaction, method calls, and data flow?

**Good answer:** "Object A calls method on Object B, which returns the result."

**Great answer:** "Let me trace through a use case. When a user does [action]: 1) Controller receives the request, 2) Calls Service.method(params), 3) Service creates/retrieves Domain objects, 4) Domain object A delegates to B via method call, 5) Result flows back up. I'm using the principle of Tell Don't Ask - A tells B what to do rather than asking B for data and doing it itself."

**Red flag:** All logic in one God class. Objects that get data from each other instead of delegating behavior.

---

### Question 16: "Where does validation logic live?"

**What they're testing:** Do you understand where to put business rules?

**Good answer:** "Validation is in the service layer."

**Great answer:** "There are two types of validation: 1) Input validation (is the email format valid?) - this lives at the boundary, in the controller or API layer, 2) Business rule validation (can this user make this move?) - this lives in the domain objects. For example, in chess, `Piece.get_possible_moves()` encapsulates movement validation. The Game class validates turn order. Each object validates its own invariants."

**Red flag:** All validation in one Validator class. No validation at all. Validation scattered randomly.

---

## Phase 3: Code Phase (Questions 17-22)

### Question 17: "Walk me through this method."

**What they're testing:** Can you explain code clearly? Do you understand what you wrote?

**Good answer:** Steps through the method line by line, explaining the logic.

**Great answer:** "This method does [high-level purpose]. It takes [params] and returns [result]. The algorithm works in three phases: 1) [setup], 2) [core logic], 3) [cleanup/return]. The key decision point is at line X where we check [condition] because [reason]. The time complexity is O(n) because [explanation]."

**Red flag:** Can't explain their own code. Reads the code line-by-line without higher-level explanation.

---

### Question 18: "What's the time complexity?"

**What they're testing:** Do you think about performance? Can you analyze algorithms?

**Good answer:** "This is O(n) where n is the number of items."

**Great answer:** "Let me break it down: The outer loop runs O(n) times, and for each iteration, the `find_spot` call is O(m) where m is spots per floor. So the total is O(n * m). In our case, n = number of floors (say 5) and m = spots per floor (say 100), so it's effectively O(500) per request - well within our performance requirements. If we needed better, we could maintain a sorted structure of available spots for O(log m) lookup."

**Red flag:** "It's O(1)" for a clearly linear algorithm. Not knowing Big-O notation. Over-optimizing a method called once per day.

---

### Question 19: "How do you handle concurrency?"

**What they're testing:** Do you understand thread safety? This separates L3 from L4.

**Good answer:** "I'd add locks to shared resources."

**Great answer:** "Concurrency issues arise at three points in this design: 1) [shared resource A] - I use a Lock to protect assign/remove operations, 2) [counter B] - I use atomic operations or a lock, 3) [read-heavy resource C] - I'd use a ReadWriteLock since reads are concurrent-safe. The key principle is: lock the minimum scope necessary. I avoid global locks because they become bottlenecks."

**Red flag:** "Python has the GIL so we don't need to worry about threads." Not understanding that the GIL doesn't protect application-level race conditions.

---

### Question 20: "Is this code testable?"

**What they're testing:** Do you think about testing? Is your design test-friendly?

**Good answer:** "Yes, we can unit test each class independently."

**Great answer:** "Yes, and here's why: 1) Dependencies are injected (the scheduler is passed in, not hardcoded), so we can mock them, 2) Each class has a single responsibility, so tests are focused, 3) The core logic (like move validation in chess) has no side effects, making it pure-function testable. For example, I'd test the Pawn's `get_possible_moves()` by setting up a Board with specific pieces and asserting the moves list."

**Red flag:** "We'd need to set up the entire system to test one class." That's a design smell.

---

### Question 21: "Why are you using enums here?"

**What they're testing:** Do you understand when to use enums vs classes?

**Good answer:** "Enums represent a fixed set of values that won't change."

**Great answer:** "I use enums for values that are: 1) Fixed at compile time (VehicleType won't get new values often), 2) Used for comparison, not behavior, 3) Don't need polymorphism. If the values needed different behavior, I'd use the class hierarchy instead. For example, VehicleType is an enum because it's just a label, but ParkingSpot is a class hierarchy because different spot types have different `can_fit` behavior."

**Red flag:** Using strings instead of enums for fixed values. Or using enums with switch statements instead of polymorphism.

---

### Question 22: "Can you handle error cases?"

**What they're testing:** Do you think about what can go wrong?

**Good answer:** "I return None or raise an exception when something fails."

**Great answer:** "I use different error handling strategies for different cases: 1) Expected failures (parking lot full) - return None/empty Optional, the caller handles it, 2) Programming errors (null piece on occupied square) - raise ValueError, these are bugs, 3) External failures (payment processor down) - use a result type or specific exception with retry logic. I never use exceptions for control flow."

**Red flag:** No error handling. Catching generic Exception everywhere. Using exceptions for normal control flow.

---

## Phase 4: Edge Cases (Questions 23-26)

### Question 23: "What happens when [resource] is full?"

**What they're testing:** Do you handle boundary conditions?

**Good answer:** "Return an error/None indicating the resource is unavailable."

**Great answer:** "When the resource is full: 1) Immediately - return appropriate status to the caller, 2) Display - update the status board (Observer pattern notifies the display), 3) Future requests - queue them with priority or reject with a clear message, 4) Monitoring - emit a metric so we can track how often this happens and add capacity."

**Red flag:** Not handling it at all. Crashing with an IndexError.

---

### Question 24: "What if two requests conflict?"

**What they're testing:** Do you understand race conditions?

**Good answer:** "I use a lock to serialize conflicting operations."

**Great answer:** "The conflict scenario is: Thread A checks availability, Thread B checks availability, both see 'available', both try to assign. My solution: the `assign_vehicle` method is atomic - it holds a lock, checks availability inside the lock, and assigns in one critical section. The return value tells the caller if assignment succeeded. If it failed, the caller retries with the next option. This is the check-then-act pattern done correctly."

**Red flag:** "That won't happen in practice." Yes, it will. Or: "We can use a global lock." That's too coarse.

---

### Question 25: "What if the system crashes midway?"

**What they're testing:** Do you think about durability and recovery?

**Good answer:** "We should persist state to handle crashes."

**Great answer:** "Crash recovery depends on what was in-progress: 1) Mid-transaction (payment started but not confirmed) - we need idempotent operations and a transaction log, 2) State recovery - persist critical state changes to durable storage synchronously, 3) Data integrity - use write-ahead logging: write to log before modifying in-memory state. On restart, replay the log. For our scope, at minimum, tickets should be persisted so we know which vehicles are parked."

**Red flag:** "We keep everything in memory." Not thinking about durability at all.

---

### Question 26: "What are the bottlenecks?"

**What they're testing:** Can you identify performance hotspots?

**Good answer:** "The main bottleneck is [specific shared resource]."

**Great answer:** "Let me trace the hot path: For each entry request, we iterate floors and spots to find an available spot. With 5 floors and 500 spots each, that's 2500 iterations worst case. The bottleneck is the linear scan. To optimize: 1) Maintain a priority queue of available spots per type, reducing lookup to O(log n), 2) Use floor-level counts for quick 'is floor full' checks, 3) Shard the lock by floor so different floors don't contend."

**Red flag:** "There are no bottlenecks." Every system has them. Or: premature optimization without identifying the actual bottleneck.

---

## Phase 5: Follow-ups and Scalability (Questions 27-30)

### Question 27: "How would you scale this?"

**What they're testing:** Can you evolve a design? Do you understand scaling dimensions?

**Good answer:** "We could add more instances and use a load balancer."

**Great answer:** "Scaling depends on the bottleneck: 1) Read-heavy (checking availability) - cache the availability data, use read replicas, 2) Write-heavy (entries/exits) - partition by floor or zone, each partition handles its own operations independently, 3) Compute-heavy (scheduling algorithm) - precompute and cache results, invalidate on state change. The key is: identify the bottleneck first, then scale that specific dimension."

**Red flag:** "Use microservices!" without explaining what benefit that provides. Or: "Use Redis!" for everything.

---

### Question 28: "How would you add feature X without changing existing code?"

**What they're testing:** Is your code actually open for extension?

**Good answer:** "I'd create a new class that implements the existing interface."

**Great answer:** "Since [interface/abstract class] defines the contract, I add feature X by: 1) Creating NewClassX that implements [interface], 2) Registering it with the system (if using a factory or registry), 3) Zero changes to existing classes. Let me demonstrate: [writes code for the new class]. Notice that [existing class A], [existing class B] are completely untouched."

**Red flag:** "I'd add an if-else to the existing method." That's the exact opposite of OCP.

---

### Question 29: "If you had more time, what would you improve?"

**What they're testing:** Self-awareness. Do you see the weaknesses in your own design?

**Good answer:** "I'd add better error handling and tests."

**Great answer:** "Three things: 1) [Specific technical improvement] - my `find_spot` uses linear search, I'd replace it with a heap-based structure for O(log n), 2) [Design improvement] - I'd add the Observer pattern to decouple the display board from the core logic, 3) [Operational improvement] - add event logging for every state change so we have an audit trail. The highest impact is #1 because it affects every request."

**Red flag:** "It's perfect as-is." No design is perfect in 45 minutes. Or: listing 20 improvements without prioritizing.

---

### Question 30: "How would you test this system?"

**What they're testing:** Testing mindset. Unit vs integration thinking.

**Good answer:** "I'd write unit tests for each class."

**Great answer:** "I'd test at three levels: 1) **Unit tests** - test each class in isolation. Mock dependencies. Example: test Pawn.get_possible_moves() with different board states, 2) **Integration tests** - test subsystems together. Example: create a full game, play a scholar's mate sequence, verify checkmate, 3) **Edge case tests** - stalemate, castling after king moved and moved back (still can't castle!), en passant timing. I'd use parameterized tests for piece movements - each piece type with 10+ board configurations."

**Red flag:** "We can test it manually." No testing plan. Or: "100% code coverage" as a goal without meaningful assertions.

---

## Quick Reference: What Each Phase Tests

| Phase | Duration | What They're Evaluating | Weight |
|-------|----------|-------------------------|--------|
| Requirements | 5-8 min | Analytical thinking, communication, scope management | 15% |
| Design | 8-12 min | OOP knowledge, class design, relationships | 30% |
| Code | 12-15 min | Implementation skill, patterns, code quality | 30% |
| Edge Cases | 5-8 min | Thoroughness, real-world thinking | 15% |
| Follow-ups | 5-8 min | Depth of knowledge, scalability thinking | 10% |

---

## The 5 Things That Get You Hired

1. **Think out loud** - The interviewer scores your thought process, not just the output
2. **Justify with principles** - "I chose X because of SRP/OCP/DIP" beats "I chose X"
3. **Handle concurrency** - Mention thread safety even if not asked. It shows seniority
4. **Accept feedback** - When the interviewer suggests a change, say "Good point" and adapt
5. **Know when to stop** - Don't gold-plate. Deliver core functionality and discuss extensions verbally

## The 5 Things That Get You Rejected

1. **Jumping to code** without requirements or design
2. **God classes** with 500 lines and 20 methods
3. **No abstraction** - everything is concrete, nothing is extensible
4. **Ignoring the interviewer's hints** - they're guiding you to the right answer
5. **Over-engineering** - 7 design patterns for a simple problem
