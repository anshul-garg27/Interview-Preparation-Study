# The Complete Software Engineer Interview Playbook

> A battle-tested guide for landing offers at Google, Amazon, Meta, Microsoft, and top startups.
> This is not theory -- it is the exact playbook that engineers use to go from "just applying" to
> signing six-figure offers.

---

## Table of Contents

1. [Understanding the Interview Pipeline](#understanding-the-interview-pipeline)
2. [Types of Interview Rounds](#types-of-interview-rounds)
3. [3-Month Preparation Plan](#3-month-preparation-plan)
4. [Daily Routine](#daily-routine)
5. [Topic-Wise Preparation Strategy](#topic-wise-preparation-strategy)
6. [How to Track Progress](#how-to-track-progress)
7. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
8. [Resources & Tools](#resources--tools)
9. [Mindset & Mental Health](#mindset--mental-health)
10. [Quick Reference Links](#quick-reference-links)

---

## Understanding the Interview Pipeline

Every software engineering interview at a top company follows roughly the same pipeline.
Understanding each stage helps you prepare specifically for what is coming next.

```
Application → Resume Screen → Recruiter Call → Online Assessment →
Phone Screen → Onsite (4-6 rounds) → Offer → Negotiation
```

### Stage 1: Application

**What Happens**: You submit your resume through the company portal, a referral, or a recruiter reaches out to you.

**How Long**: Instant (you) / 1-4 weeks (their response)

**Key Insight**: Referrals get your resume in front of a human 10x faster than cold applications.
At Google, referred candidates are 6x more likely to get an interview.

**Action Items**:
- Get at least 2-3 referrals for your top-choice companies
- Optimize your LinkedIn -- recruiters search LinkedIn before job boards
- Apply to 15-20 companies, not 100. Quality over quantity.
- Tailor your resume keywords to each job description

### Stage 2: Resume Screen

**What Happens**: A recruiter or automated system (ATS) scans your resume for keywords,
relevant experience, and company/school brand names.

**How Long**: 1-7 days

**Key Insight**: Most ATS systems score your resume 0-100. Below 60, a human never sees it.
Key factors: job title match, skills match, years of experience, education.

**Action Items**:
- Use exact keywords from the job description
- Quantify EVERYTHING with numbers (see [Resume Guide](../01-Resume/tech-resume-guide.md))
- One page, always. No exceptions.

### Stage 3: Recruiter Call

**What Happens**: A 15-30 minute phone call. The recruiter checks your background, interest
in the role, visa status, salary expectations (sometimes), and timeline.

**How Long**: 15-30 minutes

**What They Ask**:
- "Tell me about yourself" (2-3 minute pitch)
- "Why are you interested in [Company]?"
- "What are you looking for in your next role?"
- "What is your timeline?"
- "Do you have other interviews/offers?"

**Key Insight**: This is NOT a technical round, but it IS an evaluation. Being
articulate, enthusiastic, and organized matters. Recruiters reject ~30% of candidates
at this stage.

**Action Items**:
- Prepare a 2-minute "Tell me about yourself" pitch
- Research the company (see [Company Research Guide](../02-Company-Research/how-to-research-companies.md))
- DO NOT give a salary number. Say: "I'd prefer to learn more about the role and team
  before discussing compensation."
- Have 2-3 questions ready for the recruiter

### Stage 4: Online Assessment (OA)

**What Happens**: A timed coding test on HackerRank, CodeSignal, or a proprietary platform.
Typically 1-3 problems in 60-90 minutes.

**How Long**: 60-120 minutes

**Companies That Use OA**: Amazon (almost always), Google (sometimes), Meta (rarely),
Microsoft (sometimes), most startups

**Typical Format**:
| Company | # Problems | Time | Difficulty | Platform |
|---------|-----------|------|------------|----------|
| Amazon | 2 | 70 min | Med + Med/Hard | HackerRank |
| Google | 2 | 90 min | Med-Hard | Google internal |
| Microsoft | 2-3 | 75 min | Easy-Med | Codility |
| Startups | 1-3 | 60-90 min | Easy-Hard | HackerRank/CodeSignal |

**Key Insight**: OAs are often auto-graded. Partial credit matters -- passing 12/15
test cases is much better than 0/15. Brute force first, optimize later.

**Action Items**:
- Practice on the exact platform (HackerRank vs LeetCode feels different)
- Time yourself strictly
- Always handle edge cases (empty input, single element, overflow)
- Read the problem TWICE before coding

### Stage 5: Phone Screen

**What Happens**: A 45-60 minute technical interview over video call. One interviewer,
one coding problem (sometimes two). You code in a shared editor (CoderPad, Google Docs, etc.)

**How Long**: 45-60 minutes

**Key Insight**: Phone screens are the highest-rejection stage. Companies reject 60-70%
of candidates here. The bar is: "Can this person solve a LeetCode medium cleanly in
30 minutes while communicating well?"

**Action Items**:
- Practice coding in Google Docs or CoderPad (NOT your IDE)
- Talk through your approach before coding
- Test your code with examples before saying "done"
- Aim for optimal solution, but a working brute force beats a broken optimal

### Stage 6: Onsite Interviews

**What Happens**: 4-6 back-to-back interviews (virtual or in-person), each 45-60 minutes.
This is "The Day." Multiple round types: coding, system design, behavioral, sometimes
machine coding.

**How Long**: Full day (4-6 hours)

**Typical Onsite Schedule**:
```
9:00 AM  - Coding Round 1 (DSA)
10:00 AM - Coding Round 2 (DSA)
11:00 AM - System Design (HLD)
12:00 PM - Lunch (casual, but you're still being evaluated)
1:00 PM  - Behavioral/Culture Fit
2:00 PM  - Low Level Design / Machine Coding
3:00 PM  - Hiring Manager Chat
```

**Key Insight**: You do NOT need to ace every round. Most companies use a "strong hire
in 3 out of 5 rounds" heuristic. One bad round is recoverable. Two bad rounds is
usually not.

**Action Items**:
- Practice 3-4 rounds back-to-back to build stamina
- Have a system for quickly switching mental gears between round types
- Eat well, sleep well the night before
- See [Interview Day Checklist](../05-Day-Of-Tips/interview-day-checklist.md)

### Stage 7: Offer

**What Happens**: The recruiter calls (almost always a phone call, not email) to
extend a verbal offer. They share: base salary, stock, bonus, sign-on, level, team.

**How Long**: Typically 1-3 weeks after onsite

**Key Insight**: The first number they give is NEVER the final number. Every offer
is negotiable. See [Negotiation Guide](../04-Negotiation/salary-negotiation-guide.md).

### Stage 8: Negotiation

**What Happens**: You counter-offer, they revise, you accept (or decline).

**How Long**: 1-2 weeks of back-and-forth

**Key Insight**: Candidates who negotiate earn 10-20% more on average. That is
$30,000-$80,000/year at senior levels. There is almost zero risk to negotiating
professionally.

---

## Types of Interview Rounds

| Round | Duration | What's Tested | Companies | Level |
|-------|----------|---------------|-----------|-------|
| DSA / Coding | 45-60 min | Algorithms, Data Structures | All | All |
| System Design (HLD) | 45-60 min | Architecture, Scalability | All | L4+ (3+ yrs) |
| Low Level Design (LLD) | 45-60 min | OOP, Design Patterns, Clean Code | All | All levels |
| Machine Coding | 90-120 min | Working code, Clean design, Tests | Flipkart, Uber, Swiggy, PhonePe | All |
| Behavioral | 30-45 min | Soft skills, Leadership, Culture fit | All | All |
| Bar Raiser (Amazon) | 45 min | Overall calibration, Leadership Principles | Amazon | All |
| Hiring Manager | 30 min | Team fit, Growth potential, Motivation | Most companies | All |
| System Design (LLD/OOD) | 45-60 min | Object-Oriented Design | Google, Meta | L3-L4 |

### DSA / Coding Round Deep Dive

**What They Want**:
1. Correct solution that handles edge cases
2. Optimal time and space complexity
3. Clean, readable code (not competitive programming style)
4. Clear communication of your thought process
5. Ability to test your own code

**How It Typically Goes**:
```
0-5 min:   Read problem, ask clarifying questions
5-10 min:  Discuss approach, get interviewer buy-in
10-35 min: Write code
35-45 min: Test with examples, fix bugs
45-50 min: Discuss optimizations, follow-up questions
```

**Most Common Topics by Frequency**:
```
Arrays & Strings      ████████████████████  (25%)
Trees & Graphs        ███████████████       (18%)
Dynamic Programming   ████████████          (15%)
Hashing               ███████████           (12%)
Two Pointers/Sliding  ████████              (10%)
Linked Lists          ██████                (7%)
Stack & Queue         █████                 (6%)
Sorting & Searching   ████                  (4%)
Bit Manipulation      ██                    (2%)
Math                  █                     (1%)
```

### System Design (HLD) Round Deep Dive

**What They Want**:
1. Structured approach (requirements -> high-level -> deep dive -> trade-offs)
2. Scale awareness (millions of users, terabytes of data)
3. Knowledge of distributed systems concepts
4. Ability to make and justify trade-offs
5. Depth in at least one area

**How It Typically Goes**:
```
0-5 min:    Understand problem, gather requirements
5-10 min:   Estimate scale (QPS, storage, bandwidth)
10-25 min:  High-level design (components, data flow)
25-40 min:  Deep dive into 1-2 critical components
40-45 min:  Discuss trade-offs, bottlenecks, monitoring
```

**Most Common System Design Questions**:
1. Design a URL Shortener (TinyURL)
2. Design Twitter/X Feed
3. Design WhatsApp/Messenger
4. Design Netflix/YouTube
5. Design Uber/Lyft
6. Design Instagram
7. Design Google Search
8. Design a Rate Limiter
9. Design a Notification System
10. Design Dropbox/Google Drive

### Low Level Design (LLD) Round Deep Dive

**What They Want**:
1. Clean OOP: proper use of classes, interfaces, abstractions
2. Design Patterns: know when to use Strategy, Observer, Factory, etc.
3. SOLID Principles in practice
4. Extensible design that handles future requirements
5. Clean, readable, modular code

**Most Common LLD Questions**:
1. Parking Lot System
2. Elevator System
3. Chess / Tic-Tac-Toe
4. Library Management
5. Vending Machine
6. BookMyShow (Movie Booking)
7. Splitwise (Expense Sharing)
8. Snake and Ladder Game
9. Online Shopping Cart
10. ATM Machine

### Machine Coding Round Deep Dive

**What They Want**:
1. Fully working code in 90-120 minutes
2. Clean design (not spaghetti code)
3. Proper use of OOP and design patterns
4. Handling of edge cases
5. Code that is easy to extend

**Key Difference from LLD**: In LLD, you discuss the design. In machine coding,
you actually write the complete working code. Time management is critical.

**How It Typically Goes**:
```
0-10 min:   Read problem, identify entities and behaviors
10-20 min:  Quick design (class diagram on paper)
20-80 min:  Code implementation
80-90 min:  Testing, edge cases
90-120 min: Refactor, add features if time permits
```

### Behavioral Round Deep Dive

**What They Want**:
1. Specific examples from YOUR experience (not hypotheticals)
2. STAR format: Situation, Task, Action, Result
3. Self-awareness: what you learned, what you would do differently
4. Leadership signals: initiative, ownership, conflict resolution
5. Cultural fit: values alignment with the company

**Top 10 Behavioral Questions**:
1. Tell me about yourself.
2. Tell me about a challenging project/bug you worked on.
3. Tell me about a conflict with a teammate and how you resolved it.
4. Tell me about a time you had to make a decision with incomplete information.
5. Tell me about a time you failed.
6. Tell me about a time you went above and beyond.
7. Tell me about a time you disagreed with your manager.
8. Tell me about a time you had to learn something quickly.
9. Why are you leaving your current company?
10. Where do you see yourself in 5 years?

---

## 3-Month Preparation Plan

### Prerequisites
- You can write code in at least one language (Python, Java, C++)
- You understand basic data structures (arrays, linked lists, stacks, queues)
- You have 3 hours/day available (1.5 morning + 1.5 evening)

### Month 1: Foundation (Weeks 1-4)

#### Week 1: Arrays, Strings, Hashing
| Day | Topic | Problems | Time |
|-----|-------|----------|------|
| Mon | Array basics | Two Sum, Best Time to Buy Stock | 1.5h |
| Tue | String manipulation | Valid Palindrome, Longest Substring | 1.5h |
| Wed | Hashing fundamentals | Group Anagrams, Top K Frequent | 1.5h |
| Thu | Two Pointers | Container With Most Water, 3Sum | 1.5h |
| Fri | Sliding Window | Min Window Substring, Max Sliding Window | 1.5h |
| Sat | Practice Day | Solve 3 new medium problems | 3h |
| Sun | Review | Re-solve problems you struggled with | 1.5h |

#### Week 2: Linked Lists, Stacks, Queues
| Day | Topic | Problems | Time |
|-----|-------|----------|------|
| Mon | Linked List basics | Reverse LL, Merge Two Sorted | 1.5h |
| Tue | Linked List advanced | Detect Cycle, LRU Cache | 1.5h |
| Wed | Stacks | Valid Parentheses, Min Stack | 1.5h |
| Thu | Queues & Deques | Implement Queue using Stacks | 1.5h |
| Fri | Monotonic Stack | Next Greater Element, Largest Rectangle | 1.5h |
| Sat | Practice Day | 3 new medium problems | 3h |
| Sun | Review | Re-solve + start LLD basics | 1.5h |

#### Week 3: Trees, Graphs (Part 1)
| Day | Topic | Problems | Time |
|-----|-------|----------|------|
| Mon | Binary Tree basics | Inorder, Preorder, Level Order | 1.5h |
| Tue | BST operations | Validate BST, Kth Smallest | 1.5h |
| Wed | Tree problems | Max Depth, Diameter, LCA | 1.5h |
| Thu | Graph basics (BFS) | Number of Islands, Rotten Oranges | 1.5h |
| Fri | Graph basics (DFS) | Clone Graph, Course Schedule | 1.5h |
| Sat | Practice Day | 3 tree/graph mediums | 3h |
| Sun | Review + LLD study | OOP, SOLID principles overview | 1.5h |

#### Week 4: Recursion, Backtracking
| Day | Topic | Problems | Time |
|-----|-------|----------|------|
| Mon | Recursion fundamentals | Power of Two, Fibonacci | 1.5h |
| Tue | Backtracking basics | Subsets, Permutations | 1.5h |
| Wed | Backtracking medium | Combination Sum, Word Search | 1.5h |
| Thu | Backtracking hard | N-Queens, Sudoku Solver | 1.5h |
| Fri | Mixed practice | 2 random medium problems | 1.5h |
| Sat | Month 1 Assessment | Solve 3 unseen problems (timed) | 3h |
| Sun | Review & plan Month 2 | Re-solve weak areas, adjust plan | 1.5h |

**Month 1 Targets**:
- 80+ LeetCode problems solved
- Comfortable with arrays, strings, trees, graphs
- Basic understanding of OOP and SOLID

### Month 2: Core (Weeks 5-8)

#### Week 5: Dynamic Programming (Part 1)
| Day | Topic | Problems | Time |
|-----|-------|----------|------|
| Mon | DP concepts, 1D DP | Climbing Stairs, House Robber | 1.5h |
| Tue | 1D DP continued | Coin Change, Longest Increasing Subseq | 1.5h |
| Wed | 2D DP | Unique Paths, Edit Distance | 1.5h |
| Thu | 2D DP continued | Longest Common Subsequence | 1.5h |
| Fri | Knapsack Pattern | 0/1 Knapsack, Partition Equal Subset | 1.5h |
| Sat | DP Practice | 3 DP mediums | 3h |
| Sun | Review + LLD | Study 1 design pattern (Strategy) | 1.5h |

#### Week 6: Dynamic Programming (Part 2) + Greedy
| Day | Topic | Problems | Time |
|-----|-------|----------|------|
| Mon | Interval DP | Burst Balloons, Matrix Chain | 1.5h |
| Tue | String DP | Palindrome Partitioning, Regex Match | 1.5h |
| Wed | Greedy basics | Activity Selection, Jump Game | 1.5h |
| Thu | Greedy medium | Merge Intervals, Task Scheduler | 1.5h |
| Fri | Mixed DP + Greedy | 2 random problems | 1.5h |
| Sat | LLD Deep Dive | Parking Lot design (full) | 3h |
| Sun | Review | Re-solve DP problems, review patterns | 1.5h |

#### Week 7: System Design (HLD) Fundamentals
| Day | Topic | Activity | Time |
|-----|-------|----------|------|
| Mon | HLD basics | Scaling, Load Balancers, CDN | 1.5h AM + 1 LC |
| Tue | Databases | SQL vs NoSQL, Sharding, Replication | 1.5h AM + 1 LC |
| Wed | Caching | Cache strategies, Redis, Memcached | 1.5h AM + 1 LC |
| Thu | Message Queues | Kafka, RabbitMQ, Pub/Sub | 1.5h AM + 1 LC |
| Fri | Practice | Design URL Shortener (full) | 1.5h AM + 1 LC |
| Sat | Practice | Design Twitter Feed (full) | 3h |
| Sun | Review | Review all HLD concepts | 1.5h |

#### Week 8: System Design (HLD) Practice
| Day | Topic | Activity | Time |
|-----|-------|----------|------|
| Mon | Design WhatsApp | Full design walkthrough | 1.5h + 1 LC |
| Tue | Design Netflix | Full design walkthrough | 1.5h + 1 LC |
| Wed | Design Uber | Full design walkthrough | 1.5h + 1 LC |
| Thu | LLD: Elevator | Full LLD walkthrough | 1.5h + 1 LC |
| Fri | LLD: BookMyShow | Full LLD walkthrough | 1.5h + 1 LC |
| Sat | Mock Interview | Full 60-min HLD mock | 3h |
| Sun | Review & adjust | Weak area focus | 1.5h |

**Month 2 Targets**:
- 150+ LeetCode problems (cumulative)
- DP pattern mastery
- 5+ system design problems practiced
- 3+ LLD problems designed
- Behavioral stories drafted (5-7 STAR stories)

### Month 3: Polish (Weeks 9-12)

#### Week 9: Machine Coding + Advanced Topics
| Day | Topic | Activity | Time |
|-----|-------|----------|------|
| Mon | Machine Coding | Build Parking Lot (timed 90 min) | 1.5h + 1 LC |
| Tue | Machine Coding | Build Snake & Ladder (timed 90 min) | 1.5h + 1 LC |
| Wed | Graph Advanced | Dijkstra, Topological Sort, Union-Find | 1.5h + 1 LC |
| Thu | Trie + Segment Tree | Implement Trie, Range Query | 1.5h + 1 LC |
| Fri | Behavioral Prep | Write 7 STAR stories | 1.5h + 1 LC |
| Sat | Full Mock | Coding + Behavioral (back-to-back) | 3h |
| Sun | Review | Polish weak areas | 1.5h |

#### Week 10: Mock Interviews + Company-Specific Prep
| Day | Topic | Activity | Time |
|-----|-------|----------|------|
| Mon | Mock Coding | Practice on Pramp or Interviewing.io | 1.5h + 1 LC |
| Tue | Mock HLD | Practice system design with a friend | 1.5h + 1 LC |
| Wed | Company Research | Deep dive on target company | 1.5h + 1 LC |
| Thu | Mock Behavioral | Record yourself answering 5 questions | 1.5h + 1 LC |
| Fri | Machine Coding | Build Vending Machine (timed 90 min) | 1.5h + 1 LC |
| Sat | Full Mock | Complete 4-round mock onsite | 4h |
| Sun | Review & adjust | Feedback analysis | 1.5h |

#### Week 11: Intensive Mock Interviews
| Day | Activity | Time |
|-----|----------|------|
| Mon | Mock #1 (Coding) - Get feedback | 2h |
| Tue | Fix weak spots from Mock #1 | 2h |
| Wed | Mock #2 (Full onsite simulation) | 4h |
| Thu | Fix weak spots from Mock #2 | 2h |
| Fri | Mock #3 (Behavioral focus) | 2h |
| Sat | Mock #4 (System Design focus) | 3h |
| Sun | Rest & light review | 1h |

#### Week 12: Final Sprint
| Day | Activity | Time |
|-----|----------|------|
| Mon | Revise top 50 LC patterns | 2h |
| Tue | Revise system design notes | 2h |
| Wed | Revise LLD notes + SOLID | 1.5h |
| Thu | Review all STAR stories | 1h |
| Fri | Light practice (2 easy problems for confidence) | 1h |
| Sat | Rest. Trust your preparation. | 0h |
| Sun | Interview day prep (see Day-Of checklist) | 30min |

**Month 3 Targets**:
- 200+ LeetCode problems (cumulative)
- 8+ system design problems
- 5+ LLD problems
- 2-3 machine coding builds
- 7+ polished STAR stories
- 4+ mock interviews completed
- Company-specific preparation done

---

## Daily Routine

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY SCHEDULE                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Morning Session (1.5 hours):                               │
│  ┌─────────────────────────────────────────────────┐       │
│  │  Problem 1: Medium (30 min)                      │       │
│  │  Problem 2: Hard attempt OR 2nd Medium (30 min)  │       │
│  │  Review & Notes (30 min)                         │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
│  Evening Session (1.5 hours):                               │
│  ┌─────────────────────────────────────────────────┐       │
│  │  Monday:    System Design study/practice         │       │
│  │  Tuesday:   LLD / Machine Coding                 │       │
│  │  Wednesday: System Design study/practice         │       │
│  │  Thursday:  LLD / Machine Coding                 │       │
│  │  Friday:    Behavioral prep (STAR stories)       │       │
│  │  Saturday:  Full Mock Interview (3 hours)        │       │
│  │  Sunday:    Review weak areas + rest             │       │
│  └─────────────────────────────────────────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### How to Solve a LeetCode Problem (The Method)

Follow this exact process for every problem:

```
Step 1: Read the problem (2 min)
  - Read it twice
  - Identify: input type, output type, constraints

Step 2: Work through examples (3 min)
  - Trace through given examples by hand
  - Create your own edge case example

Step 3: Identify the pattern (5 min)
  - Which category? (Two pointers? DP? Graph?)
  - What data structures help? (HashMap? Stack? Heap?)

Step 4: Plan your approach (5 min)
  - Pseudocode or bullet points
  - State time & space complexity BEFORE coding

Step 5: Code (15 min)
  - Write clean code, not clever code
  - Use meaningful variable names
  - Handle edge cases

Step 6: Test (5 min)
  - Trace through with Example 1
  - Try empty input, single element, large input
  - Fix any bugs

Step 7: Optimize (5 min)
  - Can you improve time complexity?
  - Can you reduce space?
  - Is there a cleaner way to write this?
```

### If You Are Stuck on a Problem

```
0-15 min:  Try harder. Re-read the problem. Draw pictures.
15-25 min: Look at hints (if available). Think about the category.
25-30 min: Look at the solution. BUT:
  1. Read ONLY the approach (not the code)
  2. Close the solution
  3. Implement it yourself
  4. Come back to this problem in 3 days
```

**NEVER** spend more than 45 minutes on a single problem during prep. The goal is
to learn patterns, not struggle heroically.

---

## Topic-Wise Preparation Strategy

### Tier 1: Must Know (Asked in 80% of interviews)
- Arrays & Strings (Two Pointers, Sliding Window)
- Hash Maps & Sets
- Binary Trees & BST
- BFS & DFS (Graph Traversal)
- Dynamic Programming (1D & 2D)
- Sorting & Binary Search

### Tier 2: Frequently Asked (Asked in 50% of interviews)
- Linked Lists
- Stacks & Queues (Monotonic Stack)
- Greedy Algorithms
- Backtracking
- Heaps / Priority Queue
- Union Find

### Tier 3: Occasionally Asked (Asked in 20% of interviews)
- Trie
- Segment Tree / BIT
- Bit Manipulation
- Math & Geometry
- Topological Sort
- Advanced Graph (Dijkstra, Bellman-Ford)

**Strategy**: Master Tier 1 completely before touching Tier 3. Most candidates
fail because they spread too thin, not because they lack knowledge of advanced topics.

---

## How to Track Progress

### Weekly Tracking Template

```markdown
## Week [X] Progress Report
Date: [Start] to [End]

### Problems Solved
| # | Problem | Difficulty | Topic | Solved? | Time | Notes |
|---|---------|-----------|-------|---------|------|-------|
| 1 |         |           |       | Y/N     | min  |       |
| 2 |         |           |       | Y/N     | min  |       |
...

### Topics Covered
- [ ] Topic 1: Comfort level (1-5)
- [ ] Topic 2: Comfort level (1-5)

### Mock Interview Score
- Coding: _/10
- Communication: _/10
- Design: _/10

### What Went Well
-

### What Needs Improvement
-

### Plan for Next Week
-
```

### Monthly Milestones

| Metric | Month 1 | Month 2 | Month 3 |
|--------|---------|---------|---------|
| LC Problems | 80 | 150 | 200+ |
| HLD Problems | 0 | 5 | 8+ |
| LLD Problems | 1 | 4 | 6+ |
| Mock Interviews | 0 | 2 | 6+ |
| STAR Stories | Draft | 5 polished | 7+ polished |
| Confidence (1-10) | 4 | 6 | 8+ |

### Key Ratios
- Easy : Medium : Hard = 20% : 60% : 20%
- New Problems : Revisits = 70% : 30%
- Coding : Design : Behavioral = 50% : 30% : 20%

---

## Common Mistakes to Avoid

### Mistake 1: Only Doing LeetCode
LeetCode is important, but it is only 40-50% of the interview. Ignoring system design,
behavioral, and LLD is the #1 reason experienced engineers fail interviews.

### Mistake 2: Solving 500+ Problems Without Patterns
Quality > Quantity. 200 well-understood problems across all patterns beats 500 problems
done mindlessly. After each problem, ask: "What pattern did this use? Where else can
I apply it?"

### Mistake 3: Not Doing Mock Interviews
Practicing alone is like training for a fight by only hitting a punching bag.
You need the pressure of a real person asking follow-ups, watching you code,
and timing you.

### Mistake 4: Skipping Behavioral Prep
"I'll just wing it." This is a recipe for rambling, unfocused answers. At Amazon,
behavioral is 50% of the decision. At every company, a bad behavioral round can
sink an otherwise strong candidate.

### Mistake 5: Not Negotiating
You are leaving $20K-$100K on the table. Every. Single. Time.
See [Negotiation Guide](../04-Negotiation/salary-negotiation-guide.md).

### Mistake 6: Applying to Dream Company First
Use your first 2-3 interviews as warm-ups at companies you care less about.
You will be measurably better after real interview experience.

### Mistake 7: Ignoring Communication Skills
The interviewer cannot read your mind. If you solve the problem perfectly but
never explain your approach, you will get a "no hire." Think out loud.

### Mistake 8: Studying 8 Hours a Day
Burnout is real. 3 hours of focused, consistent study beats 8 hours of
exhausted cramming. Consistency > intensity.

---

## Resources & Tools

### Coding Practice
| Resource | Best For | Cost |
|----------|----------|------|
| LeetCode | DSA practice, company-tagged problems | Free / $35/mo |
| NeetCode.io | Pattern-based learning, roadmap | Free |
| Blind 75 / NeetCode 150 | Curated problem lists | Free |
| AlgoExpert | Video explanations | $99/yr |

### System Design
| Resource | Best For | Cost |
|----------|----------|------|
| System Design Interview (Alex Xu) | Book, structured approach | $30 |
| Designing Data-Intensive Apps | Deep understanding | $40 |
| Grokking System Design (Educative) | Interactive learning | $79 |
| YouTube: System Design Primer | Free explanations | Free |

### Behavioral
| Resource | Best For | Cost |
|----------|----------|------|
| Exponent | Behavioral + PM interviews | $99/mo |
| YouTube: Jeff H Sipe | Amazon LP practice | Free |
| STAR Method Template | Structuring answers | Free |

### Mock Interviews
| Resource | Best For | Cost |
|----------|----------|------|
| Pramp | Free peer mock interviews | Free |
| Interviewing.io | Anonymous mocks with engineers | Free/Paid |
| Hello Interview | AI-powered mocks | Paid |
| Friends/colleagues | Personalized feedback | Free |

### Tools
- **Timer**: Use a Pomodoro timer (30-min blocks)
- **Notes**: Notion or Obsidian for organized notes
- **Coding**: Practice in the same environment as the interview (CoderPad, Google Docs)
- **Tracking**: Spreadsheet or LeetCode progress tracker

---

## Mindset & Mental Health

### Dealing with Rejection

Rejection is NOT a measure of your worth as an engineer. It is a measure of
your fit FOR THAT INTERVIEW ON THAT DAY.

Facts to remember:
- Max Howell (creator of Homebrew) was rejected by Google for not inverting a binary tree
- Many FAANG engineers failed 3-5 interviews before getting in
- Interview performance correlates weakly with job performance
- A "no" today does not mean "no" forever (most companies allow re-applying in 6-12 months)

**After a rejection**:
1. Allow yourself 24 hours to feel disappointed
2. Ask the recruiter for feedback (they sometimes share it)
3. Analyze what went wrong objectively
4. Adjust your preparation
5. Apply again when you are ready

### Managing Interview Anxiety

**Before the interview**:
- Deep breathing: 4 counts in, 7 counts hold, 8 counts out
- Power pose: Stand tall for 2 minutes (research shows this works)
- Positive self-talk: "I have prepared. I am ready. I will do my best."
- Visualize success: Imagine yourself solving the problem confidently

**During the interview**:
- If you freeze: Say "Let me take a moment to think about this"
- If you are stuck: Talk to the interviewer, they WANT to help you
- If you make a mistake: "Good catch, let me fix that" (not "I'm so stupid")
- Remember: The interviewer wants you to succeed

### Imposter Syndrome

"Everyone else seems so much smarter and more prepared than me."

Reality check:
- 70% of people experience imposter syndrome
- The people who seem confident are often just as nervous
- You were invited to interview because your background is strong enough
- Feeling like you do not belong is itself a sign that you have high standards

**Antidote**: Keep a "wins" journal. Write down every problem you solve,
every concept you learn, every mock interview you complete.

### Taking Breaks

- **Pomodoro**: 25 min study, 5 min break
- **Daily**: At least 1 hour of non-screen activity
- **Weekly**: Take one full day off (Sunday or Saturday)
- **When burned out**: Take 2-3 days off completely. You will come back sharper.

### Celebrating Small Wins

Interview prep is a marathon. Celebrate these milestones:
- First LeetCode medium solved independently
- First 50 problems
- First mock interview completed
- First system design problem designed end-to-end
- First STAR story polished
- Getting to the onsite round
- Every offer received (even if you decline it)

---

## Quick Reference Links

| Topic | File |
|-------|------|
| Resume Guide | [01-Resume/tech-resume-guide.md](../01-Resume/tech-resume-guide.md) |
| Company Research | [02-Company-Research/how-to-research-companies.md](../02-Company-Research/how-to-research-companies.md) |
| Mock Interview Guide | [03-Mock-Interviews/how-to-conduct-mocks.md](../03-Mock-Interviews/how-to-conduct-mocks.md) |
| Salary Negotiation | [04-Negotiation/salary-negotiation-guide.md](../04-Negotiation/salary-negotiation-guide.md) |
| Interview Day Checklist | [05-Day-Of-Tips/interview-day-checklist.md](../05-Day-Of-Tips/interview-day-checklist.md) |
| Google Guide | [06-Company-Guides/Google/README.md](../06-Company-Guides/Google/README.md) |
| Amazon Guide | [06-Company-Guides/Amazon/README.md](../06-Company-Guides/Amazon/README.md) |
| Meta Guide | [06-Company-Guides/Meta/README.md](../06-Company-Guides/Meta/README.md) |
| Microsoft Guide | [06-Company-Guides/Microsoft/README.md](../06-Company-Guides/Microsoft/README.md) |

---

## Final Words

The interview process is imperfect, stressful, and sometimes unfair. But it is
also learnable. Every single skill tested in a tech interview can be practiced
and improved. You are not born knowing how to invert a binary tree or design
a URL shortener. You learn it.

The engineers who get offers are not the smartest -- they are the most prepared.
And preparation is entirely within your control.

Start today. Be consistent. Trust the process.

Good luck. You have got this.
