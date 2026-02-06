# Complete Amazon Interview Guide (SDE-1 to SDE-3)

> Amazon interviews are unique because EVERY round -- including coding and
> system design -- includes behavioral questions tied to Amazon's Leadership
> Principles. If you do not prepare for LPs, you will fail, regardless of
> how good your coding is. This guide covers everything you need to know.

---

## Table of Contents

1. [Amazon's Interview Process](#amazons-interview-process)
2. [What Makes Amazon Different](#what-makes-amazon-different)
3. [Levels at Amazon](#levels-at-amazon)
4. [Amazon Leadership Principles In Practice](#amazon-leadership-principles-in-practice)
5. [Round-by-Round Breakdown](#round-by-round-breakdown)
6. [The Bar Raiser](#the-bar-raiser)
7. [Amazon-Specific Tips](#amazon-specific-tips)
8. [Top 20 Amazon Interview Questions](#top-20-amazon-interview-questions)
9. [Amazon Interview Timeline](#amazon-interview-timeline)
10. [Amazon Offer Structure](#amazon-offer-structure)

---

## Amazon's Interview Process

```
Application / Referral
       │
       ▼
Online Assessment (OA) — 2 coding problems + work simulation
       │
       ▼
Phone Screen (45-60 min, 1 coding + behavioral)
       │
       ▼
Onsite "LOOP" (4-5 rounds in one day)
  ├── Coding Round 1 + LP questions (60 min)
  ├── Coding Round 2 + LP questions (60 min)
  ├── System Design + LP questions (60 min) [SDE-2+]
  ├── Behavioral Deep Dive / LP round (60 min)
  └── Bar Raiser round (60 min)
       │
       ▼
Debrief (interviewers meet to discuss)
       │
       ▼
Offer (or rejection)
```

### Key Timelines

| Stage | Duration |
|-------|----------|
| Application to OA | 1-2 weeks |
| OA to Phone Screen | 1-2 weeks |
| Phone Screen to Onsite | 1-3 weeks |
| Onsite to Decision | 3-7 business days |
| Decision to Written Offer | 1-2 weeks |
| **Total: Application to Offer** | **4-8 weeks** |

Amazon moves faster than Google -- expect a quicker timeline.

---

## What Makes Amazon Different

### 1. Leadership Principles Are Everything

Amazon has 16 Leadership Principles (LPs), and they are not just posters on
the wall. EVERY interview round includes LP-based behavioral questions.
Even coding rounds start or end with 10-15 minutes of LP questions.

A candidate who solves every coding problem but fails the LP evaluation
will be rejected. A candidate who struggles with one coding problem but
demonstrates strong LPs may still get hired.

### 2. The Bar Raiser

Every Amazon interview loop includes a "Bar Raiser" -- a specially trained
interviewer from a DIFFERENT team. Their job is to ensure the candidate
raises the bar (is better than 50% of current Amazonians at that level).
The Bar Raiser has veto power.

### 3. The Debrief Is Collaborative

Unlike Google's Hiring Committee (which reviews written feedback), Amazon
interviewers meet in person to discuss the candidate. Each interviewer
presents their assessment, and the group decides together.

### 4. Every Round Has Two Parts

Every Amazon interview round has:
- **Technical portion** (30-40 min): Coding, system design, or domain expertise
- **Behavioral portion** (15-20 min): LP-based stories

You MUST prepare for both.

### 5. Compensation Is Unique

Amazon's RSU vesting is heavily back-loaded (5/15/40/40 over 4 years).
They compensate with large sign-on bonuses in Years 1-2. See the
[Offer Structure](#amazon-offer-structure) section.

---

## Levels at Amazon

| Level | Title | Years | TC Range (2026) | System Design? |
|-------|-------|-------|----------------|---------------|
| L4 | SDE-1 | 0-3 | $150-190K | No |
| L5 | SDE-2 | 2-6 | $200-300K | Yes |
| L6 | SDE-3 / Senior | 5-10 | $300-450K | Yes (harder) |
| L7 | Principal | 10+ | $400-650K | Yes (expert) |

**Note**: Amazon levels are different from Google levels. Amazon L5 roughly
maps to Google L4.

---

## Amazon Leadership Principles In Practice

### The 16 Leadership Principles

Amazon evaluates candidates against these principles. You need stories for
at least 10 of them. Here are all 16 with the type of question they generate
and preparation guidance:

#### 1. Customer Obsession
> Leaders start with the customer and work backwards.

**Question Type**: "Tell me about a time you went above and beyond for a customer/user."

**What They Want**: You put the customer first, even when it was inconvenient.
You proactively identified customer pain points and solved them.

**Example Story Angle**: "I noticed users were complaining about slow page loads.
Even though it was not on our sprint, I profiled the page, found 3 unoptimized
queries, and reduced load time by 60%. User complaints dropped to zero."

#### 2. Ownership
> Leaders think long term. They act on behalf of the entire company, not just their team.

**Question Type**: "Tell me about a time you took ownership of a problem outside your team's scope."

**What They Want**: You do not say "that's not my job." You see a problem and fix it,
even if it is not your responsibility.

#### 3. Invent and Simplify
> Leaders expect and require innovation and invention.

**Question Type**: "Tell me about a time you found a simpler solution to a complex problem."

**What They Want**: You are creative and look for simpler approaches rather than
complex solutions.

#### 4. Are Right, A Lot
> Leaders have strong judgment and good instincts.

**Question Type**: "Tell me about a time your judgment proved to be correct despite pushback."

**What They Want**: You can make good decisions with imperfect data.

#### 5. Learn and Be Curious
> Leaders are never done learning.

**Question Type**: "Tell me about something new you learned recently."

**What They Want**: You actively pursue knowledge beyond your immediate role.

#### 6. Hire and Develop the Best
> Leaders raise the performance bar with every hire.

**Question Type**: "Tell me about a time you mentored someone."

**What They Want**: You invest in others' growth and raise the team's capabilities.

#### 7. Insist on the Highest Standards
> Leaders have relentlessly high standards.

**Question Type**: "Tell me about a time you refused to compromise on quality."

**What They Want**: You push for excellence even when others want to cut corners.

#### 8. Think Big
> Leaders create and communicate a bold vision.

**Question Type**: "Tell me about a time you proposed an ambitious project."

**What They Want**: You think beyond incremental improvements.

#### 9. Bias for Action
> Speed matters in business. Many decisions are reversible.

**Question Type**: "Tell me about a time you made a decision quickly without all the data."

**What They Want**: You act decisively, not waiting for perfect information.

#### 10. Frugality
> Accomplish more with less.

**Question Type**: "Tell me about a time you delivered results with limited resources."

**What They Want**: You are resourceful and avoid unnecessary spending.

#### 11. Earn Trust
> Leaders listen attentively, speak candidly, and treat others respectfully.

**Question Type**: "Tell me about a time you had to earn someone's trust."

**What They Want**: You build trust through honesty, transparency, and reliability.

#### 12. Dive Deep
> Leaders operate at all levels. No task is beneath them.

**Question Type**: "Tell me about a time you had to dive into details to solve a problem."

**What They Want**: You do not just delegate -- you understand the technical details.

#### 13. Have Backbone; Disagree and Commit
> Leaders respectfully challenge decisions they disagree with, even when uncomfortable.

**Question Type**: "Tell me about a time you disagreed with your manager or team."

**What They Want**: You voice your opinion, but once a decision is made, you commit
fully (even if you disagree).

#### 14. Deliver Results
> Leaders focus on the key inputs and deliver them with the right quality and in a timely fashion.

**Question Type**: "Tell me about a time you delivered a project under a tight deadline."

**What They Want**: You get things done. You do not just plan -- you execute.

#### 15. Strive to Be Earth's Best Employer
> Leaders work to create a safer, more productive, and more diverse environment.

**Question Type**: "Tell me about a time you helped improve your team's work environment."

**What They Want**: You care about your team's well-being and growth.

#### 16. Success and Scale Bring Broad Responsibility
> Leaders create more than they consume and leave things better than they found them.

**Question Type**: "Tell me about a decision where you considered broader impact."

**What They Want**: You think about societal and environmental impact.

### LP Preparation Strategy

1. **Write 7-10 STAR stories** from your experience
2. **Map each story to 2-3 LPs** (each story can demonstrate multiple principles)
3. **Prioritize**: Customer Obsession, Ownership, Bias for Action, Deliver Results,
   Dive Deep, and Disagree & Commit are the most commonly asked
4. **Practice out loud**: Each story should take 2-3 minutes
5. **Include metrics**: "Reduced latency by 40%", not "improved performance"

---

## Round-by-Round Breakdown

### Online Assessment (OA)

**Format**: HackerRank platform, 70 minutes total

**Content**:
- 2 coding problems (30-35 min each)
- Difficulty: LeetCode Easy + Medium, or Medium + Medium
- Sometimes includes a "work simulation" section (multiple choice behavioral)

**Common OA Topics**:
- Arrays and Strings
- Hash Maps
- BFS/DFS (graph traversal)
- Sorting
- Two pointers

**Tips**:
- Complete both problems. Partial credit matters.
- Handle edge cases (empty input, single element).
- Optimize for passing test cases, not elegance.
- The work simulation tests LP alignment -- pick the "most Amazonian" answer.

### Phone Screen (1 Round, 45-60 minutes)

**Format**: Amazon Chime video call + online code editor

**Structure**:
```
0-5 min:   Introduction
5-10 min:  LP question #1 (always)
10-40 min: Coding problem
40-50 min: LP question #2 (sometimes)
50-60 min: Your questions
```

**Tips**:
- The LP question at the start is NOT a warm-up. It is a real evaluation.
- Use STAR format. Be specific. Include numbers.
- The coding problem is typically LeetCode Medium difficulty.
- Communicate your approach clearly before coding.

### Onsite / Loop (4-5 Rounds, 60 minutes each)

Every round at Amazon follows this pattern:

```
First 10-15 min: 1-2 Leadership Principle questions
Next 35-40 min:  Technical question (coding or system design)
Last 5-10 min:   Candidate's questions
```

#### Round 1: Coding + LP (60 min)

**LP Focus**: Usually Customer Obsession, Ownership, or Deliver Results

**Coding**: LeetCode Medium, sometimes with follow-up
- Common topics: Arrays, Strings, Trees, Graphs
- Clean code expected, but correctness matters most
- Discuss complexity before and after

#### Round 2: Coding + LP (60 min)

**LP Focus**: Usually Dive Deep, Bias for Action, or Learn and Be Curious

**Coding**: LeetCode Medium to Medium-Hard
- Different topic from Round 1
- May include a design-a-data-structure problem
- Expect follow-up questions ("What if the input is 10x larger?")

#### Round 3: System Design + LP (60 min) -- SDE-2+ Only

**LP Focus**: Usually Think Big, Invent and Simplify, or Insist on Highest Standards

**System Design**: Design an Amazon-scale system
- Common questions: Design an order processing system, Design a recommendation engine,
  Design a delivery tracking system, Design Amazon's product search

**What They Evaluate**:
1. Structured approach (requirements -> design -> deep dive)
2. Scale awareness (Amazon scale = millions of transactions per hour)
3. AWS-native thinking (DynamoDB, SQS, Lambda, S3 are welcome)
4. Trade-off discussion

#### Round 4: Behavioral Deep Dive / LP Round (60 min)

**Format**: All behavioral. No coding.

**What to Expect**: 5-6 LP questions in 45 minutes. They go DEEP:

```
Interviewer: "Tell me about a time you disagreed with your manager."
You: [STAR story, 2-3 minutes]
Interviewer: "What specifically did your manager think?"
Interviewer: "Why did you believe your approach was better?"
Interviewer: "What was the outcome?"
Interviewer: "What would you do differently today?"
Interviewer: "How did your relationship with your manager change after that?"
```

Expect 3-4 follow-up questions per story. They are testing depth and authenticity.

**Tips**:
- Prepare for follow-ups: Think about WHY you made each decision
- Do not memorize scripts -- interviewers can tell
- Be honest about failures and mistakes
- Always end with what you learned

#### Round 5: Bar Raiser (60 min)

See the next section.

---

## The Bar Raiser

### What Is a Bar Raiser?

A Bar Raiser (BR) is a senior Amazonian who has been specially trained to
evaluate candidates. Key facts:

- The BR is from a DIFFERENT team than the one hiring
- They have no stake in filling the position
- Their job is to ensure the candidate is better than 50% of current Amazonians at that level
- **The BR has veto power** -- if they say "no hire," you are not hired, even if everyone else says "hire"

### What the BR Evaluates

The BR does a mix of LP + technical (or LP-only for SDE-1). They look at:

1. **Overall signal strength**: Do you consistently demonstrate LPs?
2. **Culture fit**: Will you thrive in Amazon's high-bar culture?
3. **Long-term potential**: Will you grow and contribute over time?
4. **Calibration**: Are you better than 50% of current engineers at this level?

### How to Approach the BR Round

- Treat it like any other round -- do not be intimidated
- Be genuine and consistent with your stories from other rounds
- If the BR asks the same LP as another round, give a DIFFERENT story
- Show enthusiasm and cultural alignment

---

## Amazon-Specific Tips

### Tip 1: ALWAYS Tie Answers Back to Leadership Principles

Even in technical rounds, connect your approach to LPs:

```
"I'm going to start with a brute force solution first because I believe
in Bias for Action -- getting a working solution before optimizing."

"Let me add error handling here because Customer Obsession means the
user should never see an unhandled error."
```

### Tip 2: Use Metrics in Every Answer

Amazon is a data-driven company. Every story should include numbers:

```
BAD:  "I improved the service's performance."
GOOD: "I reduced p99 latency from 2 seconds to 200ms by implementing
       a Redis cache, which improved customer satisfaction scores by 15%."
```

### Tip 3: Show "Bias for Action"

Amazon values people who act quickly rather than analyzing endlessly:

```
"Rather than waiting for the perfect requirements, I built a prototype
in 3 days, shared it with 5 customers, and iterated based on their
feedback. We launched 2 weeks ahead of schedule."
```

### Tip 4: "Disagree and Commit" Is Critical

Show you can disagree respectfully but commit fully once a decision is made:

```
"I believed we should use PostgreSQL, but my tech lead preferred DynamoDB.
I made my case with data showing our access patterns were relational.
The team decided to go with DynamoDB. Once that decision was made, I
committed fully -- I wrote the migration scripts, updated the docs,
and even helped onboard the team to DynamoDB best practices."
```

### Tip 5: Prepare 2-3 Stories Per LP

If one story does not land well, you need a backup. Map your stories:

```
Story 1 (Service migration): Ownership, Deliver Results, Dive Deep
Story 2 (Bug investigation): Customer Obsession, Dive Deep, Highest Standards
Story 3 (Team conflict): Disagree and Commit, Earn Trust
Story 4 (New feature): Bias for Action, Invent and Simplify, Think Big
Story 5 (Mentoring): Hire and Develop, Customer Obsession
Story 6 (Tight deadline): Deliver Results, Frugality, Bias for Action
Story 7 (Learning new tech): Learn and Be Curious, Ownership
```

### Tip 6: Know Amazon's Business

Mentioning Amazon-specific context shows you care:
- Amazon's retail flywheel: Lower prices -> more customers -> more sellers -> lower prices
- AWS dominance in cloud computing
- Amazon's "Working Backwards" process (start with the press release)
- The "Two-Pizza Team" philosophy (small, autonomous teams)
- "Day 1" mentality (always acting like a startup)

---

## Top 20 Amazon Interview Questions

### Coding Questions (with Hints)

| # | Question | Difficulty | Hint |
|---|----------|-----------|------|
| 1 | Two Sum | Easy | Hash map for O(n) |
| 2 | LRU Cache | Medium | HashMap + Doubly Linked List |
| 3 | Number of Islands | Medium | BFS/DFS on grid |
| 4 | Merge K Sorted Lists | Hard | Min heap of size K |
| 5 | Rotting Oranges | Medium | Multi-source BFS |
| 6 | Word Ladder | Hard | BFS level-by-level |
| 7 | Reorder Data in Log Files | Medium | Custom comparator |
| 8 | K Closest Points to Origin | Medium | Max heap of size K |
| 9 | Product of Array Except Self | Medium | Prefix/suffix products |
| 10 | Min Cost to Connect Ropes | Medium | Min heap (greedy) |
| 11 | Partition Labels | Medium | Greedy with last occurrence |
| 12 | Critical Connections in Network | Hard | Tarjan's bridge-finding |
| 13 | Copy List with Random Pointer | Medium | Hash map or interleaving |
| 14 | Design File System | Medium | Trie or HashMap |
| 15 | Maximum Units on a Truck | Easy | Sort by units, greedy fill |

### System Design Questions

| # | Question | Key Focus |
|---|----------|----------|
| 16 | Design Amazon.com Product Page | Catalog service, reviews, recommendations |
| 17 | Design Amazon Order Processing | Distributed transactions, SQS, DynamoDB |
| 18 | Design a Delivery Tracking System | Real-time location, geospatial indexing |
| 19 | Design Amazon Prime Video | Video streaming, CDN, transcoding |
| 20 | Design a Recommendation Engine | Collaborative filtering, real-time personalization |

---

## Amazon Interview Timeline

### Ideal Preparation Timeline for Amazon

```
6 weeks before: Start LeetCode (Amazon-tagged mediums)
5 weeks before: Write all STAR stories, map to LPs
4 weeks before: Practice LP answers out loud (record yourself)
3 weeks before: Start system design (for SDE-2+)
2 weeks before: Mock interviews (coding + LP, simulate Amazon format)
1 week before:  Light review, rest, read Amazon's LP page one more time
Interview day:  Execute. Tie everything to LPs.
```

---

## Amazon Offer Structure

### Understanding Amazon's Unique Compensation

Amazon's RSU vesting is back-loaded. Here is how a typical SDE-2 offer might look:

```
Base Salary: $170,000
RSU Grant:   $200,000 (over 4 years)
Sign-on:     $50,000 (Year 1) + $40,000 (Year 2)
Bonus:       Typically none (Amazon doesn't do annual bonuses for most SDEs)

Year-by-Year Breakdown:
─────────────────────────────────────
Year 1:
  Base:     $170,000
  RSU (5%): $10,000
  Sign-on:  $50,000
  Total:    $230,000

Year 2:
  Base:     $170,000
  RSU (15%):$30,000
  Sign-on:  $40,000
  Total:    $240,000

Year 3:
  Base:     $170,000
  RSU (40%):$80,000
  Sign-on:  $0
  Total:    $250,000

Year 4:
  Base:     $170,000
  RSU (40%):$80,000
  Sign-on:  $0
  Total:    $250,000
─────────────────────────────────────
```

### Key Insight

Your Year 1-2 TC is heavily propped up by sign-on bonuses. Years 3-4 is where
the RSU cliff hits. Many Amazon employees leave at Year 2 or renegotiate (get
a "refresher" RSU grant).

### What to Negotiate

1. **Sign-on bonus**: Amazon is often flexible here
2. **RSU grant**: Ask for a larger grant (spread over 4 years)
3. **Base salary**: Amazon has a base salary cap (~$175-185K for most SDEs),
   so this has limited room
4. **Level**: If you are borderline SDE-2/SDE-3, push for the higher level

---

## Final Thoughts on Amazon

Amazon interviews are a unique blend of technical skill and behavioral alignment.
The key to success:

1. **Leadership Principles are non-negotiable.** Prepare 7-10 STAR stories.
2. **Every round has LPs.** Even coding rounds start with behavioral questions.
3. **The Bar Raiser has veto power.** Be consistent and genuine.
4. **Use metrics everywhere.** Amazon is data-driven.
5. **Show Ownership and Customer Obsession** in everything you say and do.
6. **Understand the compensation structure.** The back-loaded RSU vesting is
   unique and affects negotiation strategy.

Amazon rejects good engineers every day because they did not prepare for LPs.
Do not be that candidate.

Good luck.
