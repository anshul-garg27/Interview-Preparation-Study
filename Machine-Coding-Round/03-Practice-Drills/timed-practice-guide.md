# Timed Practice Guide for Machine Coding Rounds

## How to Use This Guide

Machine coding rounds are as much about **time management** as they are about code quality.
This guide gives you a structured practice plan to build speed and confidence.

### Practice Philosophy
```
Week 1-2: Solve problems in 2.5 hours (comfort zone)
Week 3-4: Solve problems in 2 hours (building speed)
Week 5-6: Solve problems in 90 minutes (interview speed)
Week 7+:  Solve problems in 75 minutes (with buffer)
```

---

## 10 Timed Practice Problems

### Problem 1: Parking Lot System
**Difficulty**: Easy | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Multiple floors with parking spots of different sizes
- Vehicle types: Car, Bike, Truck
- Park a vehicle (assign to nearest available spot)
- Unpark a vehicle
- Check availability by floor
- Search vehicle by registration number

Key Patterns: Factory (vehicle types), Strategy (spot allocation)
Entities: ParkingLot, Floor, ParkingSpot, Vehicle, Ticket
```

**Success Criteria**: All 4 operations work, clean Vehicle hierarchy, formatted output.

---

### Problem 2: Splitwise / Expense Sharing
**Difficulty**: Easy-Medium | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Add users to the system
- Add expenses: EQUAL, EXACT, or PERCENTAGE split
- Show balances (who owes whom)
- Simplify debts (minimize transactions)

Key Patterns: Strategy (split types), Observer (balance updates)
Entities: User, Expense, Split, Balance
```

**Success Criteria**: All 3 split types work, balances are correct, simplification works.

---

### Problem 3: Task Management System (Trello-like)
**Difficulty**: Medium | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Create boards, lists, and cards
- Move cards between lists
- Assign members to cards
- Add labels and due dates
- Show board state

Key Patterns: Composite (board > list > card), State (card status)
Entities: Board, TaskList, Card, User, Label
```

**Success Criteria**: Cards can be created, moved, and assigned. Board display is clear.

---

### Problem 4: Library Management System
**Difficulty**: Easy-Medium | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Add books (with multiple copies)
- Register members
- Issue and return books
- Search by title, author, or subject
- Track overdue books with fines

Key Patterns: State (book status), Strategy (fine calculation)
Entities: Book, BookCopy, Member, Loan, Fine
```

**Success Criteria**: Issue/return cycle works, search returns correct results, fines calculated.

---

### Problem 5: Ride Sharing / Cab Booking
**Difficulty**: Medium | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Register riders and drivers
- Request a ride (source, destination)
- Match with nearest available driver
- Calculate fare (different vehicle types)
- Complete/cancel trip
- Show trip history

Key Patterns: Strategy (fare calculation), State (trip lifecycle)
Entities: User, Driver, Rider, Trip, Vehicle, Location
```

**Success Criteria**: Ride request + matching works, fare calculated correctly, trip history displayed.

---

### Problem 6: Snake and Ladder
**Difficulty**: Medium | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Configurable board size
- Add snakes (head, tail) and ladders (start, end)
- Support 2-4 players
- Dice roll, move player, handle snakes/ladders
- Detect winner
- Show board state

Key Patterns: State (game state), Command (moves)
Entities: Board, Player, Snake, Ladder, Dice, Game
```

**Success Criteria**: Full game can be played, snakes/ladders work, winner detected.

---

### Problem 7: Inventory Management System
**Difficulty**: Medium | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Add products with SKU, name, price, quantity
- Restock and sell products
- Track inventory levels
- Low stock alerts (configurable threshold)
- Generate inventory report
- Support categories and suppliers

Key Patterns: Observer (low stock alerts), Strategy (restock policies)
Entities: Product, Category, Supplier, StockEntry, Alert
```

**Success Criteria**: Buy/sell updates stock correctly, alerts fire, report is accurate.

---

### Problem 8: Movie Ticket Booking (BookMyShow-like)
**Difficulty**: Medium-Hard | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Add theaters with screens and seats
- Add movie shows (movie + screen + time)
- Search shows by movie, city, or theater
- Book seats (select specific seats)
- Cancel booking
- Show seat availability map

Key Patterns: Strategy (pricing by seat type), State (seat availability)
Entities: Theater, Screen, Seat, Movie, Show, Booking
```

**Success Criteria**: Seat selection works, double-booking prevented, availability map displayed.

---

### Problem 9: Rate Limiter
**Difficulty**: Medium-Hard | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Support multiple algorithms: Token Bucket, Sliding Window, Fixed Window
- Configure rate limits per user/API
- Check if request is allowed
- Track and display usage statistics
- Support different time windows

Key Patterns: Strategy (algorithm types), Factory (limiter creation)
Entities: RateLimiter, TokenBucket, SlidingWindow, FixedWindow, RateLimitConfig, RequestLog
```

**Success Criteria**: At least 2 algorithms work, rate limiting is accurate, stats are tracked.

---

### Problem 10: Event Calendar
**Difficulty**: Medium-Hard | **Target Time**: 90 min | **Warm-up Time**: 120 min

```
Requirements:
- Create events (title, start, end, location, attendees)
- Detect scheduling conflicts
- Recurring events (daily, weekly, monthly)
- RSVP (accept, decline, tentative)
- View calendar for a day/week
- Send reminders

Key Patterns: Observer (reminders), Strategy (recurrence rules), State (RSVP status)
Entities: Event, RecurringEvent, Calendar, User, RSVP, Reminder
```

**Success Criteria**: Events created, conflicts detected, recurring events expand correctly.

---

## Progressive Practice Schedule

### Week 1-2: Foundation (2.5 hours per problem)
```
Day 1: Problem 1 (Parking Lot) - 150 min
Day 3: Problem 2 (Splitwise) - 150 min
Day 5: Problem 4 (Library) - 150 min

Focus: Getting comfortable with the template, file structure, enums.
Goal: Complete all features. Don't worry about speed.
```

### Week 3-4: Building Speed (2 hours per problem)
```
Day 1: Problem 3 (Task Management) - 120 min
Day 3: Problem 5 (Ride Sharing) - 120 min
Day 5: Problem 6 (Snake & Ladder) - 120 min

Focus: Faster model creation, quicker service implementation.
Goal: Complete core features within 60 min, remaining in next 60.
```

### Week 5-6: Interview Speed (90 minutes per problem)
```
Day 1: Problem 7 (Inventory) - 90 min
Day 3: Problem 8 (Movie Booking) - 90 min
Day 5: Problem 9 (Rate Limiter) - 90 min

Focus: Time management, knowing when to skip features.
Goal: Working demo by minute 75. Accept partial feature coverage.
```

### Week 7+: Competition Mode (75 minutes per problem)
```
Day 1: Redo Problem 1 (Parking Lot) - 75 min
Day 3: Redo Problem 5 (Ride Sharing) - 75 min
Day 5: Problem 10 (Event Calendar) - 75 min

Focus: Speed + quality. This is faster than interviews; builds buffer.
Goal: If you can do it in 75 min, 90 min will feel comfortable.
```

---

## Self-Evaluation Checklist

### After Each Practice Session, Score Yourself (1-5)

```
EXECUTION
[ ] Code runs without errors                           ___/5
[ ] All core features produce correct output            ___/5
[ ] Demo function exercises all implemented features    ___/5

CODE QUALITY
[ ] Separate classes for separate concerns              ___/5
[ ] Enums used for all constants                        ___/5
[ ] Meaningful variable and method names                ___/5
[ ] No code duplication                                 ___/5

DESIGN
[ ] At least one design pattern used appropriately      ___/5
[ ] Easy to add a new entity type without modifying     ___/5
    existing code
[ ] Service layer separate from data models             ___/5

ROBUSTNESS
[ ] Invalid inputs handled with error messages          ___/5
[ ] No crashes on edge cases (empty lists, null, etc.)  ___/5

TIME MANAGEMENT
[ ] Started coding within 15 minutes of reading problem ___/5
[ ] Core feature working by halfway point               ___/5
[ ] Had a running demo with at least 10 minutes to spare___/5

TOTAL                                                   ___/75
```

### Score Interpretation
```
60-75:  Interview-ready. You'd pass most machine coding rounds.
45-59:  Getting close. Focus on weaker areas.
30-44:  Need more practice. Speed and structure need work.
<30:    Start with easier problems and longer time limits.
```

---

## Practice Tips

### Practicing Alone
1. **Use a timer religiously** - Set phone timer, visible on desk
2. **No looking up code** during the timed session (have patterns memorized)
3. **Record yourself** (screen recording) and review afterward
4. **Keep a mistake journal** - What went wrong? How to avoid it?
5. **Practice the template first** - Be able to create file structure in < 2 minutes
6. **Do multiple rounds on the same problem** - First solve it, then optimize for time

### Practicing With a Partner
1. **Take turns being interviewer** - One codes, other observes
2. **Interviewer gives problem and asks questions** during post-coding
3. **Interviewer notes**:
   - Time spent on each phase
   - Design decisions (good and bad)
   - Code smells
   - Missing error handling
4. **Debrief together** - Discuss what went well and what to improve
5. **Exchange solutions** - Compare approaches to the same problem

### Setting Up Your Practice Environment
```
Before you start:
1. Create a fresh directory for each practice session
2. Have your template files ready to copy
3. Set a visible countdown timer
4. Close all distractions (Slack, email, social media)
5. Have the problem statement printed or on a separate screen

During:
1. Write notes on paper (entities, relationships, priorities)
2. Create file structure first
3. Follow the 90-minute framework phase by phase
4. If stuck > 10 min, move on with a TODO comment

After:
1. Run the code and note any bugs
2. Fill in the self-evaluation checklist
3. Note what took longer than expected
4. Identify patterns you need to practice more
5. Compare with a reference solution (if available)
```

---

## Common Bottlenecks and How to Fix Them

### "I spend too much time on models"
**Fix**: Practice creating data classes until it's muscle memory. You should be able to
write a class with id, fields, str, and constructor in under 2 minutes.

### "I get stuck on the service layer"
**Fix**: Start with the simplest implementation. Return hardcoded values, then iterate.
A method that returns a dummy result is better than an empty method.

### "I forget error handling"
**Fix**: Add validation at the TOP of every service method before writing logic:
```python
def do_something(self, entity_id, param):
    entity = self._repo.find(entity_id)
    if not entity:
        print(f"[ERROR] Entity not found: {entity_id}")
        return None
    if not param:
        print(f"[ERROR] Parameter is required")
        return None
    # ... actual logic
```

### "My output is ugly"
**Fix**: Have a reusable OutputFormatter ready. Copy it from the template.
Spend 5 minutes on formatting; it makes a big impression.

### "I run out of time for the demo"
**Fix**: Write demo.py FIRST with placeholder service calls.
Fill in the service implementation to make the demo work.
This way, even if you run out of time, the demo structure is there.

### "I don't know which pattern to use"
**Fix**: Memorize this decision tree:
```
Multiple types of the same thing? → Strategy/Factory
Entity has lifecycle states?      → State pattern
One action triggers many effects? → Observer
Need to undo actions?             → Command
Creating objects of varying types? → Factory
```

---

## Tracking Your Progress

### Practice Log Template
```
Date:     ___________
Problem:  ___________
Time:     ___ minutes (target: ___ minutes)
Features: ___ / ___ completed
Score:    ___ / 75

What went well:
-
-

What to improve:
-
-

Patterns used:
-
-

Time breakdown:
  Planning:    ___ min
  Models:      ___ min
  Core logic:  ___ min
  Extra feat:  ___ min
  Demo:        ___ min
  Testing:     ___ min
```

### Milestone Checklist
```
[ ] Can create file structure + enums in < 3 minutes
[ ] Can write a complete data model class in < 2 minutes
[ ] Can implement a basic CRUD service in < 10 minutes
[ ] Can write Strategy pattern from memory
[ ] Can write Factory pattern from memory
[ ] Can write Observer pattern from memory
[ ] Solved at least 5 problems within 90 minutes
[ ] Solved at least 3 problems within 75 minutes
[ ] Can explain design decisions clearly in < 5 minutes
[ ] Can demo any solution confidently
```
