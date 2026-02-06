# Java Quick Reference for LLD Interviews

> Complete Java syntax, patterns, and idioms needed for Low-Level Design interviews.

---

## 1. Java OOP Essentials for LLD

### Interface

```java
public interface Payable {
    double calculatePay();
    default String getPayStub() { return "Pay: " + calculatePay(); } // Java 8+
}

public interface Taxable {
    double calculateTax();
}
```

### Abstract Class

```java
public abstract class Employee implements Payable {
    protected String name;
    protected String id;

    public Employee(String name, String id) {
        this.name = name;
        this.id = id;
    }

    public String getName() { return name; }
    public abstract double calculatePay(); // Subclasses must implement
}
```

### Concrete Class

```java
public class FullTimeEmployee extends Employee implements Taxable {
    private double salary;

    public FullTimeEmployee(String name, String id, double salary) {
        super(name, id);
        this.salary = salary;
    }

    @Override
    public double calculatePay() { return salary / 12; }

    @Override
    public double calculateTax() { return salary * 0.3; }
}
```

### Key Rules

```
- Interface: contract only, multiple inheritance allowed
- Abstract class: partial implementation, single inheritance
- Use interface when: multiple types share behavior contract
- Use abstract class when: shared state + partial implementation needed
- extends: class inherits class
- implements: class implements interface
- Interfaces can extend other interfaces
```

---

## 2. Java Enum Best Practices for LLD

### Basic Enum

```java
public enum OrderStatus {
    CREATED, CONFIRMED, PAID, SHIPPED, DELIVERED, CANCELLED
}
```

### Enum with Fields and Methods

```java
public enum VehicleType {
    CAR(4, 10.0),
    MOTORCYCLE(2, 5.0),
    TRUCK(6, 20.0),
    BUS(6, 15.0);

    private final int wheels;
    private final double hourlyRate;

    VehicleType(int wheels, double hourlyRate) {
        this.wheels = wheels;
        this.hourlyRate = hourlyRate;
    }

    public int getWheels() { return wheels; }
    public double getHourlyRate() { return hourlyRate; }
}
```

### Enum with Abstract Method (State Pattern)

```java
public enum TrafficLight {
    RED {
        @Override public TrafficLight next() { return GREEN; }
        @Override public int getDuration() { return 60; }
    },
    GREEN {
        @Override public TrafficLight next() { return YELLOW; }
        @Override public int getDuration() { return 45; }
    },
    YELLOW {
        @Override public TrafficLight next() { return RED; }
        @Override public int getDuration() { return 5; }
    };

    public abstract TrafficLight next();
    public abstract int getDuration();
}
```

### Enum as Singleton

```java
public enum DatabaseConnection {
    INSTANCE;

    private Connection connection;

    public Connection getConnection() {
        if (connection == null) {
            connection = createConnection();
        }
        return connection;
    }
}
// Usage: DatabaseConnection.INSTANCE.getConnection();
```

---

## 3. Java Collections for LLD

### Collections Decision Table

| Need | Collection | Time Complexity | Use Case |
|------|-----------|----------------|----------|
| Ordered list | `ArrayList` | O(1) get, O(n) insert | General purpose |
| Frequent insert/delete | `LinkedList` | O(1) insert, O(n) get | Queue implementation |
| Unique elements | `HashSet` | O(1) add/contains | Dedup, membership check |
| Sorted unique | `TreeSet` | O(log n) | Sorted iteration |
| Key-Value lookup | `HashMap` | O(1) get/put | General mapping |
| Sorted keys | `TreeMap` | O(log n) | Range queries, sorted |
| Insertion order | `LinkedHashMap` | O(1) get/put | LRU cache |
| Thread-safe map | `ConcurrentHashMap` | O(1) | Concurrent access |
| Priority ordering | `PriorityQueue` | O(log n) enqueue | Scheduling, min/max |
| FIFO queue | `ArrayDeque` | O(1) | BFS, task queue |
| Thread-safe queue | `BlockingQueue` | O(1) | Producer-consumer |

### LRU Cache with LinkedHashMap

```java
public class LRUCache<K, V> extends LinkedHashMap<K, V> {
    private final int capacity;

    public LRUCache(int capacity) {
        super(capacity, 0.75f, true); // true = access-order
        this.capacity = capacity;
    }

    @Override
    protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
        return size() > capacity;
    }
}
```

### PriorityQueue for Scheduling

```java
// Min-heap by default
PriorityQueue<Request> queue = new PriorityQueue<>(
    Comparator.comparingInt(Request::getPriority)
);

// Max-heap
PriorityQueue<Request> maxQueue = new PriorityQueue<>(
    Comparator.comparingInt(Request::getPriority).reversed()
);
```

### TreeMap for Range Queries

```java
TreeMap<Integer, ParkingSpot> spots = new TreeMap<>();
// Find nearest available spot to floor 3
Map.Entry<Integer, ParkingSpot> nearest = spots.ceilingEntry(3);
// Get all spots between floor 2 and 5
SortedMap<Integer, ParkingSpot> range = spots.subMap(2, 6);
```

---

## 4. Java Design Pattern Implementations

### Singleton (Enum-Based -- Recommended)

```java
public enum Singleton {
    INSTANCE;
    private int value;
    public int getValue() { return value; }
    public void setValue(int v) { value = v; }
}
```

### Singleton (Double-Checked Locking)

```java
public class Singleton {
    private static volatile Singleton instance;
    private Singleton() {}

    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}
```

### Factory Method

```java
public interface Notification {
    void send(String message);
}

public class EmailNotification implements Notification {
    public void send(String message) { System.out.println("Email: " + message); }
}

public class SmsNotification implements Notification {
    public void send(String message) { System.out.println("SMS: " + message); }
}

public class NotificationFactory {
    public static Notification create(String type) {
        return switch (type) {
            case "EMAIL" -> new EmailNotification();
            case "SMS" -> new SmsNotification();
            default -> throw new IllegalArgumentException("Unknown: " + type);
        };
    }
}
```

### Abstract Factory

```java
public interface UIFactory {
    Button createButton();
    TextBox createTextBox();
}

public class DarkThemeFactory implements UIFactory {
    public Button createButton() { return new DarkButton(); }
    public TextBox createTextBox() { return new DarkTextBox(); }
}

public class LightThemeFactory implements UIFactory {
    public Button createButton() { return new LightButton(); }
    public TextBox createTextBox() { return new LightTextBox(); }
}
```

### Builder (Inner Static Class)

```java
public class User {
    private final String name;      // required
    private final String email;     // required
    private final int age;          // optional
    private final String phone;     // optional

    private User(Builder builder) {
        this.name = builder.name;
        this.email = builder.email;
        this.age = builder.age;
        this.phone = builder.phone;
    }

    public static class Builder {
        private final String name;
        private final String email;
        private int age;
        private String phone;

        public Builder(String name, String email) {
            this.name = name;
            this.email = email;
        }

        public Builder age(int age) { this.age = age; return this; }
        public Builder phone(String phone) { this.phone = phone; return this; }
        public User build() { return new User(this); }
    }
}
// Usage: new User.Builder("Alice", "a@b.com").age(30).build();
```

### Strategy (with Lambdas)

```java
@FunctionalInterface
public interface PricingStrategy {
    double calculatePrice(double basePrice);
}

public class PricingService {
    private PricingStrategy strategy;

    public void setStrategy(PricingStrategy strategy) {
        this.strategy = strategy;
    }

    public double getPrice(double base) {
        return strategy.calculatePrice(base);
    }
}

// Usage with lambdas
PricingService service = new PricingService();
service.setStrategy(price -> price * 0.9);         // 10% discount
service.setStrategy(price -> price * 0.8);         // 20% discount
service.setStrategy(price -> price > 100 ? price * 0.85 : price); // conditional
```

### Observer

```java
public interface Observer {
    void update(String event, Object data);
}

public class EventManager {
    private final Map<String, List<Observer>> listeners = new HashMap<>();

    public void subscribe(String event, Observer observer) {
        listeners.computeIfAbsent(event, k -> new ArrayList<>()).add(observer);
    }

    public void unsubscribe(String event, Observer observer) {
        listeners.getOrDefault(event, List.of()).remove(observer);
    }

    public void notify(String event, Object data) {
        listeners.getOrDefault(event, List.of())
                 .forEach(obs -> obs.update(event, data));
    }
}
```

### State

```java
public interface State {
    void handle(Context context);
}

public class IdleState implements State {
    public void handle(Context context) {
        System.out.println("Processing request...");
        context.setState(new ProcessingState());
    }
}

public class ProcessingState implements State {
    public void handle(Context context) {
        System.out.println("Completing...");
        context.setState(new CompletedState());
    }
}

public class Context {
    private State state = new IdleState();
    public void setState(State state) { this.state = state; }
    public void request() { state.handle(this); }
}
```

### Command

```java
public interface Command {
    void execute();
    void undo();
}

public class PlaceOrderCommand implements Command {
    private final OrderService orderService;
    private final Order order;

    public PlaceOrderCommand(OrderService service, Order order) {
        this.orderService = service;
        this.order = order;
    }

    public void execute() { orderService.placeOrder(order); }
    public void undo() { orderService.cancelOrder(order.getId()); }
}

public class CommandInvoker {
    private final Deque<Command> history = new ArrayDeque<>();
    public void execute(Command cmd) { cmd.execute(); history.push(cmd); }
    public void undo() { if (!history.isEmpty()) history.pop().undo(); }
}
```

### Decorator

```java
public interface DataSource {
    void writeData(String data);
    String readData();
}

public class FileDataSource implements DataSource {
    public void writeData(String data) { /* write to file */ }
    public String readData() { return "raw data"; }
}

public class EncryptionDecorator implements DataSource {
    private final DataSource wrapped;
    public EncryptionDecorator(DataSource source) { this.wrapped = source; }
    public void writeData(String data) { wrapped.writeData(encrypt(data)); }
    public String readData() { return decrypt(wrapped.readData()); }
    private String encrypt(String s) { return "ENC(" + s + ")"; }
    private String decrypt(String s) { return s.replace("ENC(", "").replace(")", ""); }
}

// Usage: new EncryptionDecorator(new FileDataSource())
```

### Proxy

```java
public interface Image {
    void display();
}

public class RealImage implements Image {
    private final String filename;
    public RealImage(String f) { this.filename = f; loadFromDisk(); }
    private void loadFromDisk() { System.out.println("Loading " + filename); }
    public void display() { System.out.println("Displaying " + filename); }
}

public class LazyImageProxy implements Image {
    private final String filename;
    private RealImage realImage;
    public LazyImageProxy(String f) { this.filename = f; }
    public void display() {
        if (realImage == null) realImage = new RealImage(filename);
        realImage.display();
    }
}
```

---

## 5. Java Concurrency for LLD

### synchronized Keyword

```java
public class Counter {
    private int count = 0;

    public synchronized void increment() { count++; }
    public synchronized int getCount() { return count; }

    // Or synchronized block for finer control
    public void incrementFine() {
        synchronized (this) {
            count++;
        }
    }
}
```

### ReentrantLock

```java
public class ThreadSafeAccount {
    private final ReentrantLock lock = new ReentrantLock();
    private double balance;

    public void withdraw(double amount) {
        lock.lock();
        try {
            if (balance >= amount) {
                balance -= amount;
            }
        } finally {
            lock.unlock(); // Always unlock in finally
        }
    }

    // tryLock -- non-blocking
    public boolean tryWithdraw(double amount) {
        if (lock.tryLock()) {
            try {
                if (balance >= amount) { balance -= amount; return true; }
                return false;
            } finally { lock.unlock(); }
        }
        return false;
    }
}
```

### volatile Keyword

```java
public class SharedFlag {
    private volatile boolean running = true; // Visible across threads

    public void stop() { running = false; }

    public void run() {
        while (running) { // Reads latest value from main memory
            doWork();
        }
    }
}
```

### Atomic Classes

```java
public class AtomicCounter {
    private final AtomicInteger count = new AtomicInteger(0);

    public void increment() { count.incrementAndGet(); }
    public int get() { return count.get(); }

    // Compare-and-swap
    public boolean compareAndSet(int expected, int newVal) {
        return count.compareAndSet(expected, newVal);
    }
}

// AtomicReference for thread-safe object updates
AtomicReference<State> stateRef = new AtomicReference<>(State.IDLE);
stateRef.compareAndSet(State.IDLE, State.RUNNING);
```

### ConcurrentHashMap

```java
ConcurrentHashMap<String, Integer> map = new ConcurrentHashMap<>();
map.put("key", 1);
map.computeIfAbsent("key2", k -> expensiveComputation(k));
map.merge("key", 1, Integer::sum); // Atomic increment
```

### ExecutorService / Thread Pool

```java
// Fixed thread pool
ExecutorService executor = Executors.newFixedThreadPool(4);
executor.submit(() -> processOrder(order));
executor.shutdown();

// Scheduled tasks
ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(2);
scheduler.scheduleAtFixedRate(() -> cleanup(), 0, 1, TimeUnit.HOURS);

// Custom thread pool
ThreadPoolExecutor pool = new ThreadPoolExecutor(
    2,                  // core pool size
    10,                 // max pool size
    60, TimeUnit.SECONDS, // keep-alive
    new LinkedBlockingQueue<>(100) // work queue
);
```

### CompletableFuture

```java
CompletableFuture<Order> orderFuture = CompletableFuture
    .supplyAsync(() -> orderService.createOrder(request))
    .thenApply(order -> paymentService.processPayment(order))
    .thenApply(order -> notificationService.notify(order))
    .exceptionally(ex -> handleError(ex));

// Combine multiple futures
CompletableFuture<Void> all = CompletableFuture.allOf(
    fetchUser(), fetchProducts(), fetchRecommendations()
);
```

### Concurrency Decision Table

| Need | Use | Why |
|------|-----|-----|
| Simple mutual exclusion | `synchronized` | Built-in, simple |
| Try-lock, timed lock | `ReentrantLock` | More flexible |
| Flag visible across threads | `volatile` | Light, no locking |
| Atomic counter | `AtomicInteger` | Lock-free performance |
| Thread-safe map | `ConcurrentHashMap` | Better than synchronized map |
| Background tasks | `ExecutorService` | Managed thread pool |
| Async composition | `CompletableFuture` | Chain async operations |
| Producer-consumer | `BlockingQueue` | Built-in waiting |
| Read-heavy access | `ReadWriteLock` | Multiple readers OK |
| Count-down latch | `CountDownLatch` | Wait for N events |

---

## 6. Java 8+ Features for LLD

### Lambda Expressions in Strategy Pattern

```java
// Before Java 8: Need a class for each strategy
Comparator<Order> byPrice = new Comparator<Order>() {
    public int compare(Order a, Order b) {
        return Double.compare(a.getPrice(), b.getPrice());
    }
};

// Java 8+: Lambda
Comparator<Order> byPrice = (a, b) -> Double.compare(a.getPrice(), b.getPrice());
Comparator<Order> byDate = Comparator.comparing(Order::getCreatedAt);
```

### Stream API

```java
List<Order> orders = getOrders();

// Filter + Map + Collect
List<String> paidOrderIds = orders.stream()
    .filter(o -> o.getStatus() == OrderStatus.PAID)
    .map(Order::getId)
    .collect(Collectors.toList());

// Grouping
Map<OrderStatus, List<Order>> byStatus = orders.stream()
    .collect(Collectors.groupingBy(Order::getStatus));

// Sum
double totalRevenue = orders.stream()
    .filter(o -> o.getStatus() == OrderStatus.DELIVERED)
    .mapToDouble(Order::getTotal)
    .sum();

// Find
Optional<Order> first = orders.stream()
    .filter(o -> o.getTotal() > 1000)
    .findFirst();
```

### Optional for Null Safety

```java
// Instead of null checks
public Optional<User> findUserById(String id) {
    User user = userMap.get(id);
    return Optional.ofNullable(user);
}

// Usage
findUserById("123")
    .map(User::getEmail)
    .filter(email -> email.contains("@"))
    .ifPresent(email -> sendEmail(email));

// Or with default
String name = findUserById("123")
    .map(User::getName)
    .orElse("Unknown");
```

### Default Methods in Interfaces

```java
public interface Repository<T> {
    T findById(String id);
    List<T> findAll();
    T save(T entity);
    void delete(String id);

    // Default method -- shared implementation
    default boolean exists(String id) {
        return findById(id) != null;
    }

    default T findByIdOrThrow(String id) {
        T entity = findById(id);
        if (entity == null) throw new EntityNotFoundException(id);
        return entity;
    }
}
```

### Method References

```java
// Types of method references
list.forEach(System.out::println);             // Static
list.stream().map(String::toUpperCase);         // Instance method on element
list.stream().map(converter::convert);          // Instance method on object
list.stream().map(Order::new);                  // Constructor
```

---

## 7. Java Exception Handling for LLD

### Exception Hierarchy

```
Throwable
  ├── Error (do not catch: OutOfMemoryError, StackOverflowError)
  └── Exception
        ├── Checked (must handle: IOException, SQLException)
        └── RuntimeException / Unchecked
              ├── NullPointerException
              ├── IllegalArgumentException
              ├── IllegalStateException
              └── UnsupportedOperationException
```

### Custom Exception Hierarchy for LLD

```java
// Base exception
public class DomainException extends RuntimeException {
    private final String errorCode;
    public DomainException(String message, String errorCode) {
        super(message);
        this.errorCode = errorCode;
    }
    public String getErrorCode() { return errorCode; }
}

// Specific exceptions
public class EntityNotFoundException extends DomainException {
    public EntityNotFoundException(String entity, String id) {
        super(entity + " not found: " + id, "NOT_FOUND");
    }
}

public class InsufficientBalanceException extends DomainException {
    public InsufficientBalanceException(double required, double available) {
        super("Need " + required + " but have " + available, "INSUFFICIENT_BALANCE");
    }
}

public class InvalidStateException extends DomainException {
    public InvalidStateException(String current, String attempted) {
        super("Cannot transition from " + current + " to " + attempted, "INVALID_STATE");
    }
}
```

### When to Throw vs Handle

```
THROW when:
- Caller can recover or needs to know about the error
- Precondition violation (invalid arguments)
- Business rule violation
- Entity not found

HANDLE when:
- You can provide a reasonable default
- Retry logic makes sense
- Logging is sufficient
- At system boundaries (controller layer)
```

```java
// Service layer: throw domain exceptions
public class OrderService {
    public Order getOrder(String id) {
        return orderRepository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Order", id));
    }

    public void cancelOrder(String id) {
        Order order = getOrder(id);
        if (order.getStatus() == OrderStatus.DELIVERED) {
            throw new InvalidStateException("DELIVERED", "CANCELLED");
        }
        order.setStatus(OrderStatus.CANCELLED);
    }
}

// Controller layer: handle and return error response
public class OrderController {
    public Response getOrder(String id) {
        try {
            return Response.ok(orderService.getOrder(id));
        } catch (EntityNotFoundException e) {
            return Response.notFound(e.getMessage());
        } catch (DomainException e) {
            return Response.badRequest(e.getMessage());
        }
    }
}
```

---

## 8. Common Java Interview Code Snippets

### Thread-Safe Singleton (All Variants)

```java
// 1. Enum (BEST -- simple, serialization-safe)
public enum AppConfig {
    INSTANCE;
    private Properties config = new Properties();
    public String get(String key) { return config.getProperty(key); }
}

// 2. Double-Checked Locking
public class AppConfig {
    private static volatile AppConfig instance;
    private AppConfig() {}
    public static AppConfig getInstance() {
        if (instance == null) {
            synchronized (AppConfig.class) {
                if (instance == null) instance = new AppConfig();
            }
        }
        return instance;
    }
}

// 3. Bill Pugh (Inner Static Class)
public class AppConfig {
    private AppConfig() {}
    private static class Holder {
        private static final AppConfig INSTANCE = new AppConfig();
    }
    public static AppConfig getInstance() { return Holder.INSTANCE; }
}
```

### LRU Cache (Full Implementation)

```java
public class LRUCache<K, V> {
    private final int capacity;
    private final Map<K, Node<K, V>> map;
    private final Node<K, V> head, tail;

    public LRUCache(int capacity) {
        this.capacity = capacity;
        this.map = new HashMap<>();
        head = new Node<>(null, null);
        tail = new Node<>(null, null);
        head.next = tail;
        tail.prev = head;
    }

    public V get(K key) {
        if (!map.containsKey(key)) return null;
        Node<K, V> node = map.get(key);
        moveToHead(node);
        return node.value;
    }

    public void put(K key, V value) {
        if (map.containsKey(key)) {
            Node<K, V> node = map.get(key);
            node.value = value;
            moveToHead(node);
        } else {
            Node<K, V> node = new Node<>(key, value);
            map.put(key, node);
            addToHead(node);
            if (map.size() > capacity) {
                Node<K, V> lru = tail.prev;
                remove(lru);
                map.remove(lru.key);
            }
        }
    }

    private void addToHead(Node<K, V> node) {
        node.next = head.next;
        node.prev = head;
        head.next.prev = node;
        head.next = node;
    }

    private void remove(Node<K, V> node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void moveToHead(Node<K, V> node) {
        remove(node);
        addToHead(node);
    }

    private static class Node<K, V> {
        K key; V value;
        Node<K, V> prev, next;
        Node(K key, V value) { this.key = key; this.value = value; }
    }
}
```

### Observer with Java Interfaces

```java
public interface EventListener<T> {
    void onEvent(T event);
}

public class EventBus {
    private final Map<Class<?>, List<EventListener<?>>> listeners = new ConcurrentHashMap<>();

    public <T> void subscribe(Class<T> eventType, EventListener<T> listener) {
        listeners.computeIfAbsent(eventType, k -> new CopyOnWriteArrayList<>()).add(listener);
    }

    @SuppressWarnings("unchecked")
    public <T> void publish(T event) {
        List<EventListener<?>> list = listeners.getOrDefault(event.getClass(), List.of());
        for (EventListener<?> listener : list) {
            ((EventListener<T>) listener).onEvent(event);
        }
    }
}

// Usage
EventBus bus = new EventBus();
bus.subscribe(OrderCreatedEvent.class, event -> sendEmail(event));
bus.publish(new OrderCreatedEvent(order));
```

### Builder Pattern (Canonical Form)

```java
public class Pizza {
    private final int size;
    private final boolean cheese;
    private final boolean pepperoni;
    private final boolean mushrooms;

    private Pizza(Builder b) {
        size = b.size; cheese = b.cheese;
        pepperoni = b.pepperoni; mushrooms = b.mushrooms;
    }

    public static class Builder {
        private final int size;              // required
        private boolean cheese = false;      // optional defaults
        private boolean pepperoni = false;
        private boolean mushrooms = false;

        public Builder(int size) { this.size = size; }
        public Builder cheese() { cheese = true; return this; }
        public Builder pepperoni() { pepperoni = true; return this; }
        public Builder mushrooms() { mushrooms = true; return this; }
        public Pizza build() { return new Pizza(this); }
    }
}
// new Pizza.Builder(12).cheese().pepperoni().build();
```

### Producer-Consumer with BlockingQueue

```java
public class TaskProcessor {
    private final BlockingQueue<Task> queue = new LinkedBlockingQueue<>(100);
    private final ExecutorService workers = Executors.newFixedThreadPool(4);

    public void submitTask(Task task) throws InterruptedException {
        queue.put(task); // Blocks if queue is full
    }

    public void startWorkers() {
        for (int i = 0; i < 4; i++) {
            workers.submit(() -> {
                while (!Thread.currentThread().isInterrupted()) {
                    try {
                        Task task = queue.take(); // Blocks if queue is empty
                        task.process();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                }
            });
        }
    }
}
```

---

## 9. Java Records (Java 14+)

```java
// Immutable data carrier -- ideal for DTOs and Value Objects
public record Point(int x, int y) {}

public record OrderDTO(
    String orderId,
    String customerName,
    List<String> items,
    double total
) {
    // Compact constructor for validation
    public OrderDTO {
        if (total < 0) throw new IllegalArgumentException("Total cannot be negative");
        items = List.copyOf(items); // Defensive copy
    }
}

// Usage
OrderDTO dto = new OrderDTO("O1", "Alice", List.of("Pizza"), 25.0);
String name = dto.customerName(); // Auto-generated accessor
```

---

## 10. Common Java Idioms for LLD

### Immutable Class

```java
public final class Money {
    private final double amount;
    private final String currency;

    public Money(double amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    public Money add(Money other) {
        if (!this.currency.equals(other.currency))
            throw new IllegalArgumentException("Currency mismatch");
        return new Money(this.amount + other.amount, this.currency);
    }

    public double getAmount() { return amount; }
    public String getCurrency() { return currency; }
}
```

### Fluent Interface

```java
public class QueryBuilder {
    private String table;
    private String where;
    private String orderBy;
    private int limit;

    public QueryBuilder from(String table) { this.table = table; return this; }
    public QueryBuilder where(String cond) { this.where = cond; return this; }
    public QueryBuilder orderBy(String col) { this.orderBy = col; return this; }
    public QueryBuilder limit(int n) { this.limit = n; return this; }

    public String build() {
        return "SELECT * FROM " + table
            + (where != null ? " WHERE " + where : "")
            + (orderBy != null ? " ORDER BY " + orderBy : "")
            + (limit > 0 ? " LIMIT " + limit : "");
    }
}
// new QueryBuilder().from("orders").where("status='PAID'").limit(10).build();
```

### Comparable and Comparator

```java
// Comparable: natural ordering
public class Order implements Comparable<Order> {
    @Override
    public int compareTo(Order other) {
        return this.createdAt.compareTo(other.createdAt);
    }
}

// Comparator: custom ordering
Comparator<Order> byTotal = Comparator.comparingDouble(Order::getTotal);
Comparator<Order> byTotalDesc = byTotal.reversed();
Comparator<Order> byStatusThenTotal = Comparator
    .comparing(Order::getStatus)
    .thenComparingDouble(Order::getTotal);

Collections.sort(orders, byStatusThenTotal);
```

---

*Use this cheatsheet alongside the [one-page-java.md](../13-Quick-Revision/one-page-java.md) for quick interview day revision.*
