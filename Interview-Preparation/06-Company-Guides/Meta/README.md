# Complete Meta (Facebook) Interview Guide (E3-E6)

> Meta interviews prioritize impact, speed of execution, and coding fundamentals.
> Unlike Amazon's LP-heavy approach, Meta focuses on raw coding ability and
> system design thinking. This guide covers the exact process, what makes
> Meta different, and how to prepare specifically for Meta interviews.

---

## Table of Contents

1. [Meta's Interview Process](#metas-interview-process)
2. [What Makes Meta Different](#what-makes-meta-different)
3. [Levels at Meta](#levels-at-meta)
4. [Round-by-Round Breakdown](#round-by-round-breakdown)
5. [Meta-Specific Tips](#meta-specific-tips)
6. [Meta's Culture and Values](#metas-culture-and-values)
7. [Ninja and Pirate: Meta's Evaluation Framework](#ninja-and-pirate)
8. [Top 20 Meta Interview Questions](#top-20-meta-interview-questions)
9. [Meta Interview Timeline](#meta-interview-timeline)
10. [Meta Offer Structure](#meta-offer-structure)

---

## Meta's Interview Process

```
Application / Referral
       │
       ▼
Recruiter Screen (15-30 min phone call)
       │
       ▼
Phone Screen (45 min, 2 coding problems)
       │
       ▼
Onsite / Virtual Onsite (4-5 rounds)
  ├── Coding Round 1 (45 min, 2 problems)
  ├── Coding Round 2 (45 min, 2 problems)
  ├── System Design (45 min) [E4+]
  └── Behavioral (45 min)
       │
       ▼
Hiring Committee + Offer Review
       │
       ▼
Offer
```

### Key Timelines

| Stage | Duration |
|-------|----------|
| Application to Recruiter Screen | 1-3 weeks |
| Recruiter Screen to Phone Screen | 1-2 weeks |
| Phone Screen to Onsite | 1-3 weeks |
| Onsite to Decision | 1-2 weeks |
| Decision to Offer | 1 week |
| **Total: Application to Offer** | **4-6 weeks** |

Meta is one of the fastest FAANG companies in their interview process.

---

## What Makes Meta Different

### 1. Two Problems Per Coding Round

Most companies give one coding problem per round. Meta gives TWO. This means:
- You have about 20 minutes per problem (not 35-40)
- Speed matters more than at Google
- Problems tend to be clean LeetCode Medium (not tricky Hards)
- There is no time for a slow start or lengthy discussion

### 2. No Leadership Principles

Unlike Amazon, Meta does not have a formal LP framework. The behavioral round
evaluates general qualities: impact, collaboration, initiative, and communication.
You do not need to memorize a list of principles.

### 3. "Move Fast" Is Real

Meta's culture values speed of execution. In interviews, this translates to:
- Solve problems quickly and cleanly
- In system design, show you can make decisions without overthinking
- In behavioral, show examples of shipping fast and iterating

### 4. Coding Is King

At Meta, coding rounds carry the most weight. If you crush the coding rounds
but have an average system design round, you are likely fine. If you crush
system design but fail coding, you are likely rejected.

**Weight approximation**:
- Coding: 50%
- System Design: 30%
- Behavioral: 20%

### 5. Strong Focus on Product Impact

Meta evaluates "impact" heavily. In behavioral rounds, they want to hear:
- What was the user/business impact of your work?
- How did you measure success?
- What metrics moved?

### 6. E3-E4 Do Not Get System Design

New grads (E3) and some E4 candidates do an additional coding round instead
of system design. System design is for E4+ (and mandatory from E5).

---

## Levels at Meta

| Level | Title | Years | TC Range (2026) | System Design? |
|-------|-------|-------|----------------|---------------|
| E3 | Software Engineer | 0-2 | $180-220K | No |
| E4 | Software Engineer | 2-5 | $280-380K | Sometimes |
| E5 | Senior SWE | 5-10 | $380-550K | Yes |
| E6 | Staff SWE | 8-15 | $500-750K | Yes (harder) |
| E7 | Senior Staff SWE | 15+ | $750K-1.1M | Yes (expert) |

**Note**: Meta tends to pay at the top of the FAANG range, especially for E5+.
They are also one of the most generous with RSU grants.

---

## Round-by-Round Breakdown

### Phone Screen (1 Round, 45 minutes)

**Format**: Video call + CoderPad (real code editor, can run code)

**Structure**:
```
0-2 min:   Introduction
2-22 min:  Problem 1 (LeetCode Medium)
22-42 min: Problem 2 (LeetCode Medium)
42-45 min: Your questions
```

**What to Expect**:
- 2 coding problems in 45 minutes
- Both are typically LeetCode Medium
- You CAN run your code on CoderPad
- The interviewer may give hints if you are stuck

**Tips**:
- Speed is critical. Practice solving mediums in 18-20 minutes.
- Start coding quickly -- spend 2-3 minutes on approach, not 7-8.
- Code must compile and run correctly.
- Test with the given examples, then submit.

**Common Phone Screen Topics**:
- Arrays and Strings (most common)
- Hash Maps and Sets
- Linked Lists
- Binary Trees
- Sorting and Searching

### Coding Rounds (2 Rounds, 45 minutes each)

**Format**: CoderPad (can run code)

**Structure** (each round):
```
0-2 min:   Introduction
2-22 min:  Problem 1
22-42 min: Problem 2
42-45 min: Brief questions (optional)
```

**What to Expect**:
- 2 problems per round = 4 coding problems total in the onsite
- Difficulty: LeetCode Medium (occasionally Easy + Medium or Medium + Hard)
- Speed and correctness are both valued
- Follow-up questions are common ("What if the input is 10x larger?")

**Common Onsite Coding Topics**:
1. **Arrays/Strings**: Two Sum variants, substring problems, sliding window
2. **Trees**: Level-order traversal, path sum, serialize/deserialize
3. **Graphs**: BFS/DFS, shortest path, connected components
4. **Dynamic Programming**: 1D DP (less common than at Google)
5. **Hash Maps**: Frequency counting, grouping, lookup optimization
6. **Stacks/Queues**: Monotonic stack, BFS with queue

**What They Evaluate**:
1. **Speed**: Can you solve 2 mediums in 40 minutes?
2. **Correctness**: Does your code run and produce correct output?
3. **Code Quality**: Is it clean, readable, and well-structured?
4. **Communication**: Did you explain your approach?
5. **Bug Fixing**: Can you debug quickly when something is wrong?

**Tips**:
- Practice solving 2 mediums back-to-back in 40 minutes
- Meta problems are "clean" -- they test fundamental skills, not obscure tricks
- Write working code first, optimize second
- Use meaningful variable names and clean structure
- If you finish early, use the time for follow-up optimization

### System Design Round (1 Round, 45 minutes) -- E4+ Only

**Format**: Whiteboard (in-person) or Excalidraw/shared doc (virtual)

**Structure**:
```
0-5 min:   Understand the problem, clarify requirements
5-10 min:  High-level design (components, data flow)
10-30 min: Deep dive into key components
30-40 min: Scaling, trade-offs, edge cases
40-45 min: Questions
```

**Common System Design Questions at Meta**:
1. Design Facebook News Feed
2. Design Instagram
3. Design Facebook Messenger
4. Design Instagram Stories
5. Design a Live Video Streaming Service
6. Design Facebook Search
7. Design a Photo Storage Service
8. Design a Notification System
9. Design Facebook Events
10. Design a Content Moderation System

**What They Evaluate**:
1. **Product thinking**: Do you understand the user experience?
2. **Technical depth**: Can you go deep on data models, APIs, and algorithms?
3. **Scaling ability**: Can you handle billions of users?
4. **Trade-off analysis**: Can you articulate why you chose X over Y?
5. **Communication**: Can you clearly present your design?

**Tips**:
- Meta interviewers value product thinking. Start by understanding the user flow.
- Show you understand the read-heavy vs write-heavy nature of social media.
- Mention caching heavily -- Meta's stack relies on Memcached/TAO.
- Discuss data models in detail (schema design matters at Meta).
- Consider privacy and content moderation in your design (it is Meta's reality).

### Behavioral Round (1 Round, 45 minutes)

**Format**: Conversation. No coding.

**Structure**:
```
0-3 min:   "Tell me about yourself"
3-12 min:  Story 1 (impact/project question)
12-22 min: Story 2 (collaboration/conflict question)
22-32 min: Story 3 (initiative/drive question)
32-40 min: Story 4 (failure/learning question)
40-45 min: Your questions
```

**Common Behavioral Questions at Meta**:
1. "Tell me about yourself."
2. "What is the project you are most proud of? What was the impact?"
3. "Tell me about a time you had to make a difficult technical decision."
4. "Tell me about a time you had a conflict with a teammate."
5. "Tell me about a time you took initiative without being asked."
6. "Tell me about a time something went wrong in production. What did you do?"
7. "Why Meta?"
8. "Tell me about a time you had to move fast and make compromises."
9. "How do you handle ambiguous requirements?"
10. "Tell me about a time you mentored someone or helped a teammate grow."

**What They Evaluate**:
- **Impact**: Did your work matter? Can you quantify it?
- **Drive**: Are you self-motivated? Do you take initiative?
- **Collaboration**: Can you work well with others?
- **Communication**: Are you clear and concise?
- **Self-awareness**: Do you learn from mistakes?

**Tips**:
- Emphasize IMPACT in every story. Meta cares deeply about measurable results.
- Use the format: "I did X, which resulted in Y% improvement in Z metric."
- Show you "move fast" -- stories about shipping quickly and iterating beat
  stories about long, careful planning.
- Be genuine about failures. Meta values growth mindset.

---

## Meta-Specific Tips

### Tip 1: Speed Is Everything in Coding Rounds

With 2 problems per round and only 45 minutes, you have roughly 20 minutes per
problem. Practice this timing:

```
Minute 0-2:  Read problem, identify pattern
Minute 2-4:  Discuss approach briefly
Minute 4-17: Code the solution
Minute 17-20: Test and fix bugs
```

If you spend 25 minutes on Problem 1, you only have 15 minutes for Problem 2.
Time management is critical.

### Tip 2: Code Must Run

Unlike Google (where you code in Google Docs), Meta uses CoderPad where you
can actually run your code. This means:
- Syntax errors are more visible
- Your code must compile and produce correct output
- Practice writing runnable code, not pseudocode

### Tip 3: Focus on Clean, Production-Quality Code

Meta engineers review code daily. They notice:
- Meaningful variable names (not `i`, `j`, `tmp`)
- Proper function decomposition
- Edge case handling
- Consistent style

### Tip 4: Product Sense Matters in System Design

Meta builds products used by billions. In system design, show product awareness:

```
"For the News Feed, the key user experience is seeing relevant content
within 2 seconds of opening the app. This means we need pre-computed
feeds cached at the edge, not generated on demand..."
```

### Tip 5: Show Impact in Behavioral

Meta's culture revolves around impact. Every behavioral answer should end with
a measurable result:

```
BAD:  "We launched the feature and it went well."
GOOD: "We launched to 100% of users in 3 weeks. Daily active usage increased
       by 12%, and the feature now accounts for 8% of total engagement."
```

### Tip 6: "Why Meta?" -- Have a Real Answer

```
WEAK: "Meta is a great company with amazing engineers."

STRONG: "I'm excited about Meta because of the scale and impact. Building
products used by 3 billion people means even a 0.1% improvement in feed
relevance affects millions of lives. I also admire Meta's investment in
AI and the Metaverse -- I want to be part of shaping how people interact
with technology in the next decade."
```

---

## Meta's Culture and Values

### Move Fast

Meta's original motto was "Move Fast and Break Things." While they have evolved
to "Move Fast with Stable Infrastructure," the bias toward speed remains.

**In interviews**: Show you can make decisions quickly, ship fast, and iterate.

### Focus on Impact

Every project at Meta is evaluated on its impact. "What moved?" is the
fundamental question.

**In interviews**: Quantify everything. User growth, revenue impact, latency
improvement, cost savings.

### Be Bold

Meta values engineers who take on ambitious projects, even at the risk of failure.

**In interviews**: Share stories about ambitious projects, even if they did not
fully succeed. Show you aim high.

### Be Open

Meta has a culture of transparency and open communication.

**In interviews**: Be honest about failures and mistakes. Show you give and
receive feedback well.

### Build Social Value

Meta cares about how technology impacts society.

**In interviews**: If relevant, mention considerations about user safety,
privacy, or societal impact in your system design and behavioral answers.

---

## Ninja and Pirate

Meta historically used an internal evaluation framework with two axes:

### Ninja (Technical Skill)
- Algorithm and coding ability
- System design capability
- Code quality and debugging skill
- Technical depth and breadth

### Pirate (Impact and Drive)
- Willingness to take risks
- Shipping speed
- Self-direction and initiative
- Ability to navigate ambiguity

The ideal Meta candidate scores high on BOTH axes -- technically excellent
AND impactful/driven. A pure "ninja" (technically brilliant but no drive)
or a pure "pirate" (driven but technically weak) is not ideal.

---

## Top 20 Meta Interview Questions

### Coding Questions (with Hints)

| # | Question | Difficulty | Hint |
|---|----------|-----------|------|
| 1 | Valid Palindrome II | Easy | Two pointers, allow one deletion |
| 2 | Merge Intervals | Medium | Sort by start, merge overlapping |
| 3 | Binary Tree Right Side View | Medium | BFS level-order, take last per level |
| 4 | Subarray Sum Equals K | Medium | Prefix sum + hash map |
| 5 | Lowest Common Ancestor of BT | Medium | Recursive DFS |
| 6 | Random Pick with Weight | Medium | Prefix sum + binary search |
| 7 | Add Binary | Easy | String manipulation or bit ops |
| 8 | Minimum Remove to Make Valid Parens | Medium | Stack for indices |
| 9 | Range Sum of BST | Easy | DFS with pruning |
| 10 | Vertical Order Traversal of BT | Hard | BFS + column tracking + sort |
| 11 | Nested List Weight Sum | Medium | DFS with depth tracking |
| 12 | Dot Product of Two Sparse Vectors | Easy | Hash map or two pointer on pairs |
| 13 | Buildings With an Ocean View | Medium | Monotonic stack or right-to-left scan |
| 14 | Making A Large Island | Hard | Union-Find or DFS + marking |
| 15 | K Closest Points to Origin | Medium | Quickselect or max heap |

### System Design Questions

| # | Question | Key Focus |
|---|----------|----------|
| 16 | Design Facebook News Feed | Feed ranking, pre-computation, caching |
| 17 | Design Instagram | Photo storage, CDN, feed generation |
| 18 | Design Facebook Messenger | Real-time messaging, delivery guarantees |
| 19 | Design a Live Streaming Platform | Low-latency video, CDN, chat |
| 20 | Design a Content Moderation System | ML pipeline, human review, policy enforcement |

---

## Meta Interview Timeline

### Ideal Preparation Timeline for Meta

```
6 weeks before: Start LeetCode (Meta-tagged problems, focus on SPEED)
5 weeks before: Practice solving 2 mediums in 40 minutes
4 weeks before: Start system design (Meta products: Feed, Messenger, Instagram)
3 weeks before: Behavioral prep (impact stories, "Why Meta?")
2 weeks before: Mock interviews (simulate 2-problem rounds)
1 week before:  Light review, rest, research Meta's recent news
Interview day:  Move fast. Solve clean. Show impact.
```

### After the Interview

| Timeline | What Happens |
|----------|-------------|
| Day 1 | Send thank-you email |
| Week 1 | Interviewers submit feedback |
| Week 1-2 | Hiring committee reviews |
| Week 2 | Recruiter calls with decision |
| Week 2-3 | Offer letter sent |
| Week 3-4 | Negotiation and acceptance |

---

## Meta Offer Structure

### Typical Meta Compensation

Meta's compensation is straightforward compared to Amazon:

```
Example: E5 (Senior SWE) Offer

Base Salary:  $215,000
Bonus:        15% of base = ~$32,000
RSU Grant:    $600,000 over 4 years = $150,000/year
Sign-on:      $50,000 (Year 1)
─────────────────────────────────────
Year 1 TC:    $447,000
Year 2+ TC:   $397,000
```

### RSU Vesting at Meta

Meta uses a standard vesting schedule:
```
Every quarter: 6.25% of total grant vests (4 years = 16 quarters)
```

This is the most employee-friendly vesting at any FAANG company. No cliff,
no back-loading. You start receiving shares from your first quarter.

### What to Negotiate

1. **RSU grant**: This is where Meta has the most room. Ask for 15-25% more shares.
2. **Sign-on bonus**: Usually flexible, especially in Year 1.
3. **Base salary**: Some room, but Meta has bands per level.
4. **Level**: If borderline E4/E5, push for E5 -- the TC difference is $100K+.

---

## Final Thoughts on Meta

Meta interviews reward engineers who are fast, clean, and impactful. The key
differentiators:

1. **Speed**: You must solve 2 problems per round. Practice timed solving.
2. **Clean code**: Your code runs on CoderPad. It must work.
3. **Impact focus**: Every behavioral answer should end with a metric.
4. **Product sense**: In system design, show you understand the product and its users.
5. **Move fast**: Show you ship quickly and iterate, not overplan.

Meta pays at the top of the market and has the most employee-friendly vesting
schedule. If you prepare for the speed-focused format, you will be well-positioned.

Good luck.
