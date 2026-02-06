# LLD Mini Problem Exercises

10 mini LLD problems designed as 15-minute exercises. Each focuses on identifying key classes, relationships, and design patterns.

---

## Problem 1: Task Management System (Trello-like)

### Requirements
- Users can create boards, each containing multiple lists
- Lists contain cards (tasks) that can be moved between lists
- Cards have title, description, due date, assignees, labels, and checklists
- Users can comment on cards
- Support drag-and-drop reordering within and across lists
- Activity history for all changes on a card

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- Board, List, Card — core domain objects
- User — with roles (owner, member, viewer)
- Comment — linked to card and user
- Label — reusable across cards
- Checklist and ChecklistItem — nested in card
- Activity — audit log entry

</details>

### Solution

```mermaid
classDiagram
    class User {
        -user_id: str
        -name: str
        -email: str
    }

    class Board {
        -board_id: str
        -title: str
        -owner: User
        -members: list~BoardMember~
        -lists: list~TaskList~
        +add_list(name: str): TaskList
        +add_member(user: User, role: Role)
    }

    class BoardMember {
        -user: User
        -role: Role
    }

    class TaskList {
        -list_id: str
        -name: str
        -position: int
        -cards: list~Card~
        +add_card(title: str): Card
        +move_card(card: Card, target_list: TaskList, position: int)
    }

    class Card {
        -card_id: str
        -title: str
        -description: str
        -due_date: datetime
        -position: int
        -assignees: list~User~
        -labels: list~Label~
        -checklists: list~Checklist~
        -comments: list~Comment~
        -activities: list~Activity~
        +assign(user: User)
        +add_label(label: Label)
        +add_comment(user: User, text: str)
    }

    class Label {
        -name: str
        -color: str
    }

    class Checklist {
        -title: str
        -items: list~ChecklistItem~
        +add_item(text: str)
        +completion_percentage(): float
    }

    class ChecklistItem {
        -text: str
        -is_done: bool
        +toggle()
    }

    class Comment {
        -author: User
        -text: str
        -created_at: datetime
    }

    class Activity {
        -user: User
        -action: str
        -timestamp: datetime
        -details: str
    }

    Board "1" --> "*" TaskList
    Board "1" --> "*" BoardMember
    TaskList "1" --> "*" Card
    Card --> "*" Label
    Card --> "*" Checklist
    Card --> "*" Comment
    Card --> "*" Activity
    Checklist --> "*" ChecklistItem
    BoardMember --> User
```

### Design Decisions
- **Composite potential:** Checklists within cards are a lightweight composite
- **Observer pattern:** Activity log acts as an observer, recording all card mutations
- **Position field:** Enables drag-and-drop reordering without restructuring the list
- **BoardMember vs User:** Separates user identity from board-specific role

---

## Problem 2: Playlist Manager

### Requirements
- Users can create, rename, and delete playlists
- Songs have title, artist, album, duration, and genre
- Playlists support add, remove, and reorder songs
- Play modes: sequential, shuffle, repeat-one, repeat-all
- Recently played history tracked per user
- Collaborative playlists (multiple editors)

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- Song, Artist, Album — core music entities
- Playlist — collection of songs with ordering
- PlaybackQueue — current playback state with mode
- PlayMode (Strategy) — shuffle, sequential, repeat
- PlayHistory — recently played songs

</details>

### Solution

```mermaid
classDiagram
    class Song {
        -song_id: str
        -title: str
        -artist: Artist
        -album: Album
        -duration_seconds: int
        -genre: str
    }

    class Artist {
        -artist_id: str
        -name: str
    }

    class Album {
        -album_id: str
        -title: str
        -artist: Artist
        -songs: list~Song~
        -release_year: int
    }

    class Playlist {
        -playlist_id: str
        -name: str
        -owner: User
        -collaborators: list~User~
        -songs: list~PlaylistEntry~
        -is_public: bool
        +add_song(song: Song)
        +remove_song(song: Song)
        +reorder(from_idx: int, to_idx: int)
        +total_duration(): int
    }

    class PlaylistEntry {
        -song: Song
        -position: int
        -added_by: User
        -added_at: datetime
    }

    class PlaybackQueue {
        -current_index: int
        -queue: list~Song~
        -mode: PlayMode
        +play_next(): Song
        +play_previous(): Song
        +set_mode(mode: PlayMode)
    }

    class PlayMode {
        <<interface>>
        +next_index(current: int, queue_size: int): int
        +previous_index(current: int, queue_size: int): int
    }

    class SequentialMode {
        +next_index(current, size): int
        +previous_index(current, size): int
    }

    class ShuffleMode {
        -order: list~int~
        +next_index(current, size): int
        +previous_index(current, size): int
    }

    class RepeatOneMode {
        +next_index(current, size): int
        +previous_index(current, size): int
    }

    class PlayHistory {
        -user: User
        -entries: list~HistoryEntry~
        +record(song: Song)
        +get_recent(n: int): list~Song~
    }

    Playlist "1" --> "*" PlaylistEntry
    PlaylistEntry --> Song
    Song --> Artist
    Album --> Artist
    Album "1" --> "*" Song
    PlaybackQueue --> PlayMode
    PlayMode <|.. SequentialMode
    PlayMode <|.. ShuffleMode
    PlayMode <|.. RepeatOneMode
    PlayHistory --> Song
```

### Design Decisions
- **Strategy pattern** for PlayMode: Easily swap playback behavior
- **PlaylistEntry** wraps Song with metadata (position, who added it, when)
- **PlaybackQueue** is separate from Playlist — a queue is ephemeral runtime state
- **PlayHistory** is per-user, decoupled from playback logic

---

## Problem 3: Stack Overflow (Q&A Platform)

### Requirements
- Users can post questions with tags and descriptions
- Other users post answers; one answer can be accepted
- Voting (upvote/downvote) on questions and answers
- Users earn reputation based on votes
- Tags for categorization with search support
- Comments on questions and answers

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- Question, Answer — core content types
- User — with reputation system
- Vote — tracks who voted on what
- Tag — shared across questions
- Comment — attached to questions or answers
- Votable (interface) — shared between Question and Answer

</details>

### Solution

```mermaid
classDiagram
    class User {
        -user_id: str
        -username: str
        -reputation: int
        +ask_question(title, body, tags): Question
        +post_answer(question, body): Answer
        +vote(votable: Votable, is_upvote: bool)
        +update_reputation(delta: int)
    }

    class Votable {
        <<interface>>
        +get_vote_count(): int
        +add_vote(vote: Vote)
    }

    class Question {
        -question_id: str
        -title: str
        -body: str
        -author: User
        -tags: list~Tag~
        -answers: list~Answer~
        -accepted_answer: Answer
        -comments: list~Comment~
        -created_at: datetime
        +accept_answer(answer: Answer)
        +add_answer(answer: Answer)
        +get_vote_count(): int
    }

    class Answer {
        -answer_id: str
        -body: str
        -author: User
        -is_accepted: bool
        -comments: list~Comment~
        -created_at: datetime
        +get_vote_count(): int
    }

    class Vote {
        -voter: User
        -is_upvote: bool
        -created_at: datetime
    }

    class Tag {
        -name: str
        -description: str
        -question_count: int
    }

    class Comment {
        -author: User
        -text: str
        -created_at: datetime
    }

    Votable <|.. Question
    Votable <|.. Answer
    Question --> User : author
    Answer --> User : author
    Question "1" --> "*" Answer
    Question --> "*" Tag
    Question --> "*" Vote
    Answer --> "*" Vote
    Question --> "*" Comment
    Answer --> "*" Comment
```

### Design Decisions
- **Votable interface:** Both Question and Answer share voting behavior (ISP)
- **Reputation is derived:** Upvotes on your content increase rep (+10 for question, +15 for answer accepted)
- **Accepted answer** is a single reference on Question, not a flag on all answers
- **Observer pattern opportunity:** Notify question author when a new answer is posted

### Applicable Patterns
- **Observer:** Notify on new answers, votes, comments
- **Strategy:** Ranking algorithms for answers (by votes, by date, by acceptance)
- **Template Method:** Common voting logic shared between Question and Answer

---

## Problem 4: Food Delivery System

### Requirements
- Restaurants register with menus containing items and prices
- Customers browse restaurants, add items to cart, place orders
- Orders go through status changes: placed, confirmed, preparing, picked up, delivered
- Delivery agents assigned to orders based on location
- Rating system for restaurants and delivery agents
- Estimated delivery time calculation

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- Restaurant, Menu, MenuItem — food catalog
- Customer, DeliveryAgent — user types
- Cart, CartItem — pre-order state
- Order, OrderItem — placed order
- OrderStatus (State pattern) — lifecycle
- Rating — shared across restaurants and agents

</details>

### Solution

```mermaid
classDiagram
    class Restaurant {
        -restaurant_id: str
        -name: str
        -address: Address
        -menu: Menu
        -rating: float
        -is_open: bool
        +update_menu(menu: Menu)
    }

    class Menu {
        -categories: list~MenuCategory~
        +get_item(item_id: str): MenuItem
    }

    class MenuItem {
        -item_id: str
        -name: str
        -price: float
        -description: str
        -is_available: bool
    }

    class Customer {
        -customer_id: str
        -name: str
        -addresses: list~Address~
        -cart: Cart
        +place_order(): Order
    }

    class Cart {
        -customer: Customer
        -restaurant: Restaurant
        -items: list~CartItem~
        +add_item(item: MenuItem, qty: int)
        +remove_item(item_id: str)
        +get_total(): float
        +clear()
    }

    class CartItem {
        -menu_item: MenuItem
        -quantity: int
        -special_instructions: str
    }

    class Order {
        -order_id: str
        -customer: Customer
        -restaurant: Restaurant
        -items: list~OrderItem~
        -status: OrderStatus
        -delivery_agent: DeliveryAgent
        -delivery_address: Address
        -total_amount: float
        -created_at: datetime
        +update_status(status: OrderStatus)
        +assign_agent(agent: DeliveryAgent)
    }

    class OrderStatus {
        <<enumeration>>
        PLACED
        CONFIRMED
        PREPARING
        READY
        PICKED_UP
        DELIVERED
        CANCELLED
    }

    class DeliveryAgent {
        -agent_id: str
        -name: str
        -current_location: Location
        -is_available: bool
        -rating: float
        +accept_order(order: Order)
        +update_location(location: Location)
    }

    class Rating {
        -rater: Customer
        -score: int
        -review: str
        -created_at: datetime
    }

    Restaurant "1" --> "1" Menu
    Menu "1" --> "*" MenuItem
    Customer "1" --> "1" Cart
    Cart --> Restaurant
    Cart "1" --> "*" CartItem
    CartItem --> MenuItem
    Order --> Customer
    Order --> Restaurant
    Order --> DeliveryAgent
    Restaurant --> "*" Rating
    DeliveryAgent --> "*" Rating
```

### Design Decisions
- **Cart is per-customer, single-restaurant:** Simplifies ordering; clear on checkout
- **State pattern** for OrderStatus: Each state defines valid transitions
- **Strategy pattern** for agent assignment: Nearest agent, round-robin, load-balanced
- **Observer pattern:** Notify customer on status changes, notify agent on new orders

---

## Problem 5: Splitwise (Expense Sharing)

### Requirements
- Users create groups with members
- Members add expenses with amounts and who paid
- Split types: equal, exact amounts, percentage-based
- Track balances between every pair of users
- Simplify debts (minimize number of transactions to settle)
- Transaction history and settlement tracking

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- User — with balance tracking
- Group — collection of users
- Expense — who paid, how much, how to split
- SplitStrategy (Strategy pattern) — equal, exact, percentage
- Balance — tracks net amounts between user pairs
- Settlement — records debt payments

</details>

### Solution

```mermaid
classDiagram
    class User {
        -user_id: str
        -name: str
        -email: str
        -balances: dict~str, float~
        +get_balance_with(user: User): float
        +get_total_owed(): float
    }

    class Group {
        -group_id: str
        -name: str
        -members: list~User~
        -expenses: list~Expense~
        +add_expense(expense: Expense)
        +get_balances(): dict
        +simplify_debts(): list~Settlement~
    }

    class Expense {
        -expense_id: str
        -description: str
        -amount: float
        -paid_by: User
        -group: Group
        -split_strategy: SplitStrategy
        -participants: list~User~
        -created_at: datetime
        +get_shares(): dict~User, float~
    }

    class SplitStrategy {
        <<interface>>
        +calculate_shares(amount: float, participants: list~User~): dict~User, float~
    }

    class EqualSplit {
        +calculate_shares(amount, participants): dict
    }

    class ExactSplit {
        -amounts: dict~User, float~
        +calculate_shares(amount, participants): dict
    }

    class PercentageSplit {
        -percentages: dict~User, float~
        +calculate_shares(amount, participants): dict
    }

    class Balance {
        -from_user: User
        -to_user: User
        -amount: float
    }

    class Settlement {
        -from_user: User
        -to_user: User
        -amount: float
        -settled_at: datetime
        +settle()
    }

    Group "1" --> "*" User
    Group "1" --> "*" Expense
    Expense --> SplitStrategy
    Expense --> User : paid_by
    SplitStrategy <|.. EqualSplit
    SplitStrategy <|.. ExactSplit
    SplitStrategy <|.. PercentageSplit
    Group --> "*" Balance
```

### Design Decisions
- **Strategy pattern** for split types: Each split algorithm is interchangeable
- **Balance simplification:** Use a greedy algorithm — find max creditor and max debtor, settle between them, repeat
- **Expense stores split strategy:** Each expense can have a different split approach
- **Group-scoped balances:** Balances are tracked per group to avoid cross-group confusion

---

## Problem 6: Calendar Application

### Requirements
- Users create events with title, time, location, and attendees
- Support recurring events (daily, weekly, monthly, custom)
- Reminders at configurable times before events
- Conflict detection for overlapping events
- Multiple calendars per user (work, personal)
- RSVP for event invitations (accept, decline, tentative)

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- Calendar, Event — core entities
- RecurrenceRule — defines repeat pattern
- Reminder — notification before event
- Invitation — RSVP tracking
- TimeSlot — for conflict detection

</details>

### Solution

```mermaid
classDiagram
    class User {
        -user_id: str
        -name: str
        -calendars: list~Calendar~
        +get_events_for_date(date): list~Event~
        +check_conflicts(start, end): list~Event~
    }

    class Calendar {
        -calendar_id: str
        -name: str
        -color: str
        -owner: User
        -events: list~Event~
        +add_event(event: Event)
        +get_events_in_range(start, end): list~Event~
    }

    class Event {
        -event_id: str
        -title: str
        -description: str
        -start_time: datetime
        -end_time: datetime
        -location: str
        -organizer: User
        -invitations: list~Invitation~
        -reminders: list~Reminder~
        -recurrence: RecurrenceRule
        +is_recurring(): bool
        +get_occurrences(start, end): list~datetime~
    }

    class RecurrenceRule {
        -frequency: Frequency
        -interval: int
        -end_date: datetime
        -days_of_week: list~int~
        -count: int
        +get_dates(start, end): list~datetime~
    }

    class Frequency {
        <<enumeration>>
        DAILY
        WEEKLY
        MONTHLY
        YEARLY
    }

    class Invitation {
        -event: Event
        -invitee: User
        -status: RSVPStatus
        +respond(status: RSVPStatus)
    }

    class RSVPStatus {
        <<enumeration>>
        PENDING
        ACCEPTED
        DECLINED
        TENTATIVE
    }

    class Reminder {
        -minutes_before: int
        -type: ReminderType
        +should_trigger(current_time: datetime): bool
    }

    User "1" --> "*" Calendar
    Calendar "1" --> "*" Event
    Event --> RecurrenceRule
    Event "1" --> "*" Invitation
    Event "1" --> "*" Reminder
    Invitation --> User
```

### Applicable Patterns
- **Strategy:** Different recurrence rules (daily, weekly, custom)
- **Observer:** Notify attendees on event changes, trigger reminders
- **Iterator:** Iterate over recurring event occurrences

---

## Problem 7: File System

### Requirements
- Files have name, size, content, and permissions
- Folders can contain files or other folders (nested)
- Permissions: read, write, execute for owner/group/others
- Search by name, extension, or size
- Calculate total size of a folder (recursive)
- Copy, move, delete operations

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- FileSystemNode (abstract) — shared interface
- File, Folder — composite pattern
- Permission — read/write/execute
- SearchCriteria — for flexible file search

</details>

### Solution

```mermaid
classDiagram
    class FileSystemNode {
        <<abstract>>
        -name: str
        -created_at: datetime
        -modified_at: datetime
        -parent: Folder
        -permissions: Permission
        +get_size(): int*
        +get_path(): str
        +delete()
        +move(target: Folder)
        +copy(target: Folder): FileSystemNode
    }

    class File {
        -content: bytes
        -extension: str
        +get_size(): int
        +read(): bytes
        +write(content: bytes)
    }

    class Folder {
        -children: list~FileSystemNode~
        +get_size(): int
        +add(node: FileSystemNode)
        +remove(node: FileSystemNode)
        +list_contents(): list~FileSystemNode~
        +search(criteria: SearchCriteria): list~FileSystemNode~
    }

    class Permission {
        -owner_read: bool
        -owner_write: bool
        -owner_execute: bool
        -group_read: bool
        -group_write: bool
        -group_execute: bool
        +can_read(user: User): bool
        +can_write(user: User): bool
    }

    class SearchCriteria {
        <<interface>>
        +matches(node: FileSystemNode): bool
    }

    class NameSearch {
        -pattern: str
        +matches(node): bool
    }

    class ExtensionSearch {
        -extension: str
        +matches(node): bool
    }

    class SizeSearch {
        -min_size: int
        -max_size: int
        +matches(node): bool
    }

    FileSystemNode <|-- File
    FileSystemNode <|-- Folder
    Folder "1" --> "*" FileSystemNode
    FileSystemNode --> Permission
    SearchCriteria <|.. NameSearch
    SearchCriteria <|.. ExtensionSearch
    SearchCriteria <|.. SizeSearch
```

### Applicable Patterns
- **Composite:** File and Folder share interface; Folder contains children
- **Strategy:** SearchCriteria implementations for flexible search
- **Visitor:** Could traverse the tree applying operations (size calc, permission check)

---

## Problem 8: URL Shortener

### Requirements
- Generate short URLs from long URLs
- Redirect short URL to original long URL
- Track click analytics (count, referrer, geo, timestamp)
- Custom aliases (user-defined short codes)
- URL expiration after a configurable TTL
- Rate limiting for URL creation

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- URL (ShortURL) — maps short code to long URL
- URLEncoder — generates short codes (Strategy)
- ClickEvent — analytics per click
- RateLimiter — limits creation frequency
- ExpirationPolicy — TTL management

</details>

### Solution

```mermaid
classDiagram
    class URLService {
        -repository: URLRepository
        -encoder: URLEncoder
        -rate_limiter: RateLimiter
        +shorten(long_url: str, custom_alias: str, ttl: int): ShortURL
        +resolve(short_code: str): str
        +get_analytics(short_code: str): URLAnalytics
    }

    class ShortURL {
        -short_code: str
        -long_url: str
        -created_by: User
        -created_at: datetime
        -expires_at: datetime
        -is_active: bool
        +is_expired(): bool
    }

    class URLEncoder {
        <<interface>>
        +encode(url_id: int): str
        +decode(short_code: str): int
    }

    class Base62Encoder {
        +encode(url_id): str
        +decode(short_code): int
    }

    class HashEncoder {
        +encode(url_id): str
        +decode(short_code): int
    }

    class ClickEvent {
        -short_url: ShortURL
        -timestamp: datetime
        -ip_address: str
        -user_agent: str
        -referrer: str
        -country: str
    }

    class URLAnalytics {
        -short_url: ShortURL
        -total_clicks: int
        -clicks_by_date: dict
        -clicks_by_country: dict
        -top_referrers: list
        +get_summary(): dict
    }

    class URLRepository {
        <<interface>>
        +save(url: ShortURL)
        +find_by_code(code: str): ShortURL
        +record_click(event: ClickEvent)
    }

    class RateLimiter {
        <<interface>>
        +is_allowed(user_id: str): bool
    }

    URLService --> URLRepository
    URLService --> URLEncoder
    URLService --> RateLimiter
    URLEncoder <|.. Base62Encoder
    URLEncoder <|.. HashEncoder
    ShortURL "1" --> "*" ClickEvent
    URLAnalytics --> ShortURL
```

### Design Decisions
- **Strategy for encoding:** Base62 (compact) vs. hash-based (unpredictable)
- **Repository abstraction:** Switch between Redis, SQL, NoSQL
- **ClickEvent is append-only:** High write throughput for analytics
- **Rate limiter as dependency:** Can swap token bucket, sliding window, etc.

---

## Problem 9: Logging Framework

### Requirements
- Log messages at levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Multiple output destinations: console, file, database, remote server
- Configurable log format (timestamp, level, message, source)
- Log filtering by level threshold
- Support for structured logging (key-value pairs)
- Log rotation for file-based logging

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- Logger — main entry point
- LogHandler (abstract) — output destinations
- LogFormatter — controls output format
- LogLevel — enumeration with ordering
- LogRecord — single log entry
- LogFilter — determines if a record should be processed

</details>

### Solution

```mermaid
classDiagram
    class Logger {
        -name: str
        -handlers: list~LogHandler~
        -level: LogLevel
        +debug(message: str, **kwargs)
        +info(message: str, **kwargs)
        +warning(message: str, **kwargs)
        +error(message: str, **kwargs)
        +critical(message: str, **kwargs)
        +add_handler(handler: LogHandler)
        +set_level(level: LogLevel)
    }

    class LogRecord {
        -timestamp: datetime
        -level: LogLevel
        -message: str
        -logger_name: str
        -extra: dict
    }

    class LogLevel {
        <<enumeration>>
        DEBUG = 10
        INFO = 20
        WARNING = 30
        ERROR = 40
        CRITICAL = 50
    }

    class LogHandler {
        <<abstract>>
        -level: LogLevel
        -formatter: LogFormatter
        -filters: list~LogFilter~
        +handle(record: LogRecord)
        +emit(record: LogRecord)*
    }

    class ConsoleHandler {
        +emit(record: LogRecord)
    }

    class FileHandler {
        -filepath: str
        -max_bytes: int
        -backup_count: int
        +emit(record: LogRecord)
        +rotate()
    }

    class DatabaseHandler {
        -connection: DBConnection
        +emit(record: LogRecord)
    }

    class LogFormatter {
        <<interface>>
        +format(record: LogRecord): str
    }

    class SimpleFormatter {
        -pattern: str
        +format(record): str
    }

    class JSONFormatter {
        +format(record): str
    }

    class LogFilter {
        <<interface>>
        +should_log(record: LogRecord): bool
    }

    class LevelFilter {
        -min_level: LogLevel
        +should_log(record): bool
    }

    Logger "1" --> "*" LogHandler
    LogHandler --> LogFormatter
    LogHandler --> "*" LogFilter
    LogHandler <|-- ConsoleHandler
    LogHandler <|-- FileHandler
    LogHandler <|-- DatabaseHandler
    LogFormatter <|.. SimpleFormatter
    LogFormatter <|.. JSONFormatter
    LogFilter <|.. LevelFilter
```

### Applicable Patterns
- **Chain of Responsibility:** Logger hierarchy (child -> parent propagation)
- **Strategy:** Formatters and filters are interchangeable strategies
- **Observer:** Handlers are observers of log events
- **Template Method:** LogHandler.handle() does filtering, then calls abstract emit()

---

## Problem 10: Rate Limiter

### Requirements
- Limit API requests per user/IP to a configured threshold
- Support multiple algorithms: token bucket, sliding window, fixed window
- Configurable limits per API endpoint
- Return remaining quota information in responses
- Distributed rate limiting across multiple servers
- Graceful handling when limit is exceeded (return 429 with retry-after)

### Key Classes to Identify
<details>
<summary>Click to reveal hints</summary>

- RateLimiter (interface) — check if request is allowed
- TokenBucketLimiter — refills tokens at fixed rate
- SlidingWindowLimiter — counts requests in rolling window
- FixedWindowLimiter — counts per fixed time window
- RateLimitConfig — per-endpoint configuration
- RateLimitResult — allowed/denied with metadata

</details>

### Solution

```mermaid
classDiagram
    class RateLimiter {
        <<interface>>
        +is_allowed(key: str): RateLimitResult
    }

    class TokenBucketLimiter {
        -max_tokens: int
        -refill_rate: float
        -buckets: dict~str, Bucket~
        +is_allowed(key: str): RateLimitResult
    }

    class SlidingWindowLimiter {
        -window_size_ms: int
        -max_requests: int
        -requests: dict~str, list~int~~
        +is_allowed(key: str): RateLimitResult
    }

    class FixedWindowLimiter {
        -window_size_ms: int
        -max_requests: int
        -windows: dict~str, WindowCounter~
        +is_allowed(key: str): RateLimitResult
    }

    class RateLimitResult {
        -allowed: bool
        -remaining: int
        -retry_after_ms: int
        -limit: int
    }

    class RateLimitConfig {
        -endpoint: str
        -requests_per_window: int
        -window_size_ms: int
        -algorithm: str
    }

    class Bucket {
        -tokens: float
        -last_refill: int
        -max_tokens: int
        -refill_rate: float
        +consume(): bool
        +refill()
    }

    class RateLimitMiddleware {
        -config: dict~str, RateLimitConfig~
        -limiters: dict~str, RateLimiter~
        +handle_request(endpoint: str, client_key: str): RateLimitResult
    }

    RateLimiter <|.. TokenBucketLimiter
    RateLimiter <|.. SlidingWindowLimiter
    RateLimiter <|.. FixedWindowLimiter
    TokenBucketLimiter --> Bucket
    RateLimitMiddleware --> RateLimiter
    RateLimitMiddleware --> RateLimitConfig
```

### Design Decisions
- **Strategy pattern:** Swap algorithms per endpoint without changing middleware
- **RateLimitResult:** Rich response object includes remaining quota and retry hint
- **Key-based limiting:** Same algorithm, different keys (user ID, IP, API key)
- **Distributed extension:** Replace in-memory dict with Redis for multi-server support

### Algorithm Comparison

| Algorithm | Pros | Cons |
|-----------|------|------|
| Token Bucket | Smooth, allows bursts | Memory per bucket |
| Sliding Window | Accurate, no boundary issues | More memory (stores timestamps) |
| Fixed Window | Simple, low memory | Allows 2x burst at window boundary |
