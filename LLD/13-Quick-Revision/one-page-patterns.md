# One-Page Design Patterns Revision

> All 23 GoF patterns — name, intent, one-line code idea, when to use.

---

## Creational Patterns (5) — Object Creation

| # | Pattern           | Intent                                    | Core Idea (Python)                         | When to Use                    |
|---|-------------------|-------------------------------------------|--------------------------------------------|--------------------------------|
| 1 | **Factory Method**| Let subclasses decide which class to create| `factory.create("type") -> Product`        | Unknown types at compile time  |
| 2 | **Abstract Factory**| Create families of related objects       | `UIFactory.create_button(); .create_menu()`| Cross-platform, theme systems  |
| 3 | **Builder**       | Build complex object step-by-step         | `Builder().set_a().set_b().build()`        | Many constructor params        |
| 4 | **Prototype**     | Clone existing objects instead of creating | `copy.deepcopy(template)`                  | Expensive creation, many copies|
| 5 | **Singleton**     | Only one instance, global access          | `cls._instance or cls()`                   | Config, DB pool, Logger        |

### Creational Quick Code

```python
# Factory
class Factory:
    def create(self, type): return {"a": A, "b": B}[type]()

# Builder
query = QueryBuilder().table("users").where("age>18").build()

# Singleton
class DB:
    _inst = None
    def __new__(cls): cls._inst = cls._inst or super().__new__(cls); return cls._inst
```

---

## Structural Patterns (7) — Object Composition

| # | Pattern       | Intent                                | Core Idea                                    | When to Use                    |
|---|---------------|---------------------------------------|----------------------------------------------|--------------------------------|
| 6 | **Adapter**   | Convert incompatible interface        | `Adapter wraps Adaptee, exposes Target API`  | Legacy integration             |
| 7 | **Bridge**    | Separate abstraction from implementation| `Shape(renderer) — renderer varies`        | Two dimensions of variation    |
| 8 | **Composite** | Tree structure, uniform treatment     | `Folder.get_size() sums children.get_size()`| Files, menus, org charts       |
| 9 | **Decorator** | Add behavior dynamically              | `Milk(Sugar(Coffee())).cost()`              | Wrapping, middleware           |
| 10| **Facade**    | Simplify complex subsystem            | `OrderFacade.place_order()` calls 5 services| Complex subsystem              |
| 11| **Flyweight** | Share objects to save memory          | `cache.get(key) or create_and_cache()`      | Millions of similar objects    |
| 12| **Proxy**     | Control access to object              | `Proxy checks auth, then delegates to Real` | Lazy load, cache, security     |

### Structural Quick Code

```python
# Adapter
class Adapter:
    def __init__(self, adaptee): self.a = adaptee
    def request(self): return self.a.specific_request()

# Decorator
class Logged:
    def __init__(self, wrapped): self.w = wrapped
    def do(self): print("log"); return self.w.do()

# Composite
class Folder:
    def size(self): return sum(c.size() for c in self.children)
```

---

## Behavioral Patterns (11) — Object Communication

| #  | Pattern              | Intent                                 | Core Idea                                     | When to Use                   |
|----|----------------------|----------------------------------------|-----------------------------------------------|-------------------------------|
| 13 | **Chain of Resp.**   | Pass request along handler chain      | `h1.next = h2; h1.handle(req)`               | Middleware, approval chains   |
| 14 | **Command**          | Encapsulate request as object         | `cmd.execute(); cmd.undo()`                   | Undo/redo, task queues        |
| 15 | **Interpreter**      | Evaluate grammar/expressions          | `Add(Num(3), Num(5)).interpret()`             | Parsers, rule engines         |
| 16 | **Iterator**         | Traverse collection without exposing  | `for item in collection: ...`                 | Custom traversal              |
| 17 | **Mediator**         | Centralize complex communications     | `chatroom.send(msg, sender, receiver)`        | Chat rooms, UI coordination   |
| 18 | **Memento**          | Capture/restore object state          | `snapshot = obj.save(); obj.restore(snapshot)`| Save/load, undo               |
| 19 | **Observer**         | Notify dependents of state change     | `subject.notify() -> observer.update()`       | Events, pub/sub               |
| 20 | **State**            | Behavior changes with internal state  | `machine.state = NextState()`                 | Vending machines, workflows   |
| 21 | **Strategy**         | Swap algorithms at runtime            | `context.strategy = NewAlgo()`                | Payment, sorting, pricing     |
| 22 | **Template Method**  | Skeleton in base, steps in subclass   | `base.process() calls self.step1(), step2()` | ETL pipelines, tests          |
| 23 | **Visitor**          | Add operations without changing class | `element.accept(visitor)`                     | Compilers, exporters          |

### Behavioral Quick Code

```python
# Strategy
class Sorter:
    def __init__(self, strategy): self.s = strategy
    def sort(self, data): return self.s.sort(data)

# Observer
class EventBus:
    def on(self, event, cb): self.listeners[event].append(cb)
    def emit(self, event, data): [cb(data) for cb in self.listeners[event]]

# State
class Vending:
    def insert_coin(self): self.state.insert_coin(self)  # Delegates to state
```

---

## Pattern Selection Cheat Sheet

```
Need ONE instance?             → Singleton
Need to CREATE objects?        → Factory / Abstract Factory / Builder
Need to COPY objects?          → Prototype
Need to ADAPT interface?       → Adapter
Need to ADD behavior?          → Decorator
Need to SIMPLIFY subsystem?    → Facade
Need to CONTROL access?        → Proxy
Need to handle TREE structure? → Composite
Need to SWAP algorithms?       → Strategy
Need to change BEHAVIOR by STATE? → State
Need to NOTIFY on changes?     → Observer
Need UNDO/REDO?                → Command + Memento
Need to CHAIN handlers?        → Chain of Responsibility
Need to TRAVERSE collection?   → Iterator
Need to COORDINATE objects?    → Mediator
Need to ADD operations to tree?→ Visitor
Need SKELETON algorithm?       → Template Method
```

---

## Top 10 Most Used in Interviews

1. **Strategy** — Algorithm swapping
2. **Observer** — Event notification
3. **Factory Method** — Object creation
4. **Singleton** — Single instance
5. **State** — State machines
6. **Command** — Undo/queuing
7. **Decorator** — Dynamic behavior
8. **Facade** — Simplification
9. **Builder** — Complex construction
10. **Composite** — Tree structures

---

*One-page revision | 2026-02-06*
