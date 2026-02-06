# Day Before Interview — The Final Review

> THE document to read the night before your LLD interview. Confidence, clarity, execution.

---

## Top 10 Things Interviewers Look For

| #  | What They Evaluate                        | How to Demonstrate It                              |
|----|-------------------------------------------|----------------------------------------------------|
| 1  | **Requirement gathering**                 | Ask 3-5 clarifying questions before designing       |
| 2  | **Object-oriented thinking**              | Identify clear classes with single responsibilities |
| 3  | **Clean class design**                    | Private fields, public methods, meaningful names    |
| 4  | **Correct relationships**                 | IS-A vs HAS-A, composition over inheritance         |
| 5  | **Design pattern application**            | Use 1-2 patterns and explain WHY you chose them     |
| 6  | **Extensibility**                         | Show how a new type/feature can be added easily     |
| 7  | **Edge case awareness**                   | Mention concurrency, error handling, limits          |
| 8  | **Communication throughout**              | Think aloud, explain trade-offs, ask for feedback   |
| 9  | **Working code**                          | Code compiles/runs, not pseudocode                  |
| 10 | **Time management**                       | Cover all steps within the time limit               |

---

## Most Common Mistakes (Avoid These!)

| Mistake                             | Why It Hurts                          | Fix                                    |
|-------------------------------------|---------------------------------------|----------------------------------------|
| Jumping to code immediately         | Shows lack of planning                | Spend 10 min on design first           |
| God class (one class does everything)| Shows weak OOP understanding         | Split by responsibility                |
| Not asking requirements             | You'll solve the wrong problem        | Always clarify scope first             |
| Over-engineering                    | 30 classes for a simple problem       | 5-8 core classes is usually right      |
| Hardcoding types in if/elif         | Violates OCP, hard to extend          | Use Strategy or Factory                |
| Not using interfaces/abstract classes| Misses extensibility opportunity     | At least one ABC for key abstractions  |
| Silent coding                       | Interviewer can't evaluate thinking   | Narrate your decisions aloud           |
| Ignoring edge cases                 | Shows lack of production experience   | Mention 2-3 edge cases proactively     |
| Forcing patterns that don't fit     | "Pattern tourist" impression          | Only use patterns you can justify      |
| Not handling follow-ups gracefully  | Shows rigidity                        | Say "Good point, I'd modify by..."     |

---

## Pattern Selection Quick Guide

**Memorize these 5 questions:**

| Question to Ask Yourself                    | If Yes, Use...                     |
|---------------------------------------------|------------------------------------|
| "Are there different types of [X]?"         | Factory Method                     |
| "Does [X] change behavior based on state?"  | State Pattern                      |
| "Can the algorithm for [X] vary?"           | Strategy Pattern                   |
| "Do multiple objects need to know about [X]?"| Observer Pattern                  |
| "Is [X] constructed in multiple steps?"     | Builder Pattern                    |

**Top 4 patterns to know cold:**
1. **Strategy** — Different algorithms for the same task
2. **Observer** — Notify when something changes
3. **Factory** — Create objects without specifying exact type
4. **State** — Behavior depends on current state

---

## Time Management Plan

### For a 45-Minute Interview

```
[0-5 min]   REQUIREMENTS — Ask questions, list core features
[5-10 min]  CLASSES — Identify 5-8 core classes, their responsibilities
[10-15 min] RELATIONSHIPS — Draw class diagram, define interfaces
[15-30 min] CODE — Implement core classes, apply patterns
[30-40 min] WALKTHROUGH — Demo the flow, handle interviewer questions
[40-45 min] EXTENSIONS — Discuss scalability, edge cases, improvements
```

### Time Checkpoints

| Time Passed | You Should Have...                                   |
|-------------|------------------------------------------------------|
| 5 min       | Requirements clarified, scope defined                 |
| 10 min      | Core classes identified, relationships sketched       |
| 15 min      | UML diagram or class structure on board               |
| 25 min      | 2-3 core classes coded                                |
| 35 min      | Working code, at least one design pattern applied     |
| 45 min      | Discussed extensions and trade-offs                   |

**If running out of time:** Skip less important classes, focus on the core interaction.

---

## Quick Mental Walkthrough Template

When you get any LLD problem, run this checklist mentally:

### Phase 1: Understand (2 min)
- [ ] What is the MAIN entity? (Parking lot, elevator, game...)
- [ ] Who are the ACTORS? (User, admin, driver...)
- [ ] What are the 3-5 CORE actions? (book, cancel, search...)

### Phase 2: Structure (5 min)
- [ ] List 5-8 classes (nouns from requirements)
- [ ] For each class: 2-3 key attributes, 1-2 key methods
- [ ] Draw relationships (arrows between classes)
- [ ] Identify at least 1 interface/abstract class

### Phase 3: Patterns (3 min)
- [ ] Is there a varying algorithm? -> Strategy
- [ ] Is there a notification need? -> Observer
- [ ] Is there object creation complexity? -> Factory
- [ ] Is there a state machine? -> State
- [ ] Is there a need for extension? -> OCP via abstraction

### Phase 4: Code (15 min)
- [ ] Start with the central class (e.g., ParkingLot, Game)
- [ ] Code the abstract classes / interfaces first
- [ ] Then concrete implementations
- [ ] Wire them together in a main method or demo

### Phase 5: Discuss (5 min)
- [ ] Walk through a sample scenario end-to-end
- [ ] Mention 2 edge cases you handled
- [ ] Mention 1 thing you'd improve with more time
- [ ] Be ready for "how would you add [X]?"

---

## Confidence Boosting Reminders

### What you should know going in:

**You DO know this.** If you've studied OOP, SOLID, and design patterns, you have the tools. The interview is about applying them, not inventing them.

**There is no single "right" answer.** LLD interviews assess your thinking process, not whether you match a specific solution. Multiple valid designs exist.

**Simplicity wins.** A clean 5-class solution that works beats a 20-class over-engineered mess. Start simple, extend when asked.

**Communication is half the grade.** Even if your design isn't perfect, explaining your reasoning clearly shows strong engineering thinking.

**Patterns are tools, not goals.** Don't force patterns. Use them when they solve a real problem. "I chose Strategy here because the pricing algorithm varies by customer type" is strong. "I used Strategy because... it's a pattern" is weak.

**Mistakes are fine.** If the interviewer points out a flaw, say "Good point, I'd refactor by [X]." Adaptability is valued.

---

## Pre-Interview Checklist

### The Night Before
- [ ] Review this document
- [ ] Practice ONE problem end-to-end (timed, 45 min)
- [ ] Review the pattern selection quick guide above
- [ ] Get a good night's sleep

### 30 Minutes Before
- [ ] Have pen and paper (or whiteboard) ready
- [ ] Open your IDE if it's a coding interview
- [ ] Take 5 deep breaths
- [ ] Remind yourself: "I know my patterns, I know my SOLID, I've got this"

### During the Interview
- [ ] Ask requirements FIRST (shows maturity)
- [ ] Narrate your thinking (shows process)
- [ ] Draw before you code (shows planning)
- [ ] Use at least one design pattern (shows knowledge)
- [ ] Handle follow-ups gracefully (shows adaptability)

---

## Emergency Quick-Reference

### "I don't know this problem"
1. Don't panic. Identify the CORE entity.
2. List actors and actions.
3. Use the noun-verb technique to find classes and methods.
4. Apply basic OOP — it goes a long way.

### "I'm stuck on the design"
1. Start with the simplest version that works.
2. Ask the interviewer: "Should I focus on [X] or [Y] first?"
3. Write one class, then build outward.

### "The interviewer wants something different"
1. "That's a great point. Let me adjust my design."
2. Don't defend wrong decisions — pivot quickly.
3. Show that you can adapt.

### "I'm running out of time"
1. Skip the least important classes.
2. Code pseudocode with comments for remaining parts.
3. Say: "With more time, I'd implement [X] and [Y]."
4. Demonstrate you know what's missing.

---

## The Final 5 Mantras

1. **Clarify first, code later** — Requirements before design, design before code.
2. **Name things well** — Clear names show clear thinking.
3. **Think in objects** — Every noun is a class, every verb is a method.
4. **Favor composition** — It's almost always the right choice.
5. **Communicate constantly** — The interviewer wants to hear you think.

---

**You've prepared. You know this material. Trust your preparation and show them your best.**

---

*Final review document | 2026-02-06*
