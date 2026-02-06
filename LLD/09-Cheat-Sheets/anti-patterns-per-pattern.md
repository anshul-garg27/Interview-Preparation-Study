# Anti-Patterns Per Design Pattern

> For each of the 22 GoF design patterns: when NOT to use it, common misuse, performance impact, and better alternatives. This is the guide to knowing when a pattern **hurts more than it helps**.

---

## Creational Patterns

---

### Singleton

**When NOT to Use:**
- When you need testability -- Singletons are global state and make unit testing extremely difficult
- When multiple instances might be needed later (e.g., multi-tenant systems, multi-database)
- For stateless utility functions -- use a module-level function or static method instead
- When the singleton holds mutable state accessed from multiple threads

**Common Misuse:**
- Using Singleton as a "global variable" container to avoid passing dependencies properly
- Making everything a Singleton "just in case" -- Config, Logger, DBConnection, Cache all become singletons
- Assuming Singleton means "create once" when it really means "single point of access" -- these are different concepts
- Thread-unsafe implementations that create multiple instances under race conditions

**Performance Impact:**
- Synchronization overhead in thread-safe implementations (double-checked locking, locks)
- Memory: Instance lives for entire application lifetime even if no longer needed
- Hidden coupling makes it impossible to parallelize tests (shared mutable state)

**Better Alternative:**
- **Dependency Injection:** Pass the shared instance explicitly. Same "one instance" behavior, but testable and explicit
- **Module-level instance:** In Python, a module is already a singleton. `config = Config()` at module level achieves the same thing
- **Factory with caching:** If you need lazy initialization, use a factory that caches its result

---

### Factory Method

**When NOT to Use:**
- When there is only one product type and no foreseeable need for variation
- When object construction is trivial (just `ClassName()` with no logic)
- When the "factory" just wraps a constructor call without adding any value

**Common Misuse:**
- Creating a factory for every class even when direct construction is fine
- Factory that returns only one type -- adds abstraction without flexibility
- Over-nested factories: `FactoryFactory`, `AbstractFactoryProvider` -- each layer adds complexity without benefit
- Using Factory when a simple constructor parameter would suffice

**Performance Impact:**
- Extra method call and object allocation (negligible in most cases)
- Code navigation becomes harder -- "Go to definition" leads to abstract methods instead of implementations
- More classes to maintain and understand

**Better Alternative:**
- **Direct construction** when there is only one implementation
- **Constructor with parameters** when variation is just different config values
- **Simple `if/else` in a classmethod** when you have 2-3 variants and no extension expected

---

### Abstract Factory

**When NOT to Use:**
- When you have only one family of products (use simple Factory Method instead)
- When product families are unlikely to change or grow
- In small applications where the added abstraction obscures simple logic

**Common Misuse:**
- Creating abstract factories "for flexibility" when only one concrete factory ever exists
- Confusing Abstract Factory with Factory Method -- they solve different problems
- Using it when simple dependency injection would achieve the same decoupling

**Performance Impact:**
- Double indirection: factory creation + product creation
- Explosion of interfaces/classes: N products x M families = N*M classes plus N+1 abstractions
- Harder to debug -- stack traces pass through multiple layers

**Better Alternative:**
- **Factory Method** when you have one product type with variants
- **Dependency Injection container** for managing object creation in larger systems
- **Configuration-based construction** with a single factory class and config parameter

---

### Builder

**When NOT to Use:**
- For objects with 1-3 required fields and no optional fields
- When all fields are required (no benefit over a constructor)
- When the object is a simple data container (use `@dataclass` or named arguments)

**Common Misuse:**
- Builder for objects that should just use keyword arguments: `User(name="Alice", age=30)` is clearer than `UserBuilder().name("Alice").age(30).build()`
- Not validating in `build()` -- Builder defers construction but should still validate completeness
- Making Builder mutable and reusable when it should be single-use (leads to stale state bugs)

**Performance Impact:**
- Extra object allocation (the builder itself) for every construction
- Method chaining creates intermediate state that must be tracked
- More code to write and maintain per class

**Better Alternative:**
- **Keyword arguments / dataclasses** for simple objects with optional fields
- **Constructor with defaults** when Python's `def __init__(self, name, age=None)` suffices
- **Named constructor classmethods** like `User.from_dict()`, `User.guest()` for specific construction patterns

---

### Prototype

**When NOT to Use:**
- When objects are cheap to construct from scratch
- When objects have complex reference graphs that make deep copy expensive or error-prone
- When objects hold non-copyable resources (file handles, database connections, network sockets)

**Common Misuse:**
- Using shallow copy when deep copy is needed (shared mutable sub-objects cause bugs)
- Cloning objects with circular references without handling the cycle
- Using Prototype instead of just calling the constructor with the same arguments

**Performance Impact:**
- Deep copy is expensive for large object graphs
- Memory spike: temporary duplication of the entire object graph
- Circular references can cause infinite recursion without proper handling

**Better Alternative:**
- **Constructor with same arguments** when construction is straightforward
- **Copy constructor / `from_existing()` classmethod** for explicit, controlled copying
- **Immutable objects** eliminate the need for copying entirely -- share the original

---

## Structural Patterns

---

### Adapter

**When NOT to Use:**
- When you control both interfaces and can just change one to match the other
- When the adaptation is so complex that the adapter becomes a translator with business logic
- When you have dozens of adapters wrapping the same library -- consider switching libraries

**Common Misuse:**
- Creating adapters for interfaces you own (just refactor the interface instead)
- Adapter that does transformation, validation, AND adaptation -- it's doing too much
- Using Adapter when Facade would be more appropriate (simplifying vs. translating)

**Performance Impact:**
- Extra method call per invocation (usually negligible)
- If adapter does data transformation, can be significant for high-throughput paths
- Object allocation overhead if creating adapters per request

**Better Alternative:**
- **Refactor the interface** when you own both sides
- **Facade** when you're simplifying a complex API rather than adapting an incompatible one
- **Duck typing** in Python -- if the interface is close enough, just use it directly

---

### Bridge

**When NOT to Use:**
- When the "two dimensions of variation" are hypothetical (YAGNI)
- When there is only one implementation and no plan for more
- When the abstraction and implementation are tightly coupled by nature

**Common Misuse:**
- Introducing Bridge prematurely when simple inheritance works fine
- Confusing Bridge with Strategy -- Bridge separates abstraction from implementation, Strategy separates algorithms
- Over-engineering: creating bridges for dimensions that never actually vary independently

**Performance Impact:**
- Double dispatch: call through abstraction, then through implementation
- More objects in memory (abstraction + implementation pairs)
- Harder to trace execution flow

**Better Alternative:**
- **Simple inheritance** when you have one dimension of variation
- **Strategy pattern** when only the algorithm varies, not the abstraction
- **Composition** with direct references when the indirection of Bridge is unnecessary

---

### Composite

**When NOT to Use:**
- When leaf and composite objects have fundamentally different interfaces
- When you need to distinguish between leaves and composites in client code
- When the tree structure is flat (only one level deep)

**Common Misuse:**
- Forcing uniform interface when leaf operations don't make sense for composites (or vice versa)
  - Example: `add_child()` on a leaf throws an exception -- breaks Liskov Substitution
- Not handling cycles in the tree structure (parent-child loops cause infinite recursion)
- Using Composite for collections that don't have tree semantics

**Performance Impact:**
- Recursive traversal can be expensive for deep trees
- Memory overhead of storing children lists in every node (even leaves)
- Operations like `calculate_total()` traverse the entire tree every time -- consider caching

**Better Alternative:**
- **Flat list** when hierarchy is only one level deep
- **Separate interfaces** for leaf and composite when they have different capabilities
- **Visitor pattern** when operations on the tree vary frequently (avoids modifying all node classes)

---

### Decorator

**When NOT to Use:**
- When you need to modify the core behavior, not add to it (use inheritance or direct modification)
- When the number of decorator combinations creates an explosion of possibilities
- When ordering of decorators matters but isn't enforced (leads to subtle bugs)

**Common Misuse:**
- Wrapper explosion: `BufferedCompressedEncryptedLoggedRetryableConnection` -- 5 layers of decorators
- Decorators that change the interface (add new methods) -- they should only enhance existing ones
- Using decorators when mixins or simple composition would be cleaner
- Not preserving the decorated object's identity (isinstance checks fail)

**Performance Impact:**
- Each decorator layer adds a method call (stack depth grows linearly with decorators)
- Memory: each decorator creates a new object wrapping the previous one
- Debugging nightmare: stack traces show 5 layers of `execute()` calls

**Better Alternative:**
- **Mixins** when you want to combine behaviors at class definition time
- **Simple function composition** for stateless transformations
- **Middleware pipeline** for ordered processing (more explicit than nesting decorators)

---

### Facade

**When NOT to Use:**
- When the subsystem is already simple and well-designed
- When clients need fine-grained control over subsystem components
- When the facade becomes a "God object" that exposes too many subsystem features

**Common Misuse:**
- Facade that just delegates every method to a single subsystem class (adds nothing)
- Facade that grows to expose the entire subsystem interface (defeats the purpose of simplification)
- Using Facade to hide bad design instead of fixing it

**Performance Impact:**
- Minimal -- usually just a pass-through with some orchestration
- Can become a bottleneck if it serializes access to subsystem components unnecessarily

**Better Alternative:**
- **Direct subsystem access** when the subsystem is already clean
- **API Gateway** for cross-cutting concerns in distributed systems
- **Refactor the subsystem** instead of hiding its complexity behind a facade

---

### Flyweight

**When NOT to Use:**
- When objects are not numerous enough to cause memory problems
- When objects have significant extrinsic state that can't be externalized
- When the identity of each object matters (flyweights are shared, so `a is b` may be true)

**Common Misuse:**
- Premature optimization: using Flyweight when memory is not actually a problem
- Not properly separating intrinsic (shared) from extrinsic (context-specific) state
- Thread-safety issues when shared flyweight objects are mutable

**Performance Impact:**
- Reduces memory usage significantly for large numbers of similar objects
- BUT adds lookup overhead (factory/cache check on every access)
- Extrinsic state management adds complexity and potential bugs

**Better Alternative:**
- **Object pooling** when objects are expensive to create but not shareable
- **Data-oriented design** (arrays of properties instead of arrays of objects) for extreme performance
- **Interning** built into the language (Python already interns small strings and integers)

---

### Proxy

**When NOT to Use:**
- When the overhead of indirection is not justified by the benefit
- When the real object is cheap to create (no need for virtual proxy)
- When access control can be handled at the API/service layer instead

**Common Misuse:**
- Proxy that just passes everything through without adding any value
- Protection proxy that can be bypassed by accessing the real object directly
- Using proxy for logging/caching when a decorator or middleware is more appropriate

**Performance Impact:**
- Extra indirection per method call (virtual dispatch, potentially network call for remote proxy)
- Remote proxies add serialization/deserialization overhead and network latency
- Virtual proxies add branch check (is real object loaded?) on every access

**Better Alternative:**
- **Decorator** for adding behavior (logging, caching) without controlling access
- **Lazy loading at the ORM level** instead of custom virtual proxies
- **API gateway** for remote access control instead of custom remote proxies

---

## Behavioral Patterns

---

### Chain of Responsibility

**When NOT to Use:**
- When requests must be handled (no handler = bug) -- Chain allows requests to fall through unhandled
- When the order of handlers matters but is implicit and fragile
- When debugging: hard to trace which handler processed a request

**Common Misuse:**
- Chains that are too long -- request passes through 10 handlers when only 1 is relevant
- No guaranteed handling: request reaches the end of the chain with no handler
- Using Chain when a simple Strategy selection would be clearer

**Performance Impact:**
- Linear traversal: O(n) handlers checked even if the first one handles it (unless short-circuited)
- Object creation overhead for handler chain setup
- Memory for maintaining the chain links

**Better Alternative:**
- **Strategy with a selector** when exactly one handler should process each request
- **Dictionary dispatch** for mapping request types to handlers directly
- **Middleware pipeline** when every handler must process the request (not just the matching one)

---

### Command

**When NOT to Use:**
- For simple operations that don't need undo, queuing, or logging
- When the command is a trivial one-liner that doesn't justify a class
- When you won't need to serialize, queue, or replay operations

**Common Misuse:**
- Creating a Command class for every trivial operation (`SaveCommand`, `LoadCommand` that just call one method)
- Command objects that hold references to receiver state, causing memory leaks
- Not implementing undo when undo is the primary reason to use Command

**Performance Impact:**
- Object allocation per operation (command object + potential memento for undo)
- Memory for command history (grows unbounded without limit)
- Serialization overhead if commands are persisted

**Better Alternative:**
- **Direct method call** for simple operations
- **Function objects / closures** in Python: `lambda: receiver.action()` instead of a Command class
- **Event sourcing** for operation replay at an architectural level

---

### Iterator

**When NOT to Use:**
- When the collection is already iterable (Python lists, dicts, sets are all iterable)
- When random access is needed (iterators are sequential)
- When the collection is small enough to just use a list

**Common Misuse:**
- Implementing custom Iterator when Python's `__iter__`/`__next__` protocol suffices
- Not implementing Iterator as a generator (verbose class-based iterators when `yield` works)
- Iterators that hold references to the collection, preventing garbage collection

**Performance Impact:**
- Generator-based iterators are lazy and memory-efficient (good)
- Class-based iterators add object allocation overhead per iteration
- External iterators can become stale if the collection is modified during iteration

**Better Alternative:**
- **Python generators (`yield`)** for custom iteration logic
- **List comprehensions** for simple transformations
- **Built-in `itertools`** for complex iteration patterns (chain, product, groupby)

---

### Mediator

**When NOT to Use:**
- When components have simple, direct relationships (2-3 components)
- When the mediator becomes a God Object that orchestrates everything

**Common Misuse:**
- Mediator that grows to contain all business logic -- it becomes the God Class it was meant to prevent
- Using Mediator between two objects (overhead without benefit -- just have them communicate directly)
- Not defining clear protocols -- mediator becomes a dumping ground for random inter-component logic

**Performance Impact:**
- All communication goes through one object -- potential bottleneck
- If mediator is synchronous, one slow component blocks all others
- Memory: mediator holds references to all colleagues

**Better Alternative:**
- **Direct communication** when there are only 2-3 components
- **Event bus / Pub-Sub** for decoupled communication without a central orchestrator
- **Message queue** for asynchronous, distributed mediation

---

### Memento

**When NOT to Use:**
- When object state is very large (full copies are expensive)
- When the language supports immutable data structures (no need to save/restore)
- When a simple "last known good" value suffices instead of full history

**Common Misuse:**
- Storing full object snapshots when only delta/diff would suffice
- Unbounded history consuming excessive memory
- Breaking encapsulation by exposing internal state through the memento

**Performance Impact:**
- Memory: O(n * s) where n is number of snapshots and s is state size
- CPU: deep copy on every save operation
- GC pressure from many short-lived memento objects

**Better Alternative:**
- **Command pattern with undo** for operation-based undo (stores operations, not state)
- **Event sourcing** for replay-based state reconstruction
- **Copy-on-write / persistent data structures** for efficient state versioning

---

### Observer

**When NOT to Use:**
- When there's only one observer (just call a method directly)
- When notification order matters (Observer doesn't guarantee order)
- When observers need to respond synchronously and their processing time varies wildly

**Common Misuse:**
- **Memory leaks:** Observers subscribe but never unsubscribe (very common in long-lived systems)
- **Event storms:** Observer A triggers event that triggers Observer B that triggers Observer A... infinite loop
- **Debugging difficulty:** When something goes wrong, tracing the chain of notifications is extremely hard
- Using Observer for request-response communication (it's fire-and-forget, not request-reply)

**Performance Impact:**
- Synchronous notification blocks the subject until all observers finish
- O(n) notification cost per event where n is number of observers
- Memory leaks from forgotten subscriptions (especially in GC languages where reference prevents collection)

**Better Alternative:**
- **Direct method call** when there's one listener
- **Pub-Sub with message broker** for decoupled, async, cross-process communication
- **Reactive streams (RxPy)** for complex event processing with backpressure
- **Weak references** for observer registration to prevent memory leaks

---

### State

**When NOT to Use:**
- When there are only 2 states (use a boolean flag)
- When state transitions are rare and simple (if/else is clearer)
- When the number of states is large and growing (state explosion)

**Common Misuse:**
- **State explosion:** 10 states x 5 events = 50 transition methods to implement
- States that share most behavior (90% identical code in each state class)
- Not validating transitions -- allowing illegal state changes silently
- Coupling state classes to the context, making them hard to reuse

**Performance Impact:**
- Object allocation for each state transition (new state object created)
- Indirect method calls through state objects (minor overhead)
- Memory for state objects (can use Flyweight to share stateless state objects)

**Better Alternative:**
- **Boolean/enum flag** for 2-3 states with simple logic
- **State machine library** for complex state machines with many transitions
- **State table (dict)** mapping `(current_state, event) -> (next_state, action)` for data-driven machines

---

### Strategy

**When NOT to Use:**
- When there's only one algorithm and no foreseeable need for variation
- When the algorithm is trivial (a few lines of code)
- When the algorithm never changes at runtime

**Common Misuse:**
- Creating Strategy for a single algorithm "for flexibility" (YAGNI)
- Strategy classes that need extensive context from the client (breaks encapsulation)
- Over-engineering: `SortStrategy`, `FilterStrategy`, `MapStrategy` for operations that are just one-liner lambdas

**Performance Impact:**
- Extra object allocation for strategy instances
- Virtual method dispatch overhead (negligible in Python)
- May prevent compiler/interpreter optimizations (inlining)

**Better Alternative:**
- **Direct implementation** when there's one algorithm
- **Function/lambda parameter** in Python: `sorted(data, key=lambda x: x.name)` is Strategy without the ceremony
- **Dictionary dispatch** mapping names to functions for runtime algorithm selection

---

### Template Method

**When NOT to Use:**
- When subclasses need to override most steps (defeats the purpose of a shared template)
- When the algorithm has no fixed structure -- steps vary too much between implementations
- When composition (Strategy) would provide more flexibility than inheritance

**Common Misuse:**
- Template with too many hook methods (subclasses must override 8/10 steps -- that's not a template)
- Deep inheritance hierarchies: Base -> Template -> ConcreteA -> SpecializedA
- Using Template Method when Strategy would avoid the inheritance coupling

**Performance Impact:**
- Minimal -- just virtual method dispatch for the hook methods
- Inheritance hierarchy can be costly in terms of code complexity (not runtime)

**Better Alternative:**
- **Strategy pattern** when you want to swap entire algorithms via composition
- **Higher-order functions** passing step functions as parameters
- **Hooks/callbacks** for one or two customization points without requiring subclassing

---

### Visitor

**When NOT to Use:**
- When the element hierarchy changes frequently (adding a new element type requires changing ALL visitors)
- When the element interface is unstable
- When there are only 1-2 operations on the hierarchy (just put the methods on the elements)

**Common Misuse:**
- Using Visitor on a hierarchy that changes often -- every new element type requires updating every visitor
- Visitor that accesses element internals through getters (breaks encapsulation)
- Overusing double dispatch in languages that support multiple dispatch natively

**Performance Impact:**
- Double dispatch: two virtual method calls per visit (accept + visit)
- Object allocation for visitor instances
- Cache unfriendly: traversal jumps between visitor and element objects

**Better Alternative:**
- **Methods on elements** when there are only a few operations
- **Pattern matching** (Python `match/case`) for simple type-based dispatch
- **Interpreter pattern** for expression evaluation specifically

---

### Interpreter

**When NOT to Use:**
- When the grammar is complex (use a parser generator like ANTLR instead)
- When performance matters (tree-walking interpreters are slow)
- When the language/DSL is unlikely to evolve

**Common Misuse:**
- Implementing a full language parser from scratch when libraries exist
- Interpreter for grammars that should be parsed with proper tools
- Not defining a proper grammar -- the interpreter grows organically and becomes unmaintainable

**Performance Impact:**
- Tree-walking interpretation is orders of magnitude slower than compiled/bytecode execution
- Deep recursion for complex expressions
- Object allocation for every node in the expression tree

**Better Alternative:**
- **Parser generators (ANTLR, PLY)** for non-trivial grammars
- **Compiled DSL** that generates code instead of interpreting it
- **Rule engine** for business rule evaluation
- **Regular expressions** for simple pattern matching (no need for a full interpreter)

---

## Quick Reference Table

| Pattern | Primary Anti-Pattern | Key Risk |
|---|---|---|
| Singleton | Global state / untestable | Testing difficulty |
| Factory Method | Over-abstraction | Unnecessary complexity |
| Abstract Factory | Premature generalization | Class explosion |
| Builder | Ceremony for simple objects | Boilerplate |
| Prototype | Shallow copy bugs | Shared mutable state |
| Adapter | Adapting things you own | Just refactor instead |
| Bridge | Hypothetical dimensions | YAGNI |
| Composite | Forced uniform interface | LSP violations |
| Decorator | Wrapper explosion | Debug difficulty |
| Facade | Hiding bad design | God Object facade |
| Flyweight | Premature memory optimization | Complexity without need |
| Proxy | Pass-through proxy | Unnecessary indirection |
| Chain of Resp. | Unhandled requests | Silent failures |
| Command | Command for trivial ops | Boilerplate |
| Iterator | Custom when built-in works | Reinventing the wheel |
| Mediator | God Mediator | Central bottleneck |
| Memento | Unbounded history | Memory explosion |
| Observer | Memory leaks + event storms | Hard to debug |
| State | State explosion | Maintenance nightmare |
| Strategy | Strategy for one algorithm | Over-engineering |
| Template Method | Too many hooks | Fragile inheritance |
| Visitor | Unstable element hierarchy | Modification ripple |
| Interpreter | Complex grammar by hand | Performance + maintenance |

---

## The Golden Rule

> **Use a pattern when the cost of NOT using it exceeds the cost of using it.**

Before applying any pattern, ask:
1. What specific problem does this solve right now?
2. Is there a simpler solution?
3. Will the next developer understand why this pattern is here?

If you can't answer all three clearly, you probably don't need the pattern yet.
