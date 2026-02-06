# Complete LLD Glossary (A to Z)

> 100+ terms every LLD interview candidate must know, organized alphabetically with definitions, examples, and cross-references.

---

## A

### Abstraction
**Definition:** Hiding complex implementation details and exposing only the essential features of an object or system.
**Example:** A `Vehicle` abstract class exposes `start()` and `stop()` but hides engine internals.
**Related:** Encapsulation, Interface, Abstract Class

### Abstract Class
**Definition:** A class that cannot be instantiated directly and may contain both abstract (unimplemented) and concrete (implemented) methods.
**Example:** `abstract class Shape { abstract double area(); void printInfo() { ... } }`
**Related:** Interface, Pure Virtual Function, Concrete Class

### Abstract Factory
**Definition:** A creational design pattern that provides an interface for creating families of related objects without specifying their concrete classes.
**Example:** `UIFactory` creates `Button`, `TextField`, and `Checkbox` for either Windows or Mac.
**Related:** Factory Method, Builder, Prototype

### Adapter
**Definition:** A structural pattern that allows incompatible interfaces to work together by wrapping one interface to match another.
**Example:** Converting a `LegacyPrinter` with `printText()` to conform to a `ModernPrinter` interface with `print()`.
**Related:** Bridge, Facade, Decorator, Proxy

### Aggregation
**Definition:** A "has-a" relationship where the child object can exist independently of the parent. The parent does not own the child's lifecycle.
**Example:** A `Department` has `Professor` objects, but professors exist even if the department is deleted.
**Related:** Composition, Association, Multiplicity

### Anti-Pattern
**Definition:** A commonly used but ineffective or counterproductive solution to a recurring problem.
**Example:** God Object, Spaghetti Code, Lava Flow.
**Related:** Design Pattern, Refactoring, Code Smell

### Association
**Definition:** A relationship between two classes where one class uses or interacts with another. The most general form of relationship.
**Example:** A `Student` is associated with a `Course` (many-to-many).
**Related:** Aggregation, Composition, Dependency, Multiplicity

---

## B

### Behavioral Pattern
**Definition:** A category of design patterns concerned with algorithms, communication, and the assignment of responsibilities between objects.
**Example:** Strategy, Observer, Command, State, Iterator.
**Related:** Creational Pattern, Structural Pattern, Gang of Four

### Bridge Pattern
**Definition:** A structural pattern that decouples an abstraction from its implementation so both can vary independently.
**Example:** Separating `Shape` (Circle, Square) from `Renderer` (VectorRenderer, RasterRenderer).
**Related:** Adapter, Strategy, Abstract Factory

### Builder Pattern
**Definition:** A creational pattern that separates the construction of a complex object from its representation, allowing the same construction process to create different representations.
**Example:** `PizzaBuilder` with methods like `setSize()`, `addTopping()`, `setCrust()` and a final `build()`.
**Related:** Abstract Factory, Composite, Prototype

---

## C

### Chain of Responsibility
**Definition:** A behavioral pattern where a request is passed along a chain of handlers until one handles it.
**Example:** Logging levels (DEBUG -> INFO -> WARN -> ERROR) where each handler decides whether to process or pass on.
**Related:** Command, Decorator, Composite

### Class
**Definition:** A blueprint or template that defines the properties (attributes) and behaviors (methods) of objects.
**Example:** `class Car { String color; int speed; void accelerate() { ... } }`
**Related:** Object, Abstract Class, Concrete Class, Interface

### Class Diagram
**Definition:** A UML diagram that shows classes, their attributes, methods, and the relationships between them.
**Example:** A diagram showing `User`, `Order`, and `Product` classes with their associations.
**Related:** UML, Sequence Diagram, State Diagram

### Cohesion
**Definition:** The degree to which the elements inside a module (class/method) belong together. High cohesion means a class has a single, well-defined purpose.
**Example:** A `UserValidator` class that only validates user data has high cohesion. A `UserManager` that handles validation, persistence, and emailing has low cohesion.
**Related:** Coupling, SRP, GRASP, High Cohesion

### Code Smell
**Definition:** A surface-level indication in code that suggests a deeper design problem, though it may not be a bug itself.
**Example:** Long methods, large classes, feature envy, data clumps, primitive obsession.
**Related:** Anti-Pattern, Refactoring

### Command Pattern
**Definition:** A behavioral pattern that encapsulates a request as an object, allowing parameterization, queuing, logging, and undo/redo of operations.
**Example:** `LightOnCommand` wraps a `Light.turnOn()` call and can be undone with `Light.turnOff()`.
**Related:** Memento, Chain of Responsibility, Strategy

### Composite Pattern
**Definition:** A structural pattern that composes objects into tree structures to represent part-whole hierarchies, letting clients treat individual and composite objects uniformly.
**Example:** A `FileSystem` where both `File` and `Directory` implement `FileSystemComponent`.
**Related:** Iterator, Decorator, Builder, Chain of Responsibility

### Composition
**Definition:** A strong "has-a" relationship where the child object's lifecycle is entirely managed by the parent. If the parent is destroyed, so are the children.
**Example:** A `House` is composed of `Room` objects; rooms do not exist without the house.
**Related:** Aggregation, Association, Inheritance, Composition over Inheritance

### Composition over Inheritance
**Definition:** A design principle that favors composing objects with desired behaviors rather than inheriting from parent classes.
**Example:** Instead of `FlyingDuck extends Duck`, use `Duck` with a `FlyBehavior` field.
**Related:** Strategy Pattern, Delegation, Inheritance, Open-Closed Principle

### Concrete Class
**Definition:** A class that can be instantiated and has all its methods implemented (no abstract methods left unimplemented).
**Example:** `class Circle extends Shape { double area() { return Math.PI * r * r; } }`
**Related:** Abstract Class, Interface, Instantiation

### Coupling
**Definition:** The degree of interdependence between modules or classes. Low (loose) coupling is preferred for maintainability.
**Example:** A class that depends on an interface rather than a concrete class has low coupling.
**Related:** Cohesion, Dependency Injection, Dependency Inversion, Loose Coupling

### Creational Pattern
**Definition:** A category of design patterns that deal with object creation mechanisms, controlling how objects are instantiated.
**Example:** Singleton, Factory Method, Abstract Factory, Builder, Prototype.
**Related:** Structural Pattern, Behavioral Pattern, Gang of Four

---

## D

### Decorator Pattern
**Definition:** A structural pattern that dynamically adds responsibilities to objects by wrapping them, as an alternative to subclassing.
**Example:** `BufferedInputStream(new FileInputStream("file.txt"))` adds buffering to a stream.
**Related:** Composite, Proxy, Adapter, Chain of Responsibility

### Delegation
**Definition:** A technique where an object handles a request by forwarding it to a second helper object (the delegate).
**Example:** `class Printer { InkJet inkjet; void print() { inkjet.print(); } }`
**Related:** Composition, Strategy, Proxy

### Dependency
**Definition:** A relationship where one class relies on another for its functionality. If the depended-upon class changes, the dependent class may need to change.
**Example:** `OrderService` depends on `PaymentGateway` to process payments.
**Related:** Coupling, Dependency Injection, Dependency Inversion, Association

### Dependency Injection (DI)
**Definition:** A technique where an object receives its dependencies from external sources rather than creating them internally.
**Example:** `OrderService(PaymentGateway pg)` receives the gateway via constructor instead of using `new PaymentGateway()` internally.
**Related:** Inversion of Control, Dependency Inversion Principle, Loose Coupling

### Dependency Inversion Principle (DIP)
**Definition:** The D in SOLID. High-level modules should not depend on low-level modules; both should depend on abstractions. Abstractions should not depend on details.
**Example:** `NotificationService` depends on `MessageSender` interface, not directly on `EmailSender` or `SmsSender`.
**Related:** SOLID, Dependency Injection, Inversion of Control, Loose Coupling

### Design Pattern
**Definition:** A reusable, proven solution to a commonly occurring problem in software design. Not code itself, but a template for solving a problem.
**Example:** Singleton, Observer, Factory are all design patterns documented by the Gang of Four.
**Related:** Anti-Pattern, Gang of Four, Refactoring

### Diamond Problem
**Definition:** An ambiguity that arises in multiple inheritance when a class inherits from two classes that both inherit from a common superclass.
**Example:** `D extends B, C` and both `B, C extend A`. Which version of `A`'s method does `D` inherit?
**Related:** Inheritance, Interface, Mixin, Virtual Inheritance

### DRY (Don't Repeat Yourself)
**Definition:** A principle stating that every piece of knowledge should have a single, unambiguous, authoritative representation in a system.
**Example:** Extracting duplicated validation logic into a shared `Validator` utility.
**Related:** KISS, YAGNI, Refactoring, Template Method

### Duck Typing
**Definition:** A concept where an object's suitability is determined by the presence of certain methods and properties, rather than its actual type.
**Example:** In Python, if an object has `quack()` and `walk()`, it can be treated as a Duck regardless of its class.
**Related:** Polymorphism, Dynamic Dispatch, Interface

### Dynamic Dispatch
**Definition:** The process of selecting which implementation of a polymorphic method to call at runtime rather than compile time.
**Example:** Calling `shape.area()` on a `Shape` reference invokes `Circle.area()` or `Rectangle.area()` depending on the actual runtime type.
**Related:** Polymorphism, Virtual Method, Late Binding, Overriding

---

## E

### Encapsulation
**Definition:** Bundling data (fields) and the methods that operate on that data within a single unit (class), and restricting direct access to some of the object's components.
**Example:** Private fields with public getters/setters: `private int balance; public int getBalance() { ... }`
**Related:** Abstraction, Information Hiding, Access Modifiers

### Extension
**Definition:** Adding new functionality to existing code without modifying it, often through inheritance, composition, or plugins.
**Example:** Adding a `PremiumMembership` class that extends `Membership` with extra features.
**Related:** Open-Closed Principle, Inheritance, Decorator

---

## F

### Facade Pattern
**Definition:** A structural pattern that provides a simplified, unified interface to a set of interfaces in a subsystem.
**Example:** `HomeTheaterFacade` wraps `DVDPlayer`, `Projector`, `SoundSystem`, and `Lights` behind a single `watchMovie()` method.
**Related:** Adapter, Mediator, Singleton, Proxy

### Factory Method
**Definition:** A creational pattern that defines an interface for creating an object but lets subclasses decide which class to instantiate.
**Example:** `Document.createPage()` where `PDFDocument` creates `PDFPage` and `HTMLDocument` creates `HTMLPage`.
**Related:** Abstract Factory, Template Method, Prototype

### Flyweight Pattern
**Definition:** A structural pattern that minimizes memory usage by sharing as much data as possible with similar objects.
**Example:** Sharing `CharacterFormat` objects in a text editor so each character doesn't store its own font/size.
**Related:** Singleton, Prototype, Composite, Caching

### Friend Class
**Definition:** A class that is granted access to the private and protected members of another class (C++ specific concept).
**Example:** `class Engine { friend class Mechanic; }` allows `Mechanic` to access `Engine`'s private parts.
**Related:** Encapsulation, Access Modifiers

---

## G

### Gang of Four (GoF)
**Definition:** The four authors (Gamma, Helm, Johnson, Vlissides) of "Design Patterns: Elements of Reusable Object-Oriented Software" (1994), the foundational book on design patterns.
**Example:** The book documents 23 classic design patterns categorized into Creational, Structural, and Behavioral.
**Related:** Design Pattern, Creational Pattern, Structural Pattern, Behavioral Pattern

### Generalization
**Definition:** The process of extracting shared characteristics from two or more classes and creating a common superclass. The inverse of specialization.
**Example:** Extracting `Vehicle` from `Car` and `Truck` classes.
**Related:** Inheritance, Specialization, Abstraction, Type Hierarchy

### GRASP (General Responsibility Assignment Software Patterns)
**Definition:** A set of nine principles for assigning responsibilities to classes and objects in OOD: Creator, Information Expert, Low Coupling, High Cohesion, Controller, Polymorphism, Pure Fabrication, Indirection, Protected Variations.
**Example:** The Information Expert principle says: assign a responsibility to the class that has the information needed to fulfill it.
**Related:** SOLID, Cohesion, Coupling, SRP

---

## H

### High Cohesion
**Definition:** A GRASP principle stating that a class should have a focused, well-defined purpose with all its methods working toward that single purpose.
**Example:** `InvoiceCalculator` only handles invoice math, not printing or emailing.
**Related:** Cohesion, SRP, GRASP, Low Coupling

### Hook Method
**Definition:** A method defined in a base class (often with a default or empty implementation) that subclasses can override to extend or modify behavior at specific points.
**Example:** In Template Method pattern: `void onBeforeSave() {}` that subclasses can optionally override.
**Related:** Template Method, Inheritance, Overriding

---

## I

### Immutability
**Definition:** The property of an object whose state cannot be modified after creation. All fields are set at construction time.
**Example:** Java's `String` class is immutable. `final class Money { final int amount; final String currency; }`
**Related:** Thread Safety, Builder Pattern, Value Object

### Inheritance
**Definition:** A mechanism where a new class (subclass) derives properties and behavior from an existing class (superclass), establishing an "is-a" relationship.
**Example:** `class Dog extends Animal` inherits `eat()` and `sleep()` methods.
**Related:** Composition, Polymorphism, Generalization, Diamond Problem, Overriding

### Inner Class
**Definition:** A class defined within another class. It has access to the enclosing class's members, including private ones.
**Example:** `class LinkedList { class Node { int data; Node next; } }`
**Related:** Encapsulation, Class, Nested Class

### Interface
**Definition:** A contract that defines a set of abstract methods that implementing classes must provide. Supports multiple inheritance of type.
**Example:** `interface Flyable { void fly(); }` implemented by `Bird` and `Airplane`.
**Related:** Abstract Class, Polymorphism, Interface Segregation, Duck Typing

### Interface Segregation Principle (ISP)
**Definition:** The I in SOLID. Clients should not be forced to depend on interfaces they do not use. Prefer many small, specific interfaces over one large interface.
**Example:** Split `Worker` into `Workable` and `Eatable` so `Robot` doesn't need to implement `eat()`.
**Related:** SOLID, SRP, Interface, Cohesion

### Inversion of Control (IoC)
**Definition:** A design principle where the control of object creation and lifecycle is transferred from the application code to a framework or container.
**Example:** Spring Framework creates and injects beans rather than the programmer calling `new`.
**Related:** Dependency Injection, Dependency Inversion, Hollywood Principle

### Iterator Pattern
**Definition:** A behavioral pattern that provides a way to access elements of a collection sequentially without exposing its underlying representation.
**Example:** Java's `Iterator<E>` interface with `hasNext()` and `next()` methods.
**Related:** Composite, Visitor, Collection

---

## K

### KISS (Keep It Simple, Stupid)
**Definition:** A design principle that states systems work best when kept simple rather than made complex. Avoid unnecessary complexity.
**Example:** Using a simple `HashMap` instead of building a custom caching framework for a small application.
**Related:** YAGNI, DRY, Over-Engineering

---

## L

### Late Binding
**Definition:** The process of resolving which method implementation to invoke at runtime rather than at compile time.
**Example:** In Java, calling `animal.speak()` resolves to `Dog.speak()` or `Cat.speak()` at runtime.
**Related:** Dynamic Dispatch, Polymorphism, Virtual Method

### Law of Demeter (LoD)
**Definition:** A design guideline that says an object should only talk to its immediate friends, not strangers. "Don't talk to strangers."
**Example:** Avoid: `order.getCustomer().getAddress().getCity()`. Prefer: `order.getShippingCity()`.
**Related:** Loose Coupling, Encapsulation, Delegation

### Liskov Substitution Principle (LSP)
**Definition:** The L in SOLID. Objects of a superclass should be replaceable with objects of a subclass without breaking the correctness of the program.
**Example:** If `Rectangle` has `setWidth()` and `setHeight()`, `Square` cannot be a valid subtype because setting width must also set height, breaking Rectangle's contract.
**Related:** SOLID, Inheritance, Polymorphism, Design by Contract

### Loose Coupling
**Definition:** A design goal where components have minimal dependencies on each other, making the system more flexible and maintainable.
**Example:** Classes depending on interfaces (`PaymentProcessor`) rather than concrete implementations (`StripePaymentProcessor`).
**Related:** Coupling, Dependency Injection, Dependency Inversion, Law of Demeter

### Low Coupling
**Definition:** A GRASP principle emphasizing that classes should have minimal dependencies on other classes, reducing the impact of changes.
**Example:** Using events/callbacks instead of direct method calls between unrelated classes.
**Related:** GRASP, Loose Coupling, High Cohesion, Observer

---

## M

### Mediator Pattern
**Definition:** A behavioral pattern that defines an object encapsulating how a set of objects interact, promoting loose coupling by keeping objects from referring to each other directly.
**Example:** A `ChatRoom` mediator that handles message routing between `User` objects.
**Related:** Observer, Facade, Command

### Memento Pattern
**Definition:** A behavioral pattern that captures and externalizes an object's internal state so it can be restored later without violating encapsulation.
**Example:** An `EditorMemento` saves cursor position, text content, and formatting for undo functionality.
**Related:** Command, Caretaker, Originator

### Method Overloading
**Definition:** Defining multiple methods with the same name but different parameter lists (different number, types, or order of parameters) within the same class.
**Example:** `add(int a, int b)` and `add(double a, double b)` in the same `Calculator` class.
**Related:** Method Overriding, Polymorphism (compile-time), Static Dispatch

### Method Overriding
**Definition:** Providing a specific implementation in a subclass for a method already defined in its superclass, with the same signature.
**Example:** `Dog.speak()` overrides `Animal.speak()` to return "Bark" instead of the default.
**Related:** Method Overloading, Polymorphism (runtime), Dynamic Dispatch, Virtual Method

### Mixin
**Definition:** A class that provides methods to other classes through multiple inheritance or composition without being a standalone base class. Provides reusable behavior.
**Example:** A `JsonSerializableMixin` that adds `toJson()` to any class that includes it.
**Related:** Interface, Trait, Multiple Inheritance, Composition

### MVC (Model-View-Controller)
**Definition:** An architectural pattern that separates an application into three components: Model (data/logic), View (presentation), and Controller (input handling).
**Example:** Web frameworks like Spring MVC, Ruby on Rails, Django use MVC.
**Related:** MVVM, MVP, Observer, Separation of Concerns

### MVVM (Model-View-ViewModel)
**Definition:** An architectural pattern similar to MVC but uses a ViewModel to handle view logic and data binding, common in UI-heavy applications.
**Example:** Android Jetpack's ViewModel, WPF with data binding.
**Related:** MVC, MVP, Observer, Data Binding

### Multiplicity
**Definition:** In UML, a notation that specifies the number of instances of one class that can be associated with one instance of another class.
**Example:** `1..*` means one or more, `0..1` means zero or one, `*` means many.
**Related:** Association, Aggregation, Composition, UML

---

## N

### Null Object Pattern
**Definition:** A behavioral pattern that uses an object with defined neutral ("null") behavior instead of using null references to represent absence.
**Example:** `NullLogger` implements `Logger` but does nothing, avoiding null checks: `if (logger != null)`.
**Related:** Strategy, Default Implementation, Special Case Pattern

---

## O

### Object
**Definition:** An instance of a class, having its own state (field values) and behavior (methods). The fundamental building block of OOP.
**Example:** `Car myCar = new Car("Red", 120);` -- `myCar` is an object.
**Related:** Class, Instantiation, Encapsulation

### Observer Pattern
**Definition:** A behavioral pattern where an object (subject) maintains a list of dependents (observers) and notifies them automatically of state changes.
**Example:** `StockPrice` notifies `StockDisplay` and `StockAlert` whenever the price changes.
**Related:** Mediator, Event-Driven, Publish-Subscribe, MVC

### Open-Closed Principle (OCP)
**Definition:** The O in SOLID. Software entities should be open for extension but closed for modification. Add new behavior without changing existing code.
**Example:** Adding a new `Shape` subclass (e.g., `Triangle`) instead of adding `if/else` branches in `AreaCalculator`.
**Related:** SOLID, Strategy, Decorator, Template Method, Polymorphism

### Overloading
**Definition:** See Method Overloading. Providing multiple versions of a method/operator with different parameter types in the same scope.
**Example:** `print(int)`, `print(String)`, `print(double)` in the same class.
**Related:** Method Overloading, Compile-time Polymorphism

### Overriding
**Definition:** See Method Overriding. Redefining a superclass method in a subclass with the same signature to provide specialized behavior.
**Example:** `toString()` overridden in a `Student` class to return "Student: John Doe".
**Related:** Method Overriding, Runtime Polymorphism, Virtual Method

---

## P

### Pattern
**Definition:** A general reusable solution to a commonly occurring problem within a given context in software design.
**Example:** The 23 GoF patterns, GRASP patterns, architectural patterns (MVC, Microservices).
**Related:** Design Pattern, Anti-Pattern, Gang of Four

### Polymorphism
**Definition:** The ability of different objects to respond to the same message (method call) in different ways. One of the four pillars of OOP.
**Example:** `shape.draw()` calls `Circle.draw()`, `Square.draw()`, or `Triangle.draw()` depending on the actual type.
**Related:** Inheritance, Overriding, Dynamic Dispatch, Interface

### Prototype Pattern
**Definition:** A creational pattern that creates new objects by cloning an existing object (the prototype) rather than constructing from scratch.
**Example:** `Cell newCell = existingCell.clone()` creates a copy with the same configuration.
**Related:** Abstract Factory, Factory Method, Memento, Clone

### Proxy Pattern
**Definition:** A structural pattern that provides a surrogate or placeholder for another object to control access to it.
**Example:** A `VirtualImageProxy` delays loading a large image until it's actually displayed.
**Related:** Decorator, Adapter, Facade, Lazy Loading

### Pure Virtual Function
**Definition:** A method declared in a base class with no implementation, forcing all subclasses to provide their own implementation (C++ term; Java uses `abstract` methods).
**Example:** `virtual void draw() = 0;` in C++ or `abstract void draw();` in Java.
**Related:** Abstract Class, Interface, Overriding

---

## R

### Realization
**Definition:** A UML relationship where a class implements the behavior specified by an interface or abstract class.
**Example:** `ArrayList` realizes the `List` interface. Shown as a dashed arrow in UML.
**Related:** Interface, Implementation, UML

### Refactoring
**Definition:** Restructuring existing code without changing its external behavior to improve readability, reduce complexity, or improve maintainability.
**Example:** Extract Method, Rename Variable, Replace Conditional with Polymorphism.
**Related:** Code Smell, Anti-Pattern, Design Pattern, DRY

### Responsibility
**Definition:** The obligation of a class or module to perform a specific task or know certain information. Central to SRP and GRASP.
**Example:** A `PaymentProcessor` is responsible for processing payments, not for sending emails.
**Related:** SRP, GRASP, Cohesion, Separation of Concerns

---

## S

### Separation of Concerns
**Definition:** A design principle that each module or class should address a separate concern or aspect of the system's functionality.
**Example:** Separating data access (Repository), business logic (Service), and presentation (Controller).
**Related:** SRP, MVC, Layered Architecture, Cohesion

### Sequence Diagram
**Definition:** A UML diagram showing how objects interact in a particular scenario, depicting the order of messages exchanged over time.
**Example:** A diagram showing the flow: User -> Controller -> Service -> Repository -> Database.
**Related:** UML, Class Diagram, Interaction Diagram

### Singleton Pattern
**Definition:** A creational pattern that ensures a class has exactly one instance and provides a global point of access to it.
**Example:** `DatabaseConnectionPool.getInstance()` returns the same pool everywhere.
**Related:** Factory, Facade, Thread Safety, Anti-Pattern (when overused)

### SOLID
**Definition:** An acronym for five design principles: Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.
**Example:** Following SOLID makes code more maintainable, testable, and extensible.
**Related:** SRP, OCP, LSP, ISP, DIP, Clean Code

### SRP (Single Responsibility Principle)
**Definition:** The S in SOLID. A class should have only one reason to change, meaning it should have only one job or responsibility.
**Example:** Splitting `UserService` into `UserAuthService`, `UserProfileService`, and `UserNotificationService`.
**Related:** SOLID, Cohesion, Separation of Concerns, GRASP

### State Pattern
**Definition:** A behavioral pattern that allows an object to alter its behavior when its internal state changes, as if the object changed its class.
**Example:** A `VendingMachine` with states: `IdleState`, `HasMoneyState`, `DispensingState`.
**Related:** Strategy, Finite State Machine, State Diagram

### State Diagram
**Definition:** A UML diagram showing the different states an object can be in and the transitions between those states triggered by events.
**Example:** An Order state diagram: Created -> Paid -> Shipped -> Delivered (or Cancelled).
**Related:** State Pattern, UML, Finite State Machine

### Strategy Pattern
**Definition:** A behavioral pattern that defines a family of algorithms, encapsulates each one, and makes them interchangeable at runtime.
**Example:** `SortStrategy` interface with `BubbleSort`, `QuickSort`, `MergeSort` implementations, selected at runtime.
**Related:** State, Template Method, Command, Bridge

### Structural Pattern
**Definition:** A category of design patterns concerned with how classes and objects are composed to form larger structures.
**Example:** Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy.
**Related:** Creational Pattern, Behavioral Pattern, Gang of Four

---

## T

### Template Method Pattern
**Definition:** A behavioral pattern that defines the skeleton of an algorithm in a base class, letting subclasses override specific steps without changing the overall structure.
**Example:** `DataParser` defines `parse()`: `readData()` -> `processData()` -> `writeOutput()`. Subclasses implement each step.
**Related:** Strategy, Hook Method, Factory Method, Inheritance

### Thread Safety
**Definition:** A property of code that ensures correct behavior when accessed from multiple threads simultaneously, without data corruption or race conditions.
**Example:** Using `synchronized` blocks, `volatile` fields, or `ConcurrentHashMap` in Java.
**Related:** Singleton, Immutability, Mutex, Race Condition, Deadlock

### Tight Coupling
**Definition:** A design flaw where components have strong dependencies on each other, making changes difficult and error-prone.
**Example:** `OrderService` directly creates `new EmailService()` internally instead of accepting it via dependency injection.
**Related:** Loose Coupling, Dependency Injection, Dependency Inversion

### Type Hierarchy
**Definition:** The tree-like structure formed by inheritance relationships, where more general types are at the top and more specific types are at the bottom.
**Example:** `Object` -> `Animal` -> `Mammal` -> `Dog` -> `GoldenRetriever`.
**Related:** Inheritance, Generalization, Specialization, Polymorphism

---

## U

### UML (Unified Modeling Language)
**Definition:** A standardized visual modeling language for specifying, visualizing, constructing, and documenting the artifacts of software systems.
**Example:** Class diagrams, Sequence diagrams, State diagrams, Use Case diagrams.
**Related:** Class Diagram, Sequence Diagram, State Diagram, Multiplicity

### Use Case
**Definition:** A description of how a user (actor) interacts with a system to achieve a specific goal. Captures functional requirements.
**Example:** "Customer places an order" use case describes steps from browsing to checkout.
**Related:** Use Case Diagram, UML, Actor, Scenario

---

## V

### Value Object
**Definition:** An object that is defined by its attributes rather than its identity. Two value objects with the same attributes are considered equal.
**Example:** `Money(100, "USD")` is equal to another `Money(100, "USD")` regardless of being different instances.
**Related:** Immutability, Entity, DDD

### Virtual Method
**Definition:** A method that can be overridden in a derived class, enabling runtime polymorphism. In Java, all non-static methods are virtual by default.
**Example:** `virtual void draw()` in C++ allows subclasses to provide custom drawing logic.
**Related:** Overriding, Dynamic Dispatch, Late Binding, Pure Virtual Function

### Visitor Pattern
**Definition:** A behavioral pattern that lets you add further operations to objects without modifying them, by separating the algorithm from the object structure.
**Example:** `TaxVisitor` visits `Book`, `Electronics`, `Food` items to compute tax differently for each.
**Related:** Composite, Iterator, Double Dispatch, Strategy

### Volatile
**Definition:** A keyword (in Java/C++) ensuring a variable's value is always read from main memory, not from a thread's local cache, ensuring visibility across threads.
**Example:** `volatile boolean isRunning = true;` ensures all threads see the updated value.
**Related:** Thread Safety, Singleton (double-checked locking), Concurrency

---

## W

### Wrapper
**Definition:** A general term for a class that "wraps" another class to alter or extend its behavior. Decorator, Adapter, and Proxy are all wrappers.
**Example:** `BufferedReader` wraps `FileReader` to add buffering.
**Related:** Decorator, Adapter, Proxy, Delegation

---

## Y

### YAGNI (You Aren't Gonna Need It)
**Definition:** A principle stating that you should not add functionality until it is actually needed, avoiding premature complexity.
**Example:** Don't build a plugin system for an app that currently needs only one behavior.
**Related:** KISS, DRY, Over-Engineering, Agile

---

## Quick Reference Index

| Term | Category | Primary Pattern/Principle |
|------|----------|--------------------------|
| Abstraction | OOP Pillar | Fundamental |
| Abstract Factory | Creational Pattern | GoF |
| Adapter | Structural Pattern | GoF |
| Bridge | Structural Pattern | GoF |
| Builder | Creational Pattern | GoF |
| Chain of Responsibility | Behavioral Pattern | GoF |
| Cohesion | Design Metric | GRASP |
| Command | Behavioral Pattern | GoF |
| Composite | Structural Pattern | GoF |
| Coupling | Design Metric | GRASP |
| Decorator | Structural Pattern | GoF |
| Dependency Injection | Technique | DIP |
| Encapsulation | OOP Pillar | Fundamental |
| Facade | Structural Pattern | GoF |
| Factory Method | Creational Pattern | GoF |
| Flyweight | Structural Pattern | GoF |
| Inheritance | OOP Pillar | Fundamental |
| Interface Segregation | SOLID Principle | ISP |
| Iterator | Behavioral Pattern | GoF |
| Liskov Substitution | SOLID Principle | LSP |
| Mediator | Behavioral Pattern | GoF |
| Memento | Behavioral Pattern | GoF |
| Observer | Behavioral Pattern | GoF |
| Open-Closed | SOLID Principle | OCP |
| Polymorphism | OOP Pillar | Fundamental |
| Prototype | Creational Pattern | GoF |
| Proxy | Structural Pattern | GoF |
| Singleton | Creational Pattern | GoF |
| SRP | SOLID Principle | SRP |
| State | Behavioral Pattern | GoF |
| Strategy | Behavioral Pattern | GoF |
| Template Method | Behavioral Pattern | GoF |
| Visitor | Behavioral Pattern | GoF |

---

*This glossary covers 100+ terms. For deeper dives into any concept, see the dedicated study material files in this repository.*
