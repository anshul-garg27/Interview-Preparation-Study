# Design Pattern Practice Exercises

## Section A: Pattern Identification

For each scenario, identify the most appropriate design pattern and explain why.

### Scenario 1
> You need to add logging, encryption, and compression to a file writer without modifying the original class. These features should be composable in any combination.

**Answer:** **Decorator Pattern** — Wraps the original object with additional behavior. Each decorator (Logger, Encryptor, Compressor) implements the same interface and can be stacked in any order.

---

### Scenario 2
> Your application needs to support multiple database backends (MySQL, PostgreSQL, MongoDB). The client code should not change when switching databases.

**Answer:** **Abstract Factory** or **Strategy Pattern** — Abstract Factory if you need families of related objects (connection, query builder, migration tool). Strategy if it's just swappable query execution behavior.

---

### Scenario 3
> A stock trading platform needs to notify multiple displays (price chart, ticker tape, alert panel) whenever a stock price changes.

**Answer:** **Observer Pattern** — The stock price is the subject. Each display subscribes to price changes and updates automatically.

---

### Scenario 4
> You're building a document editor with undo/redo functionality. Each action (bold, delete, insert) must be reversible.

**Answer:** **Command Pattern** — Each action is encapsulated as a command object with `execute()` and `undo()` methods. A history stack manages undo/redo.

---

### Scenario 5
> An e-commerce system needs to calculate discounts differently: percentage off, flat discount, buy-one-get-one, seasonal discount. The discount strategy can change at runtime.

**Answer:** **Strategy Pattern** — Each discount type implements a `DiscountStrategy` interface. The pricing engine accepts any strategy at runtime.

---

### Scenario 6
> You need to integrate with a legacy payment gateway that has an incompatible interface. Your system expects `charge(amount, currency)` but the legacy system uses `makePayment(cents, countryCode, merchantId)`.

**Answer:** **Adapter Pattern** — Create an adapter that implements your expected interface and internally translates calls to the legacy system's API.

---

### Scenario 7
> A game character can be in states: Idle, Walking, Running, Jumping, Attacking. Each state determines which actions are valid and what transitions are allowed.

**Answer:** **State Pattern** — Each state is a class implementing a common interface. The character delegates behavior to its current state object, which handles transitions.

---

### Scenario 8
> You need to build complex SQL queries step by step: SELECT, FROM, WHERE, JOIN, ORDER BY, LIMIT. The query construction should be fluent and the final object immutable.

**Answer:** **Builder Pattern** — A `QueryBuilder` allows step-by-step construction with method chaining. The `build()` method returns an immutable `Query` object.

---

### Scenario 9
> A file system has files and directories. Directories can contain files or other directories. You need to calculate total size uniformly regardless of nesting.

**Answer:** **Composite Pattern** — Both `File` and `Directory` implement a common `FileSystemNode` interface with a `size()` method. Directory's `size()` sums its children's sizes recursively.

---

### Scenario 10
> A web server receives requests that need to pass through authentication, rate limiting, logging, and validation checks in sequence. Each check can either pass the request forward or reject it.

**Answer:** **Chain of Responsibility** — Each middleware is a handler in the chain. Each handler decides to process the request and pass it forward, or reject it.

---

### Scenario 11
> You want to ensure only one database connection pool exists throughout the application, and it must be lazily initialized and thread-safe.

**Answer:** **Singleton Pattern** — Ensures a single instance. In Python, use a module-level instance, metaclass, or `__new__` override with thread locking.

---

### Scenario 12
> A drawing application needs to create different types of shapes (Circle, Rectangle, Line) based on the tool selected by the user, without the canvas knowing the concrete shape classes.

**Answer:** **Factory Method** — Each tool creates its shape through a factory method. The canvas works with the abstract `Shape` interface.

---

### Scenario 13
> A text editor needs to efficiently store document snapshots for undo. Storing full copies is wasteful since most of the text hasn't changed.

**Answer:** **Memento Pattern** — Captures the document's internal state in a memento object. Can also combine with **Flyweight** to share unchanged text segments.

---

### Scenario 14
> You want to provide a simplified interface to a complex subsystem involving audio codecs, video processors, subtitle parsers, and file format handlers for a media player.

**Answer:** **Facade Pattern** — A `MediaPlayer` facade provides simple methods like `play(file)` that coordinate the complex subsystem internally.

---

### Scenario 15
> You need to traverse different data structures (tree, graph, linked list) uniformly, and support multiple traversal strategies (DFS, BFS, in-order).

**Answer:** **Iterator Pattern** — Each data structure provides an iterator implementing a common interface (`has_next()`, `next()`). Different traversal strategies are different iterator implementations.

---

## Section B: Implementation Challenges

### Challenge 1: Observer — Weather Station

**Problem:** Implement an Observer pattern for a weather station that broadcasts temperature, humidity, and pressure to multiple display units.

**Starter Code:**
```python
class WeatherStation:
    """Implement: register, remove, notify observers. Store weather data."""
    pass

class TemperatureDisplay:
    """Implement: update method to display temperature."""
    pass

class StatisticsDisplay:
    """Implement: update method to track and display avg/min/max temperature."""
    pass

# Usage:
# station = WeatherStation()
# temp_display = TemperatureDisplay()
# stats_display = StatisticsDisplay()
# station.register(temp_display)
# station.register(stats_display)
# station.set_measurements(25.0, 65.0, 1013.0)
# station.set_measurements(28.0, 70.0, 1012.0)
```

**Hints:**
- Define an Observer interface with `update(temperature, humidity, pressure)`
- WeatherStation maintains a list of observers
- `set_measurements` should notify all observers

**Solution:**

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, temperature: float, humidity: float, pressure: float):
        pass

class WeatherStation:
    def __init__(self):
        self._observers: list[Observer] = []
        self._temperature = 0.0
        self._humidity = 0.0
        self._pressure = 0.0

    def register(self, observer: Observer):
        self._observers.append(observer)

    def remove(self, observer: Observer):
        self._observers.remove(observer)

    def _notify_observers(self):
        for observer in self._observers:
            observer.update(self._temperature, self._humidity, self._pressure)

    def set_measurements(self, temperature: float, humidity: float, pressure: float):
        self._temperature = temperature
        self._humidity = humidity
        self._pressure = pressure
        self._notify_observers()

class TemperatureDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print(f"[Temperature Display] Current temperature: {temperature}°C")

class StatisticsDisplay(Observer):
    def __init__(self):
        self._temperatures: list[float] = []

    def update(self, temperature, humidity, pressure):
        self._temperatures.append(temperature)
        avg = sum(self._temperatures) / len(self._temperatures)
        min_t = min(self._temperatures)
        max_t = max(self._temperatures)
        print(f"[Statistics Display] Avg: {avg:.1f}°C, Min: {min_t}°C, Max: {max_t}°C")

class HumidityDisplay(Observer):
    def update(self, temperature, humidity, pressure):
        print(f"[Humidity Display] Current humidity: {humidity}%")

# Test
station = WeatherStation()
station.register(TemperatureDisplay())
station.register(StatisticsDisplay())
station.register(HumidityDisplay())

station.set_measurements(25.0, 65.0, 1013.0)
print()
station.set_measurements(28.0, 70.0, 1012.0)
print()
station.set_measurements(22.0, 90.0, 1015.0)
```

---

### Challenge 2: Strategy — Discount Calculator

**Problem:** Implement a Strategy pattern for an e-commerce discount system that supports multiple discount types.

**Starter Code:**
```python
class ShoppingCart:
    """Implement: add items, set discount strategy, calculate total."""
    pass

# Strategies to implement:
# - NoDiscount
# - PercentageDiscount(percent)
# - FlatDiscount(amount)
# - BuyOneGetOneFree (every second item is free, cheapest items free)
```

**Solution:**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CartItem:
    name: str
    price: float
    quantity: int

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate_discount(self, items: list[CartItem]) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

class NoDiscount(DiscountStrategy):
    def calculate_discount(self, items):
        return 0.0

    def description(self):
        return "No discount"

class PercentageDiscount(DiscountStrategy):
    def __init__(self, percent: float):
        self._percent = percent

    def calculate_discount(self, items):
        total = sum(item.price * item.quantity for item in items)
        return total * (self._percent / 100)

    def description(self):
        return f"{self._percent}% off"

class FlatDiscount(DiscountStrategy):
    def __init__(self, amount: float):
        self._amount = amount

    def calculate_discount(self, items):
        total = sum(item.price * item.quantity for item in items)
        return min(self._amount, total)

    def description(self):
        return f"${self._amount} off"

class BuyOneGetOneFree(DiscountStrategy):
    def calculate_discount(self, items):
        # Expand all items into individual prices and sort ascending
        all_prices = []
        for item in items:
            all_prices.extend([item.price] * item.quantity)
        all_prices.sort()

        # Every second item (cheapest ones) is free
        discount = sum(all_prices[i] for i in range(0, len(all_prices), 2))
        return discount if len(all_prices) > 1 else 0.0

    def description(self):
        return "Buy one get one free"

class ShoppingCart:
    def __init__(self):
        self._items: list[CartItem] = []
        self._discount_strategy: DiscountStrategy = NoDiscount()

    def add_item(self, name: str, price: float, quantity: int = 1):
        self._items.append(CartItem(name, price, quantity))

    def set_discount(self, strategy: DiscountStrategy):
        self._discount_strategy = strategy

    def get_subtotal(self) -> float:
        return sum(item.price * item.quantity for item in self._items)

    def get_discount(self) -> float:
        return self._discount_strategy.calculate_discount(self._items)

    def get_total(self) -> float:
        return self.get_subtotal() - self.get_discount()

    def checkout_summary(self):
        print(f"Items: {len(self._items)}")
        for item in self._items:
            print(f"  {item.name} x{item.quantity} = ${item.price * item.quantity:.2f}")
        print(f"Subtotal: ${self.get_subtotal():.2f}")
        print(f"Discount ({self._discount_strategy.description()}): -${self.get_discount():.2f}")
        print(f"Total: ${self.get_total():.2f}")

# Test
cart = ShoppingCart()
cart.add_item("Laptop", 999.99)
cart.add_item("Mouse", 29.99, 2)
cart.add_item("Keyboard", 79.99)

print("=== No Discount ===")
cart.checkout_summary()

print("\n=== 20% Off ===")
cart.set_discount(PercentageDiscount(20))
cart.checkout_summary()

print("\n=== $100 Off ===")
cart.set_discount(FlatDiscount(100))
cart.checkout_summary()
```

---

### Challenge 3: Factory — Document Converter

**Problem:** Implement a Factory pattern that creates appropriate document parsers based on file type.

**Solution:**

```python
from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def parse(self, content: str) -> dict:
        pass

    @abstractmethod
    def render(self, data: dict) -> str:
        pass

class JSONDocument(Document):
    def parse(self, content):
        import json
        return json.loads(content)

    def render(self, data):
        import json
        return json.dumps(data, indent=2)

class XMLDocument(Document):
    def parse(self, content):
        # Simplified XML parsing
        return {"raw_xml": content}

    def render(self, data):
        lines = ['<?xml version="1.0"?>']
        for key, value in data.items():
            lines.append(f"  <{key}>{value}</{key}>")
        return "\n".join(lines)

class CSVDocument(Document):
    def parse(self, content):
        lines = content.strip().split("\n")
        headers = lines[0].split(",")
        rows = [dict(zip(headers, line.split(","))) for line in lines[1:]]
        return {"headers": headers, "rows": rows}

    def render(self, data):
        lines = [",".join(data["headers"])]
        for row in data["rows"]:
            lines.append(",".join(row[h] for h in data["headers"]))
        return "\n".join(lines)

class YAMLDocument(Document):
    def parse(self, content):
        return {"raw_yaml": content}

    def render(self, data):
        return "\n".join(f"{k}: {v}" for k, v in data.items())

class DocumentFactory:
    """Factory with registration support for OCP compliance."""
    _creators: dict[str, type[Document]] = {}

    @classmethod
    def register(cls, format_type: str, document_class: type[Document]):
        cls._creators[format_type.lower()] = document_class

    @classmethod
    def create(cls, format_type: str) -> Document:
        doc_class = cls._creators.get(format_type.lower())
        if not doc_class:
            raise ValueError(f"Unsupported format: {format_type}. "
                           f"Available: {list(cls._creators.keys())}")
        return doc_class()

# Register formats
DocumentFactory.register("json", JSONDocument)
DocumentFactory.register("xml", XMLDocument)
DocumentFactory.register("csv", CSVDocument)
DocumentFactory.register("yaml", YAMLDocument)

# Usage
doc = DocumentFactory.create("json")
data = doc.parse('{"name": "Alice", "age": 30}')
print(data)  # {'name': 'Alice', 'age': 30}

csv_doc = DocumentFactory.create("csv")
print(csv_doc.render({"headers": ["name", "age"], "rows": [{"name": "Alice", "age": "30"}]}))
```

---

### Challenge 4: State — Traffic Light

**Problem:** Implement a State pattern for a traffic light that cycles through Red, Yellow, Green with different durations and rules.

**Solution:**

```python
from abc import ABC, abstractmethod

class TrafficLightState(ABC):
    @abstractmethod
    def display(self) -> str:
        pass

    @abstractmethod
    def next_state(self, light: "TrafficLight"):
        pass

    @abstractmethod
    def duration(self) -> int:
        """Duration in seconds."""
        pass

    @abstractmethod
    def can_proceed(self) -> bool:
        pass

class RedState(TrafficLightState):
    def display(self):
        return "RED - STOP"

    def next_state(self, light):
        light.set_state(GreenState())

    def duration(self):
        return 30

    def can_proceed(self):
        return False

class YellowState(TrafficLightState):
    def display(self):
        return "YELLOW - CAUTION"

    def next_state(self, light):
        light.set_state(RedState())

    def duration(self):
        return 5

    def can_proceed(self):
        return False

class GreenState(TrafficLightState):
    def display(self):
        return "GREEN - GO"

    def next_state(self, light):
        light.set_state(YellowState())

    def duration(self):
        return 25

    def can_proceed(self):
        return True

class TrafficLight:
    def __init__(self):
        self._state: TrafficLightState = RedState()

    def set_state(self, state: TrafficLightState):
        self._state = state
        print(f"Light changed to: {self._state.display()} (duration: {self._state.duration()}s)")

    def change(self):
        self._state.next_state(self)

    def display(self):
        return self._state.display()

    def can_proceed(self):
        return self._state.can_proceed()

# Test
light = TrafficLight()
print(f"Initial: {light.display()}, Can proceed: {light.can_proceed()}")
for _ in range(6):
    light.change()
```

---

### Challenge 5: Builder — Pizza Order

**Problem:** Implement a Builder pattern for constructing complex pizza orders with validation.

**Solution:**

```python
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Pizza:
    size: str
    crust: str
    sauce: str
    cheese: str
    toppings: tuple[str, ...]
    extras: tuple[str, ...]

    def __str__(self):
        parts = [f"{self.size} pizza on {self.crust} crust",
                 f"Sauce: {self.sauce}, Cheese: {self.cheese}"]
        if self.toppings:
            parts.append(f"Toppings: {', '.join(self.toppings)}")
        if self.extras:
            parts.append(f"Extras: {', '.join(self.extras)}")
        return " | ".join(parts)

class PizzaBuilder:
    VALID_SIZES = ("small", "medium", "large", "extra-large")
    VALID_CRUSTS = ("thin", "regular", "thick", "stuffed")

    def __init__(self):
        self._size = None
        self._crust = None
        self._sauce = "tomato"
        self._cheese = "mozzarella"
        self._toppings: list[str] = []
        self._extras: list[str] = []

    def size(self, size: str) -> "PizzaBuilder":
        if size not in self.VALID_SIZES:
            raise ValueError(f"Invalid size. Choose from: {self.VALID_SIZES}")
        self._size = size
        return self

    def crust(self, crust: str) -> "PizzaBuilder":
        if crust not in self.VALID_CRUSTS:
            raise ValueError(f"Invalid crust. Choose from: {self.VALID_CRUSTS}")
        self._crust = crust
        return self

    def sauce(self, sauce: str) -> "PizzaBuilder":
        self._sauce = sauce
        return self

    def cheese(self, cheese: str) -> "PizzaBuilder":
        self._cheese = cheese
        return self

    def add_topping(self, topping: str) -> "PizzaBuilder":
        if len(self._toppings) >= 10:
            raise ValueError("Maximum 10 toppings allowed")
        self._toppings.append(topping)
        return self

    def add_extra(self, extra: str) -> "PizzaBuilder":
        self._extras.append(extra)
        return self

    def build(self) -> Pizza:
        if not self._size:
            raise ValueError("Size is required")
        if not self._crust:
            raise ValueError("Crust is required")
        return Pizza(
            size=self._size,
            crust=self._crust,
            sauce=self._sauce,
            cheese=self._cheese,
            toppings=tuple(self._toppings),
            extras=tuple(self._extras),
        )

# Predefined recipes (Director role)
class PizzaRecipes:
    @staticmethod
    def margherita() -> Pizza:
        return (PizzaBuilder()
                .size("medium").crust("thin").sauce("tomato")
                .cheese("fresh mozzarella").add_topping("basil")
                .build())

    @staticmethod
    def meat_lovers() -> Pizza:
        return (PizzaBuilder()
                .size("large").crust("regular").sauce("tomato")
                .cheese("mozzarella")
                .add_topping("pepperoni").add_topping("sausage")
                .add_topping("bacon").add_topping("ham")
                .build())

# Test
custom = (PizzaBuilder()
          .size("large")
          .crust("stuffed")
          .sauce("bbq")
          .cheese("cheddar")
          .add_topping("chicken")
          .add_topping("onion")
          .add_topping("jalapeno")
          .add_extra("garlic dip")
          .build())

print("Custom:", custom)
print("Margherita:", PizzaRecipes.margherita())
print("Meat Lovers:", PizzaRecipes.meat_lovers())
```

---

### Challenge 6: Decorator — Text Formatter

**Problem:** Implement a Decorator pattern for composable text formatting operations.

**Solution:**

```python
from abc import ABC, abstractmethod

class TextComponent(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class PlainText(TextComponent):
    def __init__(self, text: str):
        self._text = text

    def render(self):
        return self._text

class TextDecorator(TextComponent):
    def __init__(self, component: TextComponent):
        self._component = component

class BoldDecorator(TextDecorator):
    def render(self):
        return f"**{self._component.render()}**"

class ItalicDecorator(TextDecorator):
    def render(self):
        return f"*{self._component.render()}*"

class UnderlineDecorator(TextDecorator):
    def render(self):
        return f"<u>{self._component.render()}</u>"

class UpperCaseDecorator(TextDecorator):
    def render(self):
        return self._component.render().upper()

class BorderDecorator(TextDecorator):
    def __init__(self, component: TextComponent, char: str = "*"):
        super().__init__(component)
        self._char = char

    def render(self):
        content = self._component.render()
        width = len(content) + 4
        border = self._char * width
        return f"{border}\n{self._char} {content} {self._char}\n{border}"

# Composable usage
text = PlainText("Hello, World!")
print("Plain:", text.render())

bold_text = BoldDecorator(text)
print("Bold:", bold_text.render())

bold_italic = ItalicDecorator(BoldDecorator(text))
print("Bold+Italic:", bold_italic.render())

fancy = BorderDecorator(UpperCaseDecorator(BoldDecorator(text)), "=")
print("Fancy:")
print(fancy.render())
```

---

### Challenge 7: Command — Calculator with Undo

**Problem:** Implement a Command pattern for a calculator that supports undo/redo.

**Solution:**

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self) -> float:
        pass

    @abstractmethod
    def undo(self) -> float:
        pass

class AddCommand(Command):
    def __init__(self, calculator: "Calculator", value: float):
        self._calc = calculator
        self._value = value

    def execute(self):
        self._calc._current += self._value
        return self._calc._current

    def undo(self):
        self._calc._current -= self._value
        return self._calc._current

class SubtractCommand(Command):
    def __init__(self, calculator, value):
        self._calc = calculator
        self._value = value

    def execute(self):
        self._calc._current -= self._value
        return self._calc._current

    def undo(self):
        self._calc._current += self._value
        return self._calc._current

class MultiplyCommand(Command):
    def __init__(self, calculator, value):
        self._calc = calculator
        self._value = value

    def execute(self):
        self._calc._current *= self._value
        return self._calc._current

    def undo(self):
        self._calc._current /= self._value
        return self._calc._current

class DivideCommand(Command):
    def __init__(self, calculator, value):
        self._calc = calculator
        self._value = value

    def execute(self):
        if self._value == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self._calc._current /= self._value
        return self._calc._current

    def undo(self):
        self._calc._current *= self._value
        return self._calc._current

class Calculator:
    def __init__(self):
        self._current = 0.0
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    @property
    def value(self):
        return self._current

    def _execute(self, command: Command):
        result = command.execute()
        self._history.append(command)
        self._redo_stack.clear()  # Clear redo on new action
        return result

    def add(self, value: float):
        return self._execute(AddCommand(self, value))

    def subtract(self, value: float):
        return self._execute(SubtractCommand(self, value))

    def multiply(self, value: float):
        return self._execute(MultiplyCommand(self, value))

    def divide(self, value: float):
        return self._execute(DivideCommand(self, value))

    def undo(self):
        if not self._history:
            print("Nothing to undo")
            return self._current
        command = self._history.pop()
        result = command.undo()
        self._redo_stack.append(command)
        return result

    def redo(self):
        if not self._redo_stack:
            print("Nothing to redo")
            return self._current
        command = self._redo_stack.pop()
        result = command.execute()
        self._history.append(command)
        return result

# Test
calc = Calculator()
print(f"Start: {calc.value}")
print(f"+ 10 = {calc.add(10)}")
print(f"* 3  = {calc.multiply(3)}")
print(f"- 5  = {calc.subtract(5)}")
print(f"/ 5  = {calc.divide(5)}")
print(f"Undo: {calc.undo()}")
print(f"Undo: {calc.undo()}")
print(f"Redo: {calc.redo()}")
```

---

### Challenge 8: Adapter — Legacy Payment System

**Problem:** Implement an Adapter to integrate a legacy payment system with a modern interface.

**Solution:**

```python
from abc import ABC, abstractmethod

# Modern interface your system uses
class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, amount: float, currency: str, card_token: str) -> dict:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> dict:
        pass

# Modern gateway (works natively)
class StripeGateway(PaymentGateway):
    def charge(self, amount, currency, card_token):
        return {"status": "success", "tx_id": "stripe_123", "amount": amount}

    def refund(self, transaction_id, amount):
        return {"status": "refunded", "tx_id": transaction_id}

# Legacy system with incompatible interface
class LegacyPaymentProcessor:
    """Cannot be modified — it's a third-party library."""
    def make_payment(self, amount_in_cents: int, country_code: str,
                     merchant_id: str, card_number: str) -> str:
        return f"LEGACY_TX_{amount_in_cents}"

    def reverse_payment(self, original_tx: str, amount_in_cents: int,
                        reason_code: int) -> bool:
        return True

# Adapter
CURRENCY_TO_COUNTRY = {"USD": "US", "EUR": "EU", "GBP": "UK", "INR": "IN"}

class LegacyPaymentAdapter(PaymentGateway):
    def __init__(self, legacy: LegacyPaymentProcessor, merchant_id: str):
        self._legacy = legacy
        self._merchant_id = merchant_id

    def charge(self, amount, currency, card_token):
        cents = int(amount * 100)
        country = CURRENCY_TO_COUNTRY.get(currency, "US")
        tx_id = self._legacy.make_payment(cents, country, self._merchant_id, card_token)
        return {"status": "success", "tx_id": tx_id, "amount": amount}

    def refund(self, transaction_id, amount):
        cents = int(amount * 100)
        success = self._legacy.reverse_payment(transaction_id, cents, reason_code=1)
        status = "refunded" if success else "failed"
        return {"status": status, "tx_id": transaction_id}

# Client code works with any gateway
def process_order(gateway: PaymentGateway, amount: float):
    result = gateway.charge(amount, "USD", "tok_test_123")
    print(f"Charge result: {result}")
    return result

# Works with modern gateway
process_order(StripeGateway(), 99.99)

# Works with legacy via adapter
legacy_adapter = LegacyPaymentAdapter(LegacyPaymentProcessor(), "MERCHANT_001")
process_order(legacy_adapter, 99.99)
```

---

### Challenge 9: Composite — Menu System

**Problem:** Implement a Composite pattern for a restaurant menu with nested categories.

**Solution:**

```python
from abc import ABC, abstractmethod

class MenuComponent(ABC):
    @abstractmethod
    def display(self, indent: int = 0) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

class MenuItem(MenuComponent):
    def __init__(self, name: str, price: float, description: str = ""):
        self._name = name
        self._price = price
        self._description = description

    def display(self, indent=0):
        prefix = "  " * indent
        desc = f" - {self._description}" if self._description else ""
        return f"{prefix}{self._name}: ${self._price:.2f}{desc}"

    def get_price(self):
        return self._price

class MenuCategory(MenuComponent):
    def __init__(self, name: str):
        self._name = name
        self._children: list[MenuComponent] = []

    def add(self, component: MenuComponent):
        self._children.append(component)

    def remove(self, component: MenuComponent):
        self._children.remove(component)

    def display(self, indent=0):
        prefix = "  " * indent
        lines = [f"{prefix}[{self._name}]"]
        for child in self._children:
            lines.append(child.display(indent + 1))
        return "\n".join(lines)

    def get_price(self):
        return sum(child.get_price() for child in self._children)

# Build menu
menu = MenuCategory("Main Menu")

appetizers = MenuCategory("Appetizers")
appetizers.add(MenuItem("Soup", 5.99, "Cream of mushroom"))
appetizers.add(MenuItem("Salad", 7.99, "Caesar salad"))
appetizers.add(MenuItem("Bruschetta", 6.99))

mains = MenuCategory("Main Course")
pasta = MenuCategory("Pasta")
pasta.add(MenuItem("Spaghetti Bolognese", 14.99))
pasta.add(MenuItem("Fettuccine Alfredo", 13.99))
mains.add(pasta)

grill = MenuCategory("From the Grill")
grill.add(MenuItem("Ribeye Steak", 24.99))
grill.add(MenuItem("Grilled Salmon", 19.99))
mains.add(grill)

desserts = MenuCategory("Desserts")
desserts.add(MenuItem("Tiramisu", 8.99))
desserts.add(MenuItem("Cheesecake", 7.99))

menu.add(appetizers)
menu.add(mains)
menu.add(desserts)

print(menu.display())
print(f"\nTotal menu value: ${menu.get_price():.2f}")
```

---

### Challenge 10: Chain of Responsibility — Validation Pipeline

**Problem:** Implement a Chain of Responsibility for validating user registration data.

**Solution:**

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class RegistrationData:
    username: str
    email: str
    password: str
    age: int

@dataclass
class ValidationResult:
    is_valid: bool
    errors: list[str]

class ValidationHandler(ABC):
    def __init__(self):
        self._next: ValidationHandler | None = None

    def set_next(self, handler: "ValidationHandler") -> "ValidationHandler":
        self._next = handler
        return handler

    def handle(self, data: RegistrationData, errors: list[str]) -> list[str]:
        self._validate(data, errors)
        if self._next:
            return self._next.handle(data, errors)
        return errors

    @abstractmethod
    def _validate(self, data: RegistrationData, errors: list[str]):
        pass

class UsernameValidator(ValidationHandler):
    def _validate(self, data, errors):
        if not data.username:
            errors.append("Username is required")
        elif len(data.username) < 3:
            errors.append("Username must be at least 3 characters")
        elif len(data.username) > 20:
            errors.append("Username must be at most 20 characters")
        elif not data.username.isalnum():
            errors.append("Username must be alphanumeric")

class EmailValidator(ValidationHandler):
    def _validate(self, data, errors):
        if not data.email:
            errors.append("Email is required")
        elif "@" not in data.email or "." not in data.email.split("@")[-1]:
            errors.append("Invalid email format")

class PasswordValidator(ValidationHandler):
    def _validate(self, data, errors):
        if not data.password:
            errors.append("Password is required")
            return
        if len(data.password) < 8:
            errors.append("Password must be at least 8 characters")
        if not any(c.isupper() for c in data.password):
            errors.append("Password must contain an uppercase letter")
        if not any(c.isdigit() for c in data.password):
            errors.append("Password must contain a digit")
        if not any(c in "!@#$%^&*" for c in data.password):
            errors.append("Password must contain a special character (!@#$%^&*)")

class AgeValidator(ValidationHandler):
    def _validate(self, data, errors):
        if data.age < 13:
            errors.append("Must be at least 13 years old")
        elif data.age > 120:
            errors.append("Invalid age")

class RegistrationValidator:
    def __init__(self):
        self._chain = UsernameValidator()
        self._chain.set_next(EmailValidator()).set_next(
            PasswordValidator()).set_next(AgeValidator())

    def validate(self, data: RegistrationData) -> ValidationResult:
        errors = self._chain.handle(data, [])
        return ValidationResult(is_valid=len(errors) == 0, errors=errors)

# Test
validator = RegistrationValidator()

print("=== Valid registration ===")
result = validator.validate(RegistrationData("alice", "alice@example.com", "Str0ng!Pass", 25))
print(f"Valid: {result.is_valid}, Errors: {result.errors}")

print("\n=== Invalid registration ===")
result = validator.validate(RegistrationData("ab", "bad-email", "weak", 10))
print(f"Valid: {result.is_valid}")
for err in result.errors:
    print(f"  - {err}")
```

---

## Section C: Pattern Comparisons

### Comparison 1: Strategy vs State

| Aspect | Strategy | State |
|--------|----------|-------|
| **Intent** | Define a family of interchangeable algorithms | Allow object to change behavior when internal state changes |
| **Who decides?** | Client selects the strategy | State transitions happen internally |
| **Awareness** | Strategies don't know about each other | States know about other states (for transitions) |
| **Replaceability** | Strategies are freely swappable | States follow defined transition rules |
| **Example** | Sorting algorithm (quicksort, mergesort) | TCP connection (listen, established, closed) |

**Rule of thumb:** If the behavior change is driven by external choice, use Strategy. If it's driven by internal state transitions, use State.

---

### Comparison 2: Command vs Strategy

| Aspect | Command | Strategy |
|--------|---------|----------|
| **Intent** | Encapsulate a request as an object | Define interchangeable algorithms |
| **Undo support** | Yes, built-in concept | No |
| **When created** | Can be created and executed later (deferred) | Typically set once and used immediately |
| **History** | Commands are often queued/logged | Strategies are not queued |
| **Example** | Text editor operations with undo | Discount calculation methods |

**Rule of thumb:** Command is for "do this thing (and maybe undo it later)." Strategy is for "do this thing this way (instead of that way)."

---

### Comparison 3: Adapter vs Facade

| Aspect | Adapter | Facade |
|--------|---------|--------|
| **Intent** | Make incompatible interface compatible | Simplify a complex subsystem |
| **Direction** | Wraps ONE existing class | Wraps MULTIPLE classes |
| **Interface** | Matches an expected interface | Defines a NEW simplified interface |
| **Existing code** | Works with code you can't change | Works with code you own but is complex |
| **Example** | Legacy API to modern interface | Media player simplifying codecs/decoders |

---

### Comparison 4: Abstract Factory vs Factory Method

| Aspect | Abstract Factory | Factory Method |
|--------|-----------------|----------------|
| **Scope** | Family of related objects | Single object |
| **Implementation** | Object composition (factory object) | Class inheritance (subclass override) |
| **Flexibility** | Swap entire product family | Swap one product type |
| **Example** | UI toolkit (Button, Checkbox for Mac/Windows) | Document app (createDocument in subclasses) |

---

### Comparison 5: Decorator vs Proxy

| Aspect | Decorator | Proxy |
|--------|-----------|-------|
| **Intent** | Add behavior dynamically | Control access to object |
| **Stacking** | Multiple decorators can stack | Usually single proxy |
| **Lifecycle** | Wrappee always exists | Proxy may create wrappee lazily |
| **Examples** | Add logging + caching + validation | Lazy loading, access control, remote proxy |

**Rule of thumb:** If you're adding features, use Decorator. If you're controlling access, use Proxy.
