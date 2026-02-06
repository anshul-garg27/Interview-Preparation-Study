# Design Patterns in Popular Frameworks and Libraries

Understanding how real frameworks use design patterns helps you recognize patterns in the wild and leverage them effectively. This guide covers Python, Java/Spring, Django, and React.

---

## 1. Python Standard Library

### Iterator Pattern: `__iter__` and `__next__`

Python's entire iteration protocol is the Iterator pattern. Every `for` loop, list comprehension, and generator uses it.

**Where in the code**: Every iterable object -- `list`, `dict`, `set`, `str`, `file`, `range`.

```python
# Python's iteration protocol IS the Iterator pattern

# 1. Built-in iterables use it
for item in [1, 2, 3]:       # list.__iter__() returns list_iterator
    pass

for char in "hello":          # str.__iter__() returns str_iterator
    pass

for line in open("file.txt"): # file.__iter__() returns self (file is its own iterator)
    pass

# 2. What's happening under the hood
nums = [10, 20, 30]
iterator = iter(nums)          # Calls nums.__iter__()
print(next(iterator))          # Calls iterator.__next__() -> 10
print(next(iterator))          # -> 20
print(next(iterator))          # -> 30
# next(iterator)               # Raises StopIteration

# 3. Custom iterator
class Countdown:
    """Iterator pattern: separate iteration state from collection."""

    def __init__(self, start: int):
        self._start = start

    def __iter__(self):
        self._current = self._start
        return self

    def __next__(self):
        if self._current <= 0:
            raise StopIteration
        val = self._current
        self._current -= 1
        return val

for n in Countdown(5):
    print(n, end=" ")  # 5 4 3 2 1

# 4. Generator: Pythonic iterator (syntactic sugar)
def countdown(start):
    while start > 0:
        yield start    # yield makes this a generator = automatic iterator
        start -= 1
```

**Key insight**: Python's `for` loop is syntactic sugar for the Iterator pattern. The `yield` keyword creates generators, which are the most Pythonic way to implement iterators.

---

### Decorator Pattern: `@property`, `@staticmethod`, `@functools.lru_cache`

Python decorators are not the GoF Decorator pattern exactly, but they serve a similar purpose: wrapping behavior around existing functions/methods.

```python
import functools
import time

# 1. @property - Decorator that turns a method into a computed attribute
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property                    # Wraps getter behavior
    def area(self):
        return 3.14159 * self._radius ** 2

    @property
    def radius(self):
        return self._radius

    @radius.setter               # Wraps setter with validation
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

c = Circle(5)
print(c.area)      # 78.54 - looks like attribute, but calls method
c.radius = 10      # Calls setter with validation


# 2. @functools.lru_cache - Adds memoization layer (classic Decorator pattern!)
@functools.lru_cache(maxsize=128)
def fibonacci(n):
    """Without cache: O(2^n). With cache decorator: O(n)."""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

fibonacci(100)  # Returns instantly, caches all intermediate results
print(fibonacci.cache_info())  # Hits, misses, size stats


# 3. @functools.wraps - Preserves original function metadata when decorating
def timing_decorator(func):
    """Custom decorator: adds timing to any function."""
    @functools.wraps(func)       # Preserves func.__name__, __doc__
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timing_decorator
def slow_function():
    """Docstring preserved by @wraps."""
    time.sleep(0.1)
    return 42

slow_function()  # Prints: slow_function took 0.1003s


# 4. @staticmethod and @classmethod - Descriptor decorators
class MyClass:
    count = 0

    @staticmethod            # No self/cls, utility method
    def validate(value):
        return value > 0

    @classmethod             # Gets cls instead of self
    def create(cls):
        cls.count += 1
        return cls()


# 5. Stacking decorators = chaining wrappers (like GoF Decorator)
@timing_decorator
@functools.lru_cache(maxsize=64)
def expensive_computation(n):
    time.sleep(0.01)
    return n ** 2

# Execution order: timing_decorator(lru_cache(expensive_computation))
```

---

### Singleton Pattern: `None`, `True`, `False`

Python guarantees exactly one instance of `None`, `True`, and `False`. Modules are also singletons.

```python
# 1. None is a singleton
a = None
b = None
assert a is b  # Same object in memory
print(id(None))  # Always the same ID

# 2. True and False are singletons
assert True is True
assert (1 == 1) is True   # Same True object

# 3. Modules are singletons - imported once, cached in sys.modules
import sys
import json
import json as json2
assert json is json2  # Same module object

# sys.modules is the singleton registry
print(type(sys.modules))  # dict: module_name -> module_object

# 4. The __new__ pattern (how to make your own singleton in Python)
class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

db1 = DatabaseConnection()
db2 = DatabaseConnection()
assert db1 is db2  # Same instance
```

---

### Factory Pattern: `dict.fromkeys()`, `datetime.now()`

Python uses classmethod factories throughout the standard library instead of overloaded constructors.

```python
from datetime import datetime, date
from collections import OrderedDict
import pathlib

# 1. dict.fromkeys() - Factory method for creating dicts
keys = ["a", "b", "c"]
d = dict.fromkeys(keys, 0)        # {'a': 0, 'b': 0, 'c': 0}

# 2. datetime factory methods
now = datetime.now()               # Factory: current time
utc = datetime.utcnow()            # Factory: UTC time
from_ts = datetime.fromtimestamp(1700000000)  # Factory: from Unix timestamp
from_str = datetime.fromisoformat("2024-01-15T10:30:00")  # Factory: from string
today = date.today()               # Factory: today's date

# 3. pathlib.Path() - Factory that creates OS-specific path
p = pathlib.Path("/tmp/test")      # Returns PosixPath on Linux/Mac, WindowsPath on Windows
# This is Abstract Factory: Path() decides which concrete class to create

# 4. int() as factory
n1 = int("42")          # From string
n2 = int("2A", 16)      # From hex string
n3 = int(3.14)           # From float
n4 = int.from_bytes(b'\x00\x0A', 'big')  # From bytes -> 10

# 5. Custom factory method pattern
class Serializer:
    @classmethod
    def from_json(cls, json_str: str) -> 'Serializer':
        import json
        data = json.loads(json_str)
        instance = cls()
        instance.data = data
        return instance

    @classmethod
    def from_csv(cls, csv_str: str) -> 'Serializer':
        instance = cls()
        instance.data = csv_str.split(",")
        return instance
```

---

### Observer Pattern: `signal` Module

```python
import signal
import sys

# Unix signals are the Observer pattern at the OS level
# Your process "subscribes" to signals

def handle_sigint(signum, frame):
    print("\nGraceful shutdown...")
    sys.exit(0)

def handle_sigusr1(signum, frame):
    print("Received SIGUSR1 - reloading config")

# Register observers (signal handlers)
signal.signal(signal.SIGINT, handle_sigint)    # Ctrl+C
# signal.signal(signal.SIGUSR1, handle_sigusr1)  # Custom signal (Unix only)

# In Django, signals are a full Observer implementation:
# from django.db.models.signals import post_save
# post_save.connect(my_handler, sender=MyModel)
```

---

### Template Method Pattern: `collections.abc`

```python
from collections.abc import Sequence

# abc.Sequence defines the template (get __len__ and __getitem__)
# and provides derived methods for free: __contains__, __iter__, __reversed__, index, count

class SortedList(Sequence):
    """Only implement 2 abstract methods, get 5 methods for free."""

    def __init__(self, items):
        self._data = sorted(items)

    def __getitem__(self, index):       # Required
        return self._data[index]

    def __len__(self):                   # Required
        return len(self._data)

    # These come free from Sequence:
    # __contains__, __iter__, __reversed__, index(), count()

sl = SortedList([3, 1, 4, 1, 5])
print(4 in sl)           # __contains__ - True
print(list(reversed(sl)))  # __reversed__ - [5, 4, 3, 1, 1]
print(sl.count(1))       # count() - 2
```

---

## 2. Java / Spring Framework

### Singleton Pattern: Spring Bean Default Scope

Spring Beans are singletons by default -- one instance per application context.

```java
// Spring creates ONE instance of UserService for the entire application
@Service  // Singleton by default
public class UserService {
    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public User findById(Long id) {
        return userRepository.findById(id).orElseThrow();
    }
}

// Every class that injects UserService gets the SAME instance
@RestController
public class UserController {
    @Autowired
    private UserService userService;  // Same instance as everywhere else
}

@Service
public class OrderService {
    @Autowired
    private UserService userService;  // Same UserService instance!
}

// To change scope:
@Scope("prototype")  // New instance each time
@Scope("request")    // One per HTTP request
@Scope("session")    // One per user session
```

**Key insight**: Spring manages the singleton lifecycle for you. Unlike the GoF Singleton (private constructor), Spring singletons are regular classes -- Spring just ensures one instance.

---

### Factory Pattern: BeanFactory and FactoryBean

```java
// 1. BeanFactory - Spring's core container IS a factory
ApplicationContext ctx = new ClassPathXmlApplicationContext("beans.xml");
UserService service = ctx.getBean(UserService.class);  // Factory creates/returns beans

// 2. FactoryBean - Custom factory for complex object creation
@Component
public class HttpClientFactoryBean implements FactoryBean<HttpClient> {

    @Override
    public HttpClient getObject() {
        return HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .followRedirects(HttpClient.Redirect.NORMAL)
            .build();
    }

    @Override
    public Class<?> getObjectType() {
        return HttpClient.class;
    }

    @Override
    public boolean isSingleton() {
        return true;
    }
}

// Spring uses the factory when someone @Autowires HttpClient
@Service
public class ApiService {
    @Autowired
    private HttpClient httpClient;  // Created by FactoryBean
}
```

---

### Proxy Pattern: Spring AOP (Aspect-Oriented Programming)

Spring creates proxy objects that wrap your beans, adding cross-cutting concerns (logging, transactions, security) transparently.

```java
// 1. @Transactional uses a proxy to wrap methods in transactions
@Service
public class TransferService {

    @Transactional  // Spring creates a PROXY around this method
    public void transfer(Account from, Account to, BigDecimal amount) {
        // Proxy starts transaction BEFORE this method
        from.debit(amount);
        to.credit(amount);
        // Proxy commits transaction AFTER this method
        // If exception thrown, proxy ROLLS BACK
    }
}

// What Spring actually creates:
// TransferService$$SpringCGLIB$$0 extends TransferService (proxy)
//   - Before: open transaction
//   - Delegate to real transfer() method
//   - After: commit (or rollback on exception)


// 2. Custom AOP proxy for logging
@Aspect
@Component
public class LoggingAspect {

    @Around("@annotation(Logged)")  // Proxy wraps any @Logged method
    public Object logExecution(ProceedingJoinPoint joinPoint) throws Throwable {
        String method = joinPoint.getSignature().getName();
        System.out.println(">>> Entering " + method);

        long start = System.currentTimeMillis();
        Object result = joinPoint.proceed();  // Call the real method
        long elapsed = System.currentTimeMillis() - start;

        System.out.println("<<< Exiting " + method + " (" + elapsed + "ms)");
        return result;
    }
}

// Usage: Just add the annotation, proxy handles the rest
@Logged
public List<User> searchUsers(String query) {
    return userRepository.search(query);
}
```

---

### Template Method Pattern: JdbcTemplate

Spring's `JdbcTemplate` handles the boilerplate (get connection, create statement, handle exceptions, close resources) and lets you fill in the variable parts.

```java
// WITHOUT Template Method: tons of boilerplate every time
public List<User> findAllManual() {
    Connection conn = null;
    PreparedStatement stmt = null;
    ResultSet rs = null;
    try {
        conn = dataSource.getConnection();           // Boilerplate
        stmt = conn.prepareStatement("SELECT * FROM users");  // Your SQL
        rs = stmt.executeQuery();                     // Boilerplate
        List<User> users = new ArrayList<>();
        while (rs.next()) {                           // Your mapping
            users.add(new User(rs.getLong("id"), rs.getString("name")));
        }
        return users;
    } catch (SQLException e) {
        throw new RuntimeException(e);                // Boilerplate
    } finally {
        // Close rs, stmt, conn in reverse order       // Boilerplate
    }
}

// WITH JdbcTemplate: you only provide the variable parts
@Repository
public class UserRepository {
    private final JdbcTemplate jdbc;

    public List<User> findAll() {
        return jdbc.query(
            "SELECT * FROM users",                    // Your SQL
            (rs, rowNum) -> new User(                 // Your mapping (RowMapper)
                rs.getLong("id"),
                rs.getString("name")
            )
        );
    }

    public User findById(Long id) {
        return jdbc.queryForObject(
            "SELECT * FROM users WHERE id = ?",
            (rs, rowNum) -> new User(rs.getLong("id"), rs.getString("name")),
            id                                        // Parameter binding
        );
    }
}

// Template Method structure:
// JdbcTemplate.query() does:
//   1. Get connection from pool     (fixed)
//   2. Create PreparedStatement     (fixed)
//   3. Execute query                (fixed)
//   4. For each row: call YOUR RowMapper  (variable - you provide this)
//   5. Handle exceptions            (fixed)
//   6. Close resources              (fixed)
```

---

### Observer Pattern: ApplicationEventPublisher

```java
// 1. Define event
public class OrderPlacedEvent extends ApplicationEvent {
    private final String orderId;
    private final BigDecimal amount;

    public OrderPlacedEvent(Object source, String orderId, BigDecimal amount) {
        super(source);
        this.orderId = orderId;
        this.amount = amount;
    }
    // getters...
}

// 2. Publisher (Subject)
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher eventPublisher;

    public void placeOrder(Order order) {
        // ... save order ...
        eventPublisher.publishEvent(
            new OrderPlacedEvent(this, order.getId(), order.getTotal())
        );
    }
}

// 3. Listeners (Observers) - completely decoupled from OrderService
@Component
public class EmailNotificationListener {
    @EventListener
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("Sending confirmation email for " + event.getOrderId());
    }
}

@Component
public class InventoryListener {
    @EventListener
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("Reserving inventory for " + event.getOrderId());
    }
}

@Component
public class AnalyticsListener {
    @Async  // Runs in separate thread!
    @EventListener
    public void onOrderPlaced(OrderPlacedEvent event) {
        System.out.println("Tracking order analytics for " + event.getOrderId());
    }
}
```

---

## 3. Django Framework

### MVC/MVT Pattern

Django uses Model-View-Template (MVT) which is a variation of MVC.

| MVC Component | Django Equivalent | Responsibility |
|---------------|-------------------|---------------|
| Model | `models.py` | Database schema, business logic |
| View | `views.py` | Request handling, business logic orchestration |
| Controller | URL dispatcher (`urls.py`) | Routes URLs to views |
| View (display) | `templates/` | HTML rendering |

```python
# models.py - MODEL: defines data + business rules
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    views_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-published_at']

    def increment_views(self):
        """Business logic lives in the model."""
        self.views_count += 1
        self.save(update_fields=['views_count'])


# views.py - VIEW: handles request/response logic
from django.shortcuts import render, get_object_or_404

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.increment_views()
    return render(request, 'articles/detail.html', {'article': article})


# urls.py - CONTROLLER: routes URLs to views
from django.urls import path

urlpatterns = [
    path('articles/<int:pk>/', article_detail, name='article-detail'),
]


# templates/articles/detail.html - TEMPLATE: presentation
# {% extends "base.html" %}
# {% block content %}
#   <h1>{{ article.title }}</h1>
#   <p>{{ article.content }}</p>
#   <small>{{ article.views_count }} views</small>
# {% endblock %}
```

---

### Chain of Responsibility: Django Middleware

Django middleware is a textbook Chain of Responsibility. Each middleware processes the request, optionally short-circuits, and passes to the next.

```python
# settings.py - The chain configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Link 1
    'django.contrib.sessions.middleware.SessionMiddleware', # Link 2
    'django.middleware.common.CommonMiddleware',            # Link 3
    'django.middleware.csrf.CsrfViewMiddleware',           # Link 4
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Link 5
    'myapp.middleware.RateLimitMiddleware',                 # Link 6 (custom)
]

# Request flows:  Security -> Session -> Common -> CSRF -> Auth -> RateLimit -> View
# Response flows: RateLimit -> Auth -> CSRF -> Common -> Session -> Security

# Custom middleware following the chain pattern
class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # Next handler in the chain
        self._request_counts = {}

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        count = self._request_counts.get(ip, 0)

        if count > 100:
            # SHORT-CIRCUIT: Don't pass to next handler
            from django.http import HttpResponse
            return HttpResponse("Rate limited", status=429)

        self._request_counts[ip] = count + 1

        # PASS TO NEXT: Continue the chain
        response = self.get_response(request)

        # Can also modify response on the way back
        response['X-RateLimit-Remaining'] = str(100 - count)
        return response


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        import time
        start = time.time()

        response = self.get_response(request)  # Pass to next in chain

        elapsed = time.time() - start
        print(f"{request.method} {request.path} -> {response.status_code} ({elapsed:.3f}s)")
        return response
```

---

### Template Method: Class-Based Views

Django's class-based views define a skeleton algorithm, and you override specific steps.

```python
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

# ListView template method:
#   1. get_queryset()        - Which objects? (YOU override)
#   2. get_context_data()    - Extra template context? (YOU override)
#   3. get_template_names()  - Which template? (usually automatic)
#   4. render_to_response()  - Render (fixed)

class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    paginate_by = 20
    template_name = 'articles/list.html'

    def get_queryset(self):
        """Override: filter to published articles only."""
        return Article.objects.filter(
            published_at__isnull=False
        ).select_related('author')

    def get_context_data(self, **kwargs):
        """Override: add extra context for template."""
        context = super().get_context_data(**kwargs)
        context['total_articles'] = Article.objects.count()
        return context


# CreateView template method:
#   1. get_form_class()     - Which form? (YOU specify)
#   2. form_valid()         - What to do on valid submit? (YOU override)
#   3. get_success_url()    - Where to redirect? (YOU override)

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['title', 'content']

    def form_valid(self, form):
        """Override: set author before saving."""
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f'/articles/{self.object.pk}/'
```

---

### Active Record / Data Mapper: Django ORM

Django's ORM uses the Active Record pattern -- model instances know how to save/load themselves.

```python
# Active Record: the model IS the database interface
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        """Override save to add validation."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        super().save(*args, **kwargs)

    def purchase(self, quantity):
        """Business logic on the model itself (Active Record style)."""
        if self.stock < quantity:
            raise ValueError("Insufficient stock")
        self.stock -= quantity
        self.save()

# Usage: object handles its own persistence
product = Product(name="Widget", price=9.99, stock=100)
product.save()          # Object saves itself to DB

product.purchase(5)     # Object modifies and saves itself
product.delete()        # Object deletes itself from DB

# QuerySet Manager is a separate Data Mapper-like layer
products = Product.objects.filter(price__lt=20)  # Manager handles queries
```

---

## 4. React Framework

### Observer Pattern: `useState` and `useEffect`

React's state management is the Observer pattern. When state changes, all "observing" components re-render.

```jsx
import React, { useState, useEffect } from 'react';

// useState: Subject (state) + automatic Observer (component re-renders)
function Counter() {
    const [count, setCount] = useState(0);
    // When setCount is called, React "notifies" this component to re-render

    return (
        <div>
            <p>Count: {count}</p>
            <button onClick={() => setCount(count + 1)}>+</button>
        </div>
    );
}

// useEffect: Subscribe to state changes (like adding an observer)
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        // This "observer" runs whenever userId changes
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(setUser);

        // Cleanup: "unsubscribe" when component unmounts
        return () => console.log('Cleanup for', userId);
    }, [userId]);  // Dependency array = "observe these values"

    return user ? <h1>{user.name}</h1> : <p>Loading...</p>;
}

// Context API: Global state with Observer pattern
const ThemeContext = React.createContext('light');

function App() {
    const [theme, setTheme] = useState('light');
    // All consumers of ThemeContext re-render when theme changes
    return (
        <ThemeContext.Provider value={theme}>
            <Header />
            <Content />
            <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
                Toggle Theme
            </button>
        </ThemeContext.Provider>
    );
}

function Header() {
    const theme = React.useContext(ThemeContext);  // "Subscribes" to theme changes
    return <header className={theme}>My App</header>;
}
```

---

### Strategy Pattern: Render Props and Component Injection

```jsx
// Strategy: Different rendering strategies injected via props

// 1. Render Props (function as child)
function DataFetcher({ url, render }) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetch(url)
            .then(res => res.json())
            .then(d => { setData(d); setLoading(false); });
    }, [url]);

    // Delegate rendering STRATEGY to the caller
    return render({ data, loading });
}

// Different rendering strategies for the same data:
function App() {
    return (
        <>
            {/* Strategy 1: Table view */}
            <DataFetcher
                url="/api/users"
                render={({ data, loading }) =>
                    loading ? <Spinner /> : <UserTable users={data} />
                }
            />

            {/* Strategy 2: Card view (same data, different presentation) */}
            <DataFetcher
                url="/api/users"
                render={({ data, loading }) =>
                    loading ? <Spinner /> : <UserCards users={data} />
                }
            />
        </>
    );
}

// 2. Component injection (Strategy via props)
function SortableList({ items, comparator }) {
    // comparator is a Strategy
    const sorted = [...items].sort(comparator);
    return <ul>{sorted.map(item => <li key={item.id}>{item.name}</li>)}</ul>;
}

// Usage with different sorting strategies:
<SortableList items={users} comparator={(a, b) => a.name.localeCompare(b.name)} />
<SortableList items={users} comparator={(a, b) => b.rating - a.rating} />
```

---

### Composite Pattern: Component Tree

React's entire rendering model is the Composite pattern. Components can contain other components, forming a tree. Leaf and composite nodes share the same interface.

```jsx
// Every React component has the same interface: receives props, returns JSX
// Leaf and composite components are interchangeable

// Leaf component (no children)
function Text({ content }) {
    return <span>{content}</span>;
}

function Icon({ name }) {
    return <i className={`icon-${name}`} />;
}

// Composite component (contains children)
function Card({ title, children }) {
    return (
        <div className="card">
            <h3>{title}</h3>
            <div className="card-body">{children}</div>
        </div>
    );
}

function Page({ children }) {
    return (
        <main className="page">
            <header>My App</header>
            {children}
            <footer>Copyright 2024</footer>
        </main>
    );
}

// Compose the tree - same interface everywhere
function App() {
    return (
        <Page>                                    {/* Composite */}
            <Card title="Welcome">                {/* Composite */}
                <Icon name="star" />              {/* Leaf */}
                <Text content="Hello world!" />   {/* Leaf */}
            </Card>
            <Card title="Stats">                  {/* Composite */}
                <Text content="42 items" />       {/* Leaf */}
            </Card>
        </Page>
    );
}

// React.Children utilities work uniformly on the composite tree
function Layout({ children }) {
    return (
        <div className="grid">
            {React.Children.map(children, (child, index) => (
                <div className="grid-item" key={index}>
                    {child}  {/* Works whether child is leaf or composite */}
                </div>
            ))}
        </div>
    );
}
```

---

### Decorator Pattern: Higher-Order Components (HOCs)

HOCs wrap a component to add behavior, exactly like the Decorator pattern.

```jsx
// HOC: Takes a component, returns an enhanced component

// 1. withAuth: Adds authentication check
function withAuth(WrappedComponent) {
    return function AuthenticatedComponent(props) {
        const [user, setUser] = useState(null);

        useEffect(() => {
            // Check authentication
            const token = localStorage.getItem('token');
            if (token) {
                setUser({ name: 'User' });
            }
        }, []);

        if (!user) {
            return <LoginPage />;  // Short-circuit: show login
        }

        // Render wrapped component with user injected
        return <WrappedComponent {...props} currentUser={user} />;
    };
}

// 2. withLogging: Adds lifecycle logging
function withLogging(WrappedComponent) {
    return function LoggedComponent(props) {
        useEffect(() => {
            console.log(`${WrappedComponent.name} mounted`);
            return () => console.log(`${WrappedComponent.name} unmounted`);
        }, []);

        return <WrappedComponent {...props} />;
    };
}

// 3. Stack decorators (same as Python/GoF decorator stacking)
function Dashboard({ currentUser }) {
    return <h1>Welcome, {currentUser.name}!</h1>;
}

// Apply decorators: Dashboard wrapped with logging, then auth
const EnhancedDashboard = withAuth(withLogging(Dashboard));
// Renders: Auth check -> Log mount -> Dashboard

// Modern React uses hooks instead of HOCs for most cases:
function useAuth() {
    const [user, setUser] = useState(null);
    useEffect(() => { /* auth check */ }, []);
    return user;
}

function Dashboard() {
    const user = useAuth();  // Custom hook replaces HOC
    if (!user) return <LoginPage />;
    return <h1>Welcome, {user.name}!</h1>;
}
```

---

## Summary: Patterns Across Frameworks

| Pattern | Python | Java/Spring | Django | React |
|---------|--------|-------------|--------|-------|
| **Iterator** | `__iter__`/`__next__`, generators | `Iterator<T>`, Streams | `QuerySet` iteration | `Array.map()`, iterables |
| **Decorator** | `@decorator` syntax, `functools` | Spring AOP `@Aspect` | Middleware decorators | HOCs, custom hooks |
| **Singleton** | `None`, modules, `__new__` | `@Scope("singleton")` | Settings module | Context providers |
| **Factory** | `classmethod`, `datetime.now()` | `BeanFactory`, `FactoryBean` | `Model.objects.create()` | `React.createElement()` |
| **Observer** | `signal` module | `@EventListener` | Django signals | `useState`, `useEffect` |
| **Template Method** | `collections.abc` | `JdbcTemplate` | Class-Based Views | Lifecycle methods |
| **Chain of Resp** | WSGI middleware | Filter chain | Middleware stack | Middleware (Next.js) |
| **Strategy** | First-class functions | `@Qualifier` injection | Configurable backends | Render props, callbacks |
| **Composite** | - | Spring component scan | Template inheritance | Component tree |
| **Proxy** | `__getattr__` | Spring AOP proxies | Lazy querysets | `React.forwardRef` |

> **Interview insight**: When asked "give me a real-world example of X pattern," referencing framework internals shows deep understanding. A candidate who says "Spring's `@Transactional` is the Proxy pattern" demonstrates they don't just know patterns in theory but recognize them in production code they use daily.
