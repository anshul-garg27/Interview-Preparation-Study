# Mock Interview Guide

> The single highest-impact activity in interview preparation is doing mock interviews.
> Practicing alone builds knowledge. Mock interviews build performance under pressure.
> There is no substitute.

---

## Table of Contents

1. [Why Mock Interviews Matter](#why-mock-interviews-matter)
2. [How to Set Up Mock Interviews](#how-to-set-up-mock-interviews)
3. [Mock Interview Templates](#mock-interview-templates)
4. [Evaluation Rubrics](#evaluation-rubrics)
5. [How to Give Good Feedback](#how-to-give-good-feedback)
6. [Common Mock Interview Mistakes](#common-mock-interview-mistakes)
7. [Self-Mock: When You Have No Partner](#self-mock-when-you-have-no-partner)
8. [Mock Interview Schedule](#mock-interview-schedule)

---

## Why Mock Interviews Matter

### The Practice-Performance Gap

Solving problems alone at your desk is fundamentally different from solving
them while someone watches, times you, and asks follow-up questions.

**What solo practice builds**:
- Algorithm knowledge
- Pattern recognition
- Coding speed

**What mock interviews build**:
- Communication under pressure
- Time management with a real clock
- Handling ambiguity (clarifying questions)
- Recovering from mistakes gracefully
- Confidence in the interview format

### The Data

- Candidates who do 5+ mock interviews are 2-3x more likely to pass onsite interviews
- Mock interviews reduce interview anxiety by an estimated 60-70%
- Communication is the #1 reason candidates fail -- and it can only be practiced with another person
- Most candidates who "know the answer" still fail because they cannot communicate it in time

---

## How to Set Up Mock Interviews

### Option 1: Free Platforms

| Platform | How It Works | Quality |
|----------|-------------|---------|
| **Pramp** | Matched with a random peer, you interview each other | Variable (depends on partner) |
| **Interviewing.io** | Practice with anonymous engineers from FAANG | High (but limited free slots) |
| **LeetCode Discuss** | Find mock partners in discussion forums | Variable |
| **Discord/Reddit** | r/cscareerquestions, various coding Discord servers | Variable |

### Option 2: Paid Platforms

| Platform | How It Works | Cost | Quality |
|----------|-------------|------|---------|
| **Interviewing.io** (paid) | Practice with FAANG engineers | $100-225/session | Very High |
| **Exponent** | Behavioral + system design mocks | $99/mo | High |
| **Hello Interview** | AI-powered mock interviews | $39-99/mo | Good for practice |
| **Meetapro** | Book sessions with industry professionals | $50-200/session | High |

### Option 3: Friends & Colleagues

**Best option if available.** Here is how to organize it:

1. **Find a partner**: Ask a friend, colleague, or classmate who is also preparing
2. **Set a schedule**: Mock each other once a week (you interview them, they interview you)
3. **Use fresh problems**: Pick problems the other person has NOT seen
4. **Simulate real conditions**: Timer, video call, shared editor (CoderPad or Google Docs)
5. **Give honest feedback**: Use the rubrics below

### Option 4: DIY (Solo Mocks)

When you have no partner, you can still simulate interview conditions.
See [Self-Mock](#self-mock-when-you-have-no-partner) section below.

---

## Mock Interview Templates

### Template 1: 60-Minute Coding Round

**Setup**: Video call + shared code editor (CoderPad, Google Docs, or Replit)

```
TIME        ACTIVITY                             INTERVIEWER NOTES
─────────────────────────────────────────────────────────────────
0:00-0:05   Introduce the problem                Read the problem clearly.
                                                  Do NOT give hints yet.

0:05-0:10   Candidate asks clarifying questions   Note if they ask good
                                                  questions or jump to
                                                  coding immediately.

0:10-0:15   Candidate discusses approach          Do they think before
                                                  coding? Do they consider
                                                  multiple approaches?

0:15-0:40   Candidate writes code                 Observe:
                                                  - Code quality
                                                  - Variable naming
                                                  - Communication
                                                  - How they handle bugs

0:40-0:50   Testing & optimization                Do they test their code?
                                                  Can they identify edge
                                                  cases? Can they optimize?

0:50-0:55   Follow-up questions                   Ask about:
                                                  - Time/space complexity
                                                  - Alternative approaches
                                                  - How to handle scale

0:55-1:00   Feedback                              Use the rubric below.
                                                  Be specific and honest.
```

**Interviewer Script**:
```
"Hi, thanks for joining. I'm going to give you a coding problem, and I'd like
you to walk me through your thought process as you solve it. Feel free to ask
any clarifying questions before you start coding. Ready?"

[Give the problem]

"Take a moment to think about your approach. When you're ready, walk me
through what you're thinking."

[If stuck after 5 minutes]:
"What data structure do you think might be useful here?"

[If stuck after 10 minutes]:
"Have you considered using [hint]?"

[After coding]:
"Can you walk me through your code with this test case: [example]?"
"What's the time and space complexity?"
"How would you optimize this?"
```

**Recommended Problems** (pick one per mock):
- Medium: LRU Cache, Merge Intervals, Word Break, Kth Largest, Group Anagrams
- Hard: Trapping Rain Water, Median of Two Sorted Arrays, Alien Dictionary

### Template 2: 45-Minute System Design Mock

**Setup**: Video call + whiteboard tool (Excalidraw, Miro, or Google Docs)

```
TIME        ACTIVITY                             INTERVIEWER NOTES
─────────────────────────────────────────────────────────────────
0:00-0:03   Introduce the problem                "Design [System X]"
                                                  Keep it open-ended.

0:03-0:08   Requirements gathering                Do they ask about:
                                                  - Functional requirements?
                                                  - Non-functional (scale)?
                                                  - Constraints?

0:08-0:13   Back-of-envelope estimation           Can they estimate:
                                                  - QPS
                                                  - Storage
                                                  - Bandwidth

0:13-0:28   High-level design                     Do they draw:
                                                  - Clear components
                                                  - Data flow arrows
                                                  - Databases
                                                  - Caches
                                                  - Load balancers

0:28-0:40   Deep dive (1-2 components)            Can they go deep on:
                                                  - Database schema
                                                  - API design
                                                  - Specific algorithm
                                                  - Scaling strategy

0:40-0:45   Trade-offs & wrap-up                  Can they discuss:
                                                  - Trade-offs made
                                                  - Bottlenecks
                                                  - How to monitor
                                                  - What they'd do next
```

**Interviewer Script**:
```
"Today I'd like you to design [System]. Let's start with understanding
the requirements. What questions do you have?"

[After requirements]:
"Let's do some quick math. How many users are we designing for?"

[During high-level design]:
"Can you walk me through the data flow for [key use case]?"

[For deep dive]:
"Let's dive deeper into [component]. How would you handle [specific challenge]?"

[Wrap-up]:
"What are the main trade-offs in your design?"
"Where are the bottlenecks? How would you address them?"
```

**Recommended Problems** (pick one per mock):
- URL Shortener, Twitter Feed, WhatsApp, Uber, Netflix, Rate Limiter

### Template 3: 45-Minute Behavioral Mock

**Setup**: Video call (no shared editor needed)

```
TIME        ACTIVITY                             INTERVIEWER NOTES
─────────────────────────────────────────────────────────────────
0:00-0:02   Warm-up                              "Tell me about yourself"
                                                  (2-minute pitch)

0:02-0:10   Story 1: Technical challenge          "Tell me about the most
                                                  challenging technical
                                                  problem you've solved."

0:10-0:18   Story 2: Conflict/disagreement        "Tell me about a time you
                                                  disagreed with a teammate
                                                  or manager."

0:18-0:26   Story 3: Leadership/initiative         "Tell me about a time you
                                                  went above and beyond or
                                                  took initiative."

0:26-0:34   Story 4: Failure/learning             "Tell me about a time
                                                  you failed. What did you
                                                  learn?"

0:34-0:40   Story 5: Company-specific             For Amazon: LP question
                                                  For Google: Googleyness
                                                  For Meta: Impact question

0:40-0:45   Feedback                              Use behavioral rubric.
```

**Interviewer Follow-Up Questions** (ask 2-3 per story):
```
- "What was YOUR specific role in that?"
- "What would you do differently if you could do it again?"
- "How did you measure the impact?"
- "What did your teammates think?"
- "What did you learn from that experience?"
- "How long did that take?"
- "What was the outcome?"
```

**STAR Format Reminder**:
```
S - Situation: Set the context (1-2 sentences)
T - Task: What was your responsibility? (1 sentence)
A - Action: What did YOU specifically do? (3-5 sentences, most important)
R - Result: What was the measurable outcome? (1-2 sentences)
```

### Template 4: 90-Minute Machine Coding Mock

**Setup**: Video call + full IDE (candidate uses their own IDE, screen shares)

```
TIME        ACTIVITY                             INTERVIEWER NOTES
─────────────────────────────────────────────────────────────────
0:00-0:05   Give the problem statement            Hand over requirements.
                                                  Answer clarifying Qs.

0:05-0:15   Candidate reads, asks questions       Do they understand the
                                                  full scope? Do they
                                                  identify edge cases?

0:15-0:25   Design phase                          Do they plan before
                                                  coding? Class diagram?
                                                  Key abstractions?

0:25-0:75   Implementation                        Observe:
                                                  - Code organization
                                                  - OOP usage
                                                  - Design patterns
                                                  - Handling extensions

0:75-0:85   Testing & demo                        Does the code run?
                                                  Does it handle edge
                                                  cases? Is it demo-able?

0:85-0:90   Feedback & discussion                 Discuss design choices.
                                                  What would they change?
```

**Recommended Problems** (pick one per mock):
- Parking Lot System (full implementation)
- Snake and Ladder Game
- Vending Machine
- Splitwise (expense sharing)
- Tic-Tac-Toe with AI opponent

---

## Evaluation Rubrics

### Coding Round Rubric

| Criteria | 1 (Poor) | 2 (Below) | 3 (Average) | 4 (Good) | 5 (Excellent) |
|----------|----------|-----------|-------------|----------|---------------|
| **Problem Understanding** | Did not read problem carefully, missed constraints | Missed some edge cases | Understood problem, asked basic questions | Asked good clarifying questions | Identified non-obvious constraints and edge cases |
| **Approach** | No clear approach, jumped to code | Single approach, no alternatives | Reasonable approach, mentioned complexity | Multiple approaches considered, chose well | Optimal approach with clear justification |
| **Code Quality** | Messy, hard to read, many bugs | Some structure, several bugs | Readable, minor bugs | Clean, well-structured, runs correctly | Production-quality, handles all edge cases |
| **Communication** | Silent coding, no explanation | Explained only when asked | Spoke occasionally while coding | Consistent communication of thought process | Clear, structured narration throughout |
| **Testing** | Did not test | Tested with given example only | Tested 2-3 cases | Tested edge cases proactively | Comprehensive testing, found and fixed bugs |
| **Time Management** | Ran out of time, incomplete | Finished late, solution incomplete | Finished on time, basic solution | Finished with time to optimize | Finished early, discussed follow-ups |

**Scoring**: Add up points. 24-30 = Strong Hire, 18-23 = Hire, 12-17 = Lean No, 6-11 = No Hire

### System Design Rubric

| Criteria | 1 (Poor) | 3 (Average) | 5 (Excellent) |
|----------|----------|-------------|---------------|
| **Requirements** | Jumped to design without gathering requirements | Asked basic functional requirements | Gathered functional + non-functional, clarified scope |
| **Estimation** | No estimation | Basic QPS calculation | Thorough: QPS, storage, bandwidth, with clear math |
| **High-Level Design** | Missing key components | Reasonable diagram with main components | Clean architecture with all necessary components |
| **Deep Dive** | Surface-level on all components | Reasonable depth on 1 area | Expert-level depth on 2+ areas |
| **Trade-offs** | No trade-offs discussed | Mentioned 1-2 trade-offs | Discussed multiple trade-offs with clear reasoning |
| **Communication** | Interviewer had to drive the discussion | Adequate explanation | Led the discussion, drew clear diagrams, structured |

### Behavioral Rubric

| Criteria | 1 (Poor) | 3 (Average) | 5 (Excellent) |
|----------|----------|-------------|---------------|
| **Structure** | Rambling, no clear format | Used STAR loosely | Clear STAR format for every story |
| **Specificity** | Vague, hypothetical answers | Some specific details | Concrete details, names, numbers, dates |
| **Self-Awareness** | No reflection, blamed others | Some reflection | Deep reflection, growth mindset, lessons learned |
| **Impact** | No measurable result | Qualitative result | Quantifiable result with business impact |
| **Authenticity** | Sounded rehearsed or generic | Somewhat genuine | Genuine, passionate, believable |

---

## How to Give Good Feedback

### The Feedback Sandwich (But Better)

After a mock interview, give feedback in this order:

1. **What went well** (specific, not vague "good job")
   - "Your approach to the problem was systematic -- I liked how you considered
     hash map vs. sorting before choosing an approach."

2. **What to improve** (actionable, not vague "do better")
   - "You went silent for 3 minutes while debugging. In a real interview,
     narrate what you're doing: 'I think there might be an off-by-one error
     in this loop, let me trace through...'"

3. **One top priority** (the single most impactful change)
   - "The number one thing to work on: Start testing your code before you
     say 'I'm done.' You had a bug in the edge case that you would have
     caught with a simple trace-through."

### Feedback Template

```markdown
## Mock Interview Feedback
Date: [Date]
Type: [Coding / System Design / Behavioral]
Problem: [Problem Name]

### What Went Well
1.
2.
3.

### What Needs Improvement
1.
2.
3.

### Top Priority for Next Mock
-

### Score (Using Rubric Above)
- [Criteria 1]: X/5
- [Criteria 2]: X/5
- ...
- Total: X/30

### Would This Be a Hire?
[ ] Strong Hire
[ ] Hire
[ ] Lean No Hire
[ ] No Hire
```

---

## Common Mock Interview Mistakes

### Mistake 1: Not Simulating Real Conditions
Using your favorite IDE with autocomplete, Stack Overflow open in another tab,
and no time pressure is NOT a mock interview. Use CoderPad or Google Docs.
Set a timer. Close all other tabs.

### Mistake 2: Always Picking Easy Problems
If you only mock with problems you can solve, you are not preparing for
the real thing. Include problems you might struggle with.

### Mistake 3: Skipping the Communication Part
Solving the problem silently and then saying "done" is a fail in real interviews.
Practice narrating your thought process the ENTIRE time.

### Mistake 4: Not Doing Enough Mocks
One mock interview is not enough. Aim for:
- Month 2: 2 mocks (one coding, one system design)
- Month 3: 4-6 mocks (mix of all types)
- Final week: 1 full-day onsite simulation

### Mistake 5: Not Acting on Feedback
If your mock partner says "you need to communicate more," and you do not
practice communication in your next mock, you are wasting both your time.

### Mistake 6: Only Doing Coding Mocks
System design and behavioral mocks are equally important. Many candidates
do 10 coding mocks and 0 behavioral mocks, then fail the behavioral round.

---

## Self-Mock: When You Have No Partner

When you cannot find a mock partner, simulate the experience:

### Method 1: Record Yourself

1. Pick a problem you have NOT seen before
2. Start a screen recording (OBS, Loom, or QuickTime)
3. Set a 45-minute timer
4. Solve the problem while talking out loud (explain EVERYTHING)
5. Stop the timer
6. Watch the recording and score yourself using the rubric

**What to Watch For**:
- How long were you silent? (Aim for < 30 seconds of silence at a time)
- Did you ask clarifying questions before coding?
- Was your code readable?
- Did you test before saying "done"?

### Method 2: Timed Problem Sets

1. Pick 2 medium problems you have not seen
2. Set a 60-minute timer for both
3. Solve on Google Docs or CoderPad (NOT your IDE)
4. Talk out loud as if someone were watching

### Method 3: AI Mock Interviews

Use AI tools for behavioral and system design practice:
- Hello Interview (dedicated interview AI)
- ChatGPT (prompt it to be an interviewer)
- Voice recording apps to practice verbal communication

### Method 4: Mirror Practice (Behavioral)

1. Stand in front of a mirror
2. Ask yourself a behavioral question out loud
3. Answer using STAR format, watching your body language
4. Time yourself (each answer should be 2-3 minutes)

---

## Mock Interview Schedule

### Recommended Schedule Over 3 Months

```
Month 1 (Foundation - Focus on solo practice):
  Week 4: First mock interview (coding, with a friend or Pramp)

Month 2 (Core):
  Week 5: Mock #2 (coding, harder problem)
  Week 7: Mock #3 (system design)
  Week 8: Mock #4 (behavioral)

Month 3 (Polish):
  Week 9:  Mock #5 (coding, recorded)
  Week 10: Mock #6 (full 2-round simulation: coding + behavioral)
  Week 11: Mock #7 (full 3-round simulation: coding + system design + behavioral)
  Week 11: Mock #8 (company-specific mock)
  Week 12: Rest / light review
```

### Full-Day Onsite Simulation (Week 11)

If possible, do one full-day mock onsite:

```
9:00 AM  - Coding Round 1 (45 min + 15 min feedback)
10:00 AM - Coding Round 2 (45 min + 15 min feedback)
11:00 AM - System Design (45 min + 15 min feedback)
12:00 PM - Lunch break (30 min)
12:30 PM - Behavioral Round (45 min + 15 min feedback)
1:30 PM  - Debrief and overall feedback (30 min)
```

This simulates the stamina required for a real onsite and helps you identify
how your performance degrades over multiple rounds.

---

## Key Takeaways

1. **Mock interviews are non-negotiable.** They are the bridge between "I know
   the answer" and "I can perform under pressure."

2. **Variety matters.** Do coding, system design, AND behavioral mocks.

3. **Get real feedback.** Self-assessment is biased. An external observer
   catches things you miss.

4. **Simulate real conditions.** Timer, shared editor, video call, no IDE
   autocomplete, no browser open.

5. **Act on feedback.** Each mock should target a specific improvement area.

6. **Do at least 6-8 mocks** before your first real interview at a target company.

Start scheduling mocks today. Your future self will thank you.
