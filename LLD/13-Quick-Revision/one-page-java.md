# One-Page Java Reference for Interview Day

> Print this. Read it 30 minutes before your interview.

---

## OOP Syntax

```java
interface Payable { double pay(); }                     // Contract
abstract class Employee { abstract double pay(); }      // Partial impl
class FullTime extends Employee implements Payable {}    // Concrete
final class Immutable { private final int x; }           // Cannot extend
record Point(int x, int y) {}                           // Java 14+ data class
```

```
extends    = class inherits class (single)
implements = class implements interface (multiple)
abstract   = cannot instantiate, may have abstract methods
final      = class: no subclass | method: no override | field: no reassign
static     = belongs to class, not instance
```

---

## Collections Cheat Sheet

| Type | Class | Get | Add | Remove | Notes |
|------|-------|-----|-----|--------|-------|
| List | `ArrayList` | O(1) | O(1)* | O(n) | Default choice |
| List | `LinkedList` | O(n) | O(1) | O(1) | Queue/Deque use |
| Set | `HashSet` | O(1) | O(1) | O(1) | Unordered unique |
| Set | `TreeSet` | O(log n) | O(log n) | O(log n) | Sorted unique |
| Map | `HashMap` | O(1) | O(1) | O(1) | Default map |
| Map | `TreeMap` | O(log n) | O(log n) | O(log n) | Sorted keys |
| Map | `LinkedHashMap` | O(1) | O(1) | O(1) | Insertion/access order |
| Queue | `PriorityQueue` | O(1) peek | O(log n) | O(log n) | Min-heap |
| Queue | `ArrayDeque` | O(1) | O(1) | O(1) | Stack or Queue |

*amortized

**Thread-safe:** `ConcurrentHashMap`, `CopyOnWriteArrayList`, `BlockingQueue`

---

## Design Patterns in Java (One-Liners)

| Pattern | Java Core |
|---------|-----------|
| **Singleton** | `enum S { INSTANCE; }` |
| **Factory** | `static create(type)` returns interface impl |
| **Builder** | Inner `static class Builder` with fluent API |
| **Strategy** | Interface + lambda: `(price) -> price * 0.9` |
| **Observer** | `Map<Event, List<Listener>>` with `notify()` |
| **State** | Interface per state, `context.setState(new X())` |
| **Command** | `execute()` + `undo()` interface |
| **Decorator** | Wraps same interface, delegates + adds behavior |
| **Proxy** | Same interface, controls access to real object |
| **Adapter** | Converts interface A to interface B |

---

## Concurrency Quick Reference

```java
synchronized void method() {}              // Intrinsic lock
ReentrantLock lock = new ReentrantLock();   // Explicit lock (try/finally)
volatile boolean flag = true;               // Visibility guarantee
AtomicInteger count = new AtomicInteger();  // Lock-free atomic ops
ConcurrentHashMap<K,V> map = new ConcurrentHashMap<>(); // Thread-safe map
```

```java
// Thread pool
ExecutorService pool = Executors.newFixedThreadPool(4);
pool.submit(() -> doWork());

// Async chain
CompletableFuture.supplyAsync(() -> fetch())
    .thenApply(data -> process(data))
    .exceptionally(ex -> fallback());
```

| Need | Use |
|------|-----|
| Simple lock | `synchronized` |
| Try-lock / timed | `ReentrantLock` |
| Atomic counter | `AtomicInteger` |
| Shared flag | `volatile` |
| Background work | `ExecutorService` |
| Async pipeline | `CompletableFuture` |
| Producer-consumer | `BlockingQueue` |

---

## Exception Hierarchy

```
Throwable
 +- Error (OOM, StackOverflow -- do not catch)
 +- Exception
     +- Checked (IOException -- must handle)
     +- RuntimeException (unchecked)
         +- NullPointerException
         +- IllegalArgumentException
         +- IllegalStateException
```

**Custom:** `class MyException extends RuntimeException { ... }`
**Throw** at service layer, **Catch** at controller layer.

---

## Java 8+ Essentials

```java
// Lambda
list.sort((a, b) -> a.compareTo(b));
list.sort(Comparator.comparing(Order::getTotal));

// Stream
list.stream()
    .filter(x -> x.isActive())
    .map(X::getName)
    .collect(Collectors.toList());

// Optional
Optional<User> user = findById(id);
String name = user.map(User::getName).orElse("Unknown");

// Method reference
list.forEach(System.out::println);   // static
list.stream().map(String::length);   // instance
```

---

## Key Java Snippets for LLD

```java
// Enum with behavior
enum Status {
    ACTIVE { boolean canTransition() { return true; } },
    CLOSED { boolean canTransition() { return false; } };
    abstract boolean canTransition();
}

// Builder
new User.Builder("name", "email").age(30).build();

// Singleton
enum Config { INSTANCE; String get(String k) {...} }

// LRU Cache
new LinkedHashMap<>(cap, 0.75f, true) {
    protected boolean removeEldestEntry(Entry e) { return size() > cap; }
};

// Immutable class
final class Money {
    private final double amount;
    Money add(Money o) { return new Money(amount + o.amount); }
}
```

---

## Common Complexity Reference

| Operation | ArrayList | HashMap | TreeMap | PriorityQueue |
|-----------|-----------|---------|---------|---------------|
| Access/Get | O(1) | O(1) | O(log n) | O(1) peek |
| Search | O(n) | O(1) | O(log n) | O(n) |
| Insert | O(1)* | O(1)* | O(log n) | O(log n) |
| Delete | O(n) | O(1) | O(log n) | O(log n) |

*amortized

---

## Interview Checklist

```
Before writing code:
[ ] Clarify requirements
[ ] Identify entities and relationships
[ ] Choose design patterns
[ ] Define interfaces first

While coding:
[ ] Use enums for fixed types/states
[ ] Builder for complex objects
[ ] Strategy for swappable algorithms
[ ] Factory for object creation
[ ] Make services stateless
[ ] Use interface for external dependencies

After coding:
[ ] Check thread safety if asked
[ ] Discuss extensibility (Open/Closed)
[ ] Mention trade-offs
```

---

*Detailed reference: [java-lld-cheatsheet.md](../09-Cheat-Sheets/java-lld-cheatsheet.md)*
