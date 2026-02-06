# Your Personal Story Bank Template

> Prepare 8 stories. Practice them until they feel natural, not memorized.
> Each story should be reusable for 3-4 different question types.

---

## How to Use This Template

1. **Fill in the blanks** with your own experiences
2. **Write it out fully** first, then practice saying it in 2-3 minutes
3. **Highlight the "I" statements** -- these are your differentiators
4. **Add real numbers** to every result
5. Review the "What to Emphasize" and "What NOT to Say" for each story type

---

## Story 1: Leadership Under Pressure

### Template

```
Situation: At [Company], during [project/quarter/incident], [what was happening
that created pressure -- deadline, outage, resource constraint, high stakes].

Task: I was responsible for [specific deliverable/outcome] with [constraint --
tight timeline, limited resources, high visibility]. The stakes were [what would
happen if we failed].

Action:
  1. First, I [assessed the situation / identified the root cause / gathered data].
     I did this by [specific method].
  2. Then, I [proposed a plan / made a key decision]. I chose this approach
     because [reasoning].
  3. I [organized the team / delegated tasks / set up a war room]. Specifically,
     I [concrete action with details].
  4. When [obstacle or complication arose], I [how you adapted]. This required
     [what it took from you -- late nights, difficult conversations, creative
     problem solving].
  5. I [drove the execution to completion] by [specific actions in the final push].

Result: [Quantifiable outcome -- percentage improvement, revenue impact, time
saved, users affected]. Additionally, [secondary impact -- team morale, process
improvement, adoption by other teams].

Learning: From this, I learned that [key takeaway about leadership under pressure].
```

### What to Emphasize
- Your decision-making process under stress
- How you rallied and organized others
- Specific actions YOU took (not the team in general)
- How you stayed calm and methodical despite pressure
- The measurable outcome

### What NOT to Say
- "I just worked harder" (not a strategy)
- "I told everyone what to do" (sounds dictatorial)
- "It was stressful but we got through it" (too vague)
- Anything that suggests panic or indecision

### Example (Filled Version)

```
Situation: At Stripe, during Black Friday week, our payment processing latency
spiked to 3x normal levels, causing transaction timeouts for merchants.

Task: As the on-call senior engineer, I was responsible for diagnosing and
resolving the issue before the peak shopping period, which was 18 hours away.
If unresolved, we estimated $5M+ in lost merchant revenue.

Action:
  1. First, I set up a war room and pulled in the 3 most relevant engineers.
     I created a shared doc to track hypotheses and findings in real-time.
  2. I analyzed the latency distribution and discovered that P99 latency was
     10x worse than P50, suggesting a specific subset of requests was the
     problem. I wrote a query to isolate these requests.
  3. I identified that a recent config change had disabled connection pooling
     for international transactions. I proposed two options to my manager: a
     quick rollback or a targeted fix. I recommended the rollback for speed.
  4. When the rollback caused a secondary issue with currency conversion caching,
     I quickly wrote a hotfix that restored the cache while keeping the
     connection pooling active.
  5. I monitored the system for the next 6 hours, set up automated alerts for
     latency thresholds, and wrote a postmortem before going to sleep.

Result: Latency returned to normal within 2 hours. We handled Black Friday with
zero payment timeouts. The postmortem I wrote led to a new config change review
process that prevented 3 similar incidents in the following quarter.

Learning: I learned that in crisis situations, having a structured approach
(war room, shared tracking, clear decision framework) is more valuable than
individual heroics. Speed matters, but so does preventing the next incident.
```

### Questions This Story Can Answer
- "Tell me about a time you led under pressure"
- "Describe a time you had to make a quick decision"
- "Tell me about a time you dealt with a production issue"
- "Describe a time you had to coordinate across a team urgently"

---

## Story 2: Conflict with a Teammate

### Template

```
Situation: At [Company], while working on [project], [teammate/peer] and I
disagreed about [what -- technical approach, priority, process, design decision].
This was important because [stakes].

Task: I needed to [resolve the disagreement / find a path forward] while
[maintaining the relationship / keeping the project on track / meeting the
deadline].

Action:
  1. First, I [sought to understand their perspective]. I scheduled a [1:1 /
     coffee chat / call] and asked them to walk me through their reasoning.
  2. I realized that [what you learned from their perspective -- they had a
     valid point about X / their concern was actually about Y].
  3. I [proposed a compromise / found data to resolve the disagreement /
     suggested a structured way to decide]. Specifically, I [concrete action].
  4. When [what happened during the resolution process], I [how you handled it
     with emotional intelligence].
  5. We agreed to [the resolution -- your approach, their approach, a hybrid,
     or a data-driven decision].

Result: [Outcome of the project]. Our relationship [improved / remained strong]
because [why]. [Any lasting impact -- process change, better collaboration
going forward].

Learning: I learned that [insight about conflict resolution -- e.g., most
conflicts come from different assumptions, not bad intentions].
```

### What to Emphasize
- That you LISTENED first before advocating
- Your emotional intelligence and empathy
- That you sought a win-win, not to "win" the argument
- The relationship outcome, not just the project outcome
- Maturity and professionalism

### What NOT to Say
- "They were wrong and I was right" (even if true, frame it differently)
- "I went to our manager to resolve it" (shows you cannot resolve conflicts directly)
- "It was not a big deal" (then why are you telling this story?)
- Speaking negatively about the other person's character
- "I just let it go" (shows avoidance, not resolution)

### Example (Filled Version)

```
Situation: At my previous company, I was working on a search service redesign
with a colleague who was equally senior. He strongly advocated for using
Elasticsearch, while I believed Solr was a better fit given our team's
expertise and our specific use case.

Task: I needed to resolve this disagreement quickly because the architecture
decision was blocking the entire project, and we had a 6-week delivery target.

Action:
  1. First, I invited him to lunch and asked him to explain his Elasticsearch
     preference in depth. I took notes and genuinely tried to understand his
     reasoning.
  2. I realized his main argument was about long-term scalability and community
     momentum, which were valid points I had not fully considered.
  3. I proposed that we each spend 2 days building a proof-of-concept with our
     preferred solution against our actual dataset, and evaluate both on 5
     agreed-upon criteria: performance, operational complexity, learning curve,
     community support, and feature fit.
  4. After the evaluation, Elasticsearch performed better on 3 of 5 criteria.
     I acknowledged this openly in our team meeting and supported moving forward
     with Elasticsearch.
  5. I offered to pair-program with him on the initial setup since he had more
     Elasticsearch experience, which helped me learn quickly and kept us on track.

Result: We delivered the search service on time. The Elasticsearch choice proved
correct -- we got 40% better query performance than our old system. My colleague
and I became close collaborators after this experience, and he later said that
my openness to changing my mind earned his respect.

Learning: I learned that the best technical decisions come from structured
evaluation, not debate. And that being willing to change your mind is a
strength, not a weakness.
```

### Questions This Story Can Answer
- "Tell me about a conflict with a coworker"
- "Describe a time you had to compromise"
- "Tell me about a time someone disagreed with your technical approach"
- "How do you handle disagreements?"

---

## Story 3: Failed Project / Mistake I Made

### Template

```
Situation: At [Company], I was working on [project/feature] that [context --
what was the goal, why it mattered].

Task: I was responsible for [your specific role/deliverable]. The expectation
was [what success looked like].

Action:
  1. I [what you did that led to the failure -- made an assumption,
     underestimated complexity, skipped a step, miscommunicated].
  2. As a result, [what went wrong -- deadline missed, bug in production,
     wrong direction, customer impact].
  3. When I realized the mistake, I [immediate response -- owned it,
     communicated to stakeholders, assessed the damage].
  4. I then [recovery actions -- fixed the issue, created a plan,
     brought in help, mitigated the impact].
  5. After the situation was resolved, I [prevention actions -- postmortem,
     process change, documentation, automated checks].

Result: [Honest result -- what was the impact, even if negative]. However,
[what you salvaged / silver lining -- the recovery went well, the process
improvement prevented future issues, trust was maintained because of
transparency].

Learning: This taught me [genuine, specific lesson]. I have since [how you
have applied this lesson -- concrete change in behavior or process].
```

### What to Emphasize
- **Ownership.** This is the #1 thing they want to hear. YOU made the mistake. You do not blame others.
- The specific lesson learned and how you changed
- Your recovery process (shows resilience)
- That you took proactive steps to prevent recurrence
- Emotional honesty ("I was disappointed in myself")

### What NOT to Say
- "It was not really my fault" (NO. Own it.)
- "It all worked out fine" (minimizes the failure)
- A failure that is actually a humble-brag ("I worked too hard")
- A failure with no consequences (not really a failure)
- A failure from 10+ years ago (too distant to be relevant)

### Example (Filled Version)

```
Situation: At my company, I was leading the migration of our user database
from PostgreSQL to a new sharded architecture to support our growth from
5M to 50M users.

Task: I was responsible for the migration plan, execution, and ensuring zero
downtime during the cutover.

Action:
  1. I underestimated the complexity of migrating user sessions. I assumed
     our session store was stateless, but it actually had dependencies on the
     old database's connection pooling behavior.
  2. During the cutover, approximately 8% of active users were logged out
     unexpectedly. This happened during business hours in our largest market.
  3. When I saw the error alerts, I immediately rolled back the migration and
     notified my manager and our customer support team within 10 minutes. I
     sent a transparent message to the team Slack channel explaining what
     happened and that I was taking responsibility.
  4. I spent the next week analyzing the session dependency, redesigning the
     migration to handle sessions separately, and building a simulation tool
     that could replay real traffic patterns against the new architecture.
  5. I wrote a detailed postmortem, presented it to the engineering org, and
     proposed a "migration readiness checklist" that included session analysis,
     traffic replay, and graduated rollout requirements.

Result: The 8% user disruption translated to about 400K users affected for
approximately 15 minutes. We received 200+ support tickets. However, the
second migration attempt 2 weeks later was flawless. The migration readiness
checklist I created was adopted as a standard process and was used for 4
subsequent migrations without incident.

Learning: I learned to never assume I understand a system's hidden dependencies.
Now, before any migration, I do a dependency mapping exercise that traces data
flow end-to-end, including session management, caching layers, and background
jobs. This has become second nature to me.
```

### Questions This Story Can Answer
- "Tell me about a time you failed"
- "Tell me about your biggest mistake"
- "Describe a time something did not go as planned"
- "Tell me about a time you learned from failure"

---

## Story 4: Delivered Under Tight Deadline

### Template

```
Situation: At [Company], [what created the tight deadline -- client demand,
competitive pressure, regulatory requirement, executive commitment].

Task: I needed to deliver [specific deliverable] by [deadline], which was
[how much shorter than normal -- "half the usual timeline" / "2 weeks instead
of the usual 6"]. [What made it hard -- scope, dependencies, team size].

Action:
  1. I [assessed what was feasible and what had to be cut]. I created a
     [prioritized plan / MVP scope / phased approach].
  2. I [communicated the plan to stakeholders]. I was transparent about
     [trade-offs -- what we would NOT include and why].
  3. I [organized the execution -- broke work into parallel streams,
     removed blockers, made quick decisions to keep momentum].
  4. When [inevitable complication], I [how you adapted without derailing
     the timeline].
  5. I [what you personally built/did to contribute, not just managed].

Result: We delivered [what] by [when]. [Quantifiable impact]. The client/
stakeholder [reaction]. [Any follow-up -- we added the cut features later,
the solution held up, etc.].

Learning: I learned that [insight about delivery under pressure -- scope
management, communication, trade-offs].
```

### What to Emphasize
- How you scoped and prioritized (not just "worked harder")
- Your communication with stakeholders about trade-offs
- That you CHOSE to cut scope rather than cut quality
- Your organizational and planning skills
- That you personally contributed, not just delegated

### What NOT to Say
- "I just worked 80-hour weeks" (not sustainable, not a strategy)
- "We cut corners to make it work" (red flag for quality)
- "I did everything myself" (not scalable, not a team player)
- Results that suggest the deadline was not actually tight

### Example (Filled Version)

```
Situation: At my company, our largest enterprise client threatened to churn
if we did not deliver a real-time analytics dashboard within 3 weeks. This
was a feature on our Q3 roadmap with a 10-week estimate.

Task: I was the tech lead responsible for delivering a working analytics
dashboard in 3 weeks with a team of 3 engineers, while our normal delivery
timeline for this feature was 10 weeks.

Action:
  1. I spent the first day defining an MVP scope with our PM and the client.
     I identified that 3 of the 8 planned chart types covered 90% of the
     client's actual use cases, so I proposed delivering those 3 first.
  2. I communicated to my manager and the sales team exactly what would and
     would not be included, with a written plan showing the Phase 2 additions
     for weeks 4-10.
  3. I broke the work into 3 parallel streams -- one engineer on data pipeline,
     one on the API layer, and I took the frontend dashboard and the integration
     testing.
  4. In week 2, we discovered the data pipeline needed a schema change that
     required DBA approval. Instead of waiting, I built a temporary adapter
     layer that worked with the existing schema, and scheduled the proper
     migration for Phase 2.
  5. I personally wrote 60% of the frontend code and did all the integration
     testing. I also set up a daily 10-minute standup specifically for this
     project to catch blockers early.

Result: We delivered the MVP dashboard 1 day early. The client renewed their
$800K annual contract and specifically mentioned the dashboard in their renewal
decision. The remaining features were delivered in Phase 2 on the original
10-week timeline.

Learning: I learned that tight deadlines are actually a forcing function for
good prioritization. The MVP we built in 3 weeks was actually better-focused
than the 10-week plan because we were forced to ruthlessly prioritize what
the client actually needed.
```

### Questions This Story Can Answer
- "Tell me about a time you delivered under a tight deadline"
- "Describe a time you had to prioritize"
- "Tell me about a time you had to make trade-offs"
- "How do you handle competing priorities?"

---

## Story 5: Disagreed with Manager/Lead

### Template

```
Situation: At [Company], my manager/tech lead [proposed/decided] [what --
technical direction, process change, priority, resource allocation] that I
believed was [why you disagreed -- risky, suboptimal, wrong approach].

Task: I needed to [express my disagreement constructively] while [maintaining
respect and the relationship / without undermining their authority].

Action:
  1. I [prepared my case before speaking up]. I gathered [data, examples,
     analysis] to support my perspective.
  2. I [requested a private conversation / brought it up in a 1:1] rather
     than [challenging them publicly / just going along with it].
  3. I [presented my concerns with data and reasoning]. I said something like
     "[specific framing -- 'I want to share a concern about X because I have
     seen Y']".
  4. I [listened to their reasoning]. I learned that [what they knew that you
     did not / their constraints / their perspective].
  5. We [reached a resolution -- they changed their mind / you changed yours /
     you found a compromise / you disagreed and committed].

Result: [What happened]. [Whether your concern was validated or not]. [Impact
on the project/team]. [Impact on your relationship with the manager].

Learning: I learned that [insight about disagree-and-commit, navigating
hierarchy, constructive dissent].
```

### What to Emphasize
- That you were respectful and professional
- That you used data and reasoning, not emotion
- That you brought it up privately, not publicly
- That you were willing to commit even if overruled
- The relationship remained healthy or improved

### What NOT to Say
- "My manager was an idiot" (never)
- "I went over their head" (unless they asked you to)
- "I was obviously right" (even if you were, show humility)
- "I just went along with it because they are the boss" (shows no backbone)

### Example (Filled Version)

```
Situation: At my company, my engineering manager decided we should rewrite
our notification service from scratch using a new framework, which would take
an estimated 3 months. I believed we should incrementally refactor the existing
service, which I estimated at 6 weeks.

Task: I needed to share my concerns about the full rewrite without being
insubordinate or dismissive of my manager's vision.

Action:
  1. I spent a day analyzing both approaches. I created a comparison document
     with estimated timelines, risk factors, and a breakdown of what we would
     gain and lose with each approach.
  2. I requested a 30-minute 1:1 with my manager and said, "I have been
     thinking about the notification service approach and would love to share
     some analysis I put together."
  3. I walked through my comparison, specifically highlighting that the rewrite
     carried a risk of 2-3 months of zero feature delivery for our users, while
     the refactor approach could deliver incremental improvements every 2 weeks.
  4. My manager explained that the new framework was a strategic bet the VP had
     endorsed, and that there were benefits I had not considered around team
     hiring and long-term maintainability. I had not been aware of this context.
  5. We agreed on a hybrid: start with a refactor of the highest-risk components
     (my suggestion), then migrate to the new framework incrementally (their
     vision), avoiding the big-bang rewrite risk.

Result: The hybrid approach delivered a 40% improvement in notification
reliability within 6 weeks (from the refactor), and the full framework
migration was completed in 4 months (better than the original 3-month estimate
for the rewrite because we had cleaner code to migrate). My manager later told
me he appreciated that I pushed back with data rather than just opinions.

Learning: I learned that disagreements are most productive when you bring data,
propose alternatives, and genuinely listen to the other perspective. Often the
best solution is a synthesis of both views.
```

### Questions This Story Can Answer
- "Tell me about a time you disagreed with your manager"
- "Describe a time you pushed back on a decision"
- "How do you handle disagreements with authority?"
- "Tell me about a time you had to influence without authority"

---

## Story 6: Went Above and Beyond

### Template

```
Situation: At [Company], [the normal expectation / baseline context]. [What
you noticed that others might have missed or ignored].

Task: My actual responsibility was [the minimum expected]. However, I saw
an opportunity to [what you could do beyond the minimum -- improve a process,
help a colleague, create something new, prevent a future problem].

Action:
  1. I [took initiative to go beyond my defined role]. I did this on my own
     because [motivation -- you cared about quality, team, users, etc.].
  2. I [specific above-and-beyond action 1].
  3. I [specific above-and-beyond action 2].
  4. I [how you balanced this with your regular responsibilities -- did not
     neglect your core work].

Result: [Impact of going above and beyond]. This [unexpected positive outcome
-- saved time/money, delighted a customer, helped a colleague succeed,
prevented a future issue].

Learning: I learned that [insight about initiative, ownership, impact].
```

### What to Emphasize
- That it was YOUR initiative (no one asked you to do it)
- That you still met your core responsibilities
- The positive impact on others (team, users, company)
- Genuine motivation (caring, not just trying to get promoted)

### What NOT to Say
- Making it sound like you are complaining about doing extra work
- Implying others should have done it but did not (blaming)
- Exaggerating the impact of what you did
- Making it about getting recognition

### Example (Filled Version)

```
Situation: At my company, our onboarding process for new engineers was ad hoc.
Each new hire was paired with a buddy, but there was no structured guide, and
it typically took new engineers 4-6 weeks to submit their first meaningful PR.

Task: My actual job was backend development on the data pipeline team.
Onboarding was not my responsibility at all. But after I onboarded our
third new hire in 6 months and watched them struggle with the same issues
I had struggled with, I decided to fix it.

Action:
  1. I spent my evenings over two weeks creating a comprehensive onboarding
     guide: environment setup, architecture overview, common debugging workflows,
     and a "first week project" that touched all major system components.
  2. I recorded 5 short video walkthroughs of our codebase -- 10 minutes each,
     covering the 5 things every new engineer asks about in their first week.
  3. I created a "first PR" template issue that was pre-scoped to be completable
     in 2-3 days and would expose the new hire to our CI/CD pipeline, testing
     framework, and code review process.
  4. I continued delivering my regular sprint commitments on time. I worked on
     the onboarding materials during slack time and my own hours.

Result: The next new hire submitted their first meaningful PR in 8 days instead
of the typical 4-6 weeks. Over the next year, the onboarding guide was used for
12 new hires, and average time-to-first-PR dropped from 5 weeks to 10 days. My
manager nominated me for a peer recognition award, and the onboarding materials
became an official part of our eng team's process.

Learning: I learned that some of the highest-impact work is not on anyone's
roadmap. Seeing a problem and fixing it, even when it is not your job, is what
separates good engineers from great ones.
```

### Questions This Story Can Answer
- "Tell me about a time you went above and beyond"
- "Describe a time you took initiative"
- "Tell me about something you did that was not in your job description"
- "Describe a time you improved a process"

---

## Story 7: Handled Ambiguous Requirements

### Template

```
Situation: At [Company], I was assigned [project/task] where [what was
ambiguous -- unclear requirements, no precedent, conflicting stakeholder
input, new domain].

Task: I needed to [deliver something concrete despite the ambiguity].
The challenge was [what made the ambiguity hard -- no one to ask,
contradictory signals, time pressure to start].

Action:
  1. I [structured the ambiguity -- broke it into what I knew, what I
     needed to find out, and what I could assume].
  2. I [sought information -- talked to stakeholders, researched
     precedents, analyzed data, ran experiments].
  3. I [made a decision / proposed a direction]. I chose to [approach]
     because [reasoning]. I documented my assumptions explicitly.
  4. I [built in flexibility / checkpoints] so we could course-correct
     if my assumptions were wrong.
  5. I [communicated my approach and assumptions] to [stakeholders] to
     get early feedback.

Result: [Outcome]. [Were your assumptions correct? If not, how did you
adapt?]. [Impact on the project].

Learning: I learned that [insight about handling ambiguity -- bias for
action, structured thinking, assumption documentation].
```

### What to Emphasize
- Your structured approach to breaking down ambiguity
- That you did not wait for perfect information -- you took action
- How you managed risk (documented assumptions, built checkpoints)
- Your communication and stakeholder management
- Comfort with uncertainty (they WANT to see this)

### What NOT to Say
- "I waited until requirements were clear" (shows passivity)
- "I just guessed" (shows recklessness)
- "Someone told me what to do" (shows you cannot handle ambiguity)

### Example (Filled Version)

```
Situation: At my company, I was asked to "build a recommendation engine" for
our product. There was no PRD, no ML team, and no historical data on user
preferences. The PM said, "We know users want recommendations, but we do not
know what kind yet."

Task: I needed to deliver a working recommendation feature within 8 weeks,
starting from near-zero clarity on what "recommendations" meant for our users.

Action:
  1. I organized a 2-hour workshop with the PM, designer, and 2 customer
     success reps. I created a simple framework: "Who are we recommending to?
     What are we recommending? Based on what signals?" This turned a vague
     idea into 3 concrete hypotheses.
  2. I proposed starting with the simplest hypothesis (collaborative filtering
     based on usage patterns) since we already had usage data. I documented
     this assumption: "We believe users who use similar features will want
     similar content."
  3. I built a lightweight prototype in 2 weeks using a simple similarity
     algorithm, not ML, to validate the concept before investing in
     infrastructure. I designed the architecture so the recommendation
     algorithm was pluggable and could be swapped later.
  4. I set up A/B testing on the prototype with 10% of users to validate
     the hypothesis before scaling. I shared weekly metrics with stakeholders.
  5. After 2 weeks of A/B testing showed a 15% increase in content engagement,
     I got the green light to invest in a proper implementation.

Result: The recommendation engine launched to 100% of users in week 7. Content
engagement increased by 22% overall. The PM later said this was the smoothest
ambiguous project she had worked on because of the structured, incremental
approach. The pluggable architecture I designed allowed us to swap in an ML-based
algorithm 6 months later with minimal changes.

Learning: I learned that ambiguity is not a problem to solve but a condition to
manage. The key is to start with the smallest experiment that can validate your
biggest assumption, and build from there.
```

### Questions This Story Can Answer
- "Tell me about a time you dealt with ambiguous requirements"
- "Describe a time you had to figure things out on your own"
- "How do you handle uncertainty?"
- "Tell me about a time you had to make decisions without complete information"

---

## Story 8: Mentored/Helped a Colleague

### Template

```
Situation: At [Company], [colleague -- junior engineer, new hire, struggling
teammate] was [what they were dealing with -- ramping up slowly, struggling
with a concept, blocked on a project, lacking confidence].

Task: I [noticed the situation and decided to help / was asked to mentor them].
My goal was to [help them become self-sufficient / unblock them / grow their
skills] not just [solve the problem for them].

Action:
  1. I [initiated the mentoring relationship]. I [scheduled regular 1:1s /
     offered pair programming / created a learning plan].
  2. I [specific teaching/mentoring action -- explained the concept, walked
     through code, shared resources, created exercises].
  3. Instead of [doing it for them], I [guided them to the answer -- asked
     questions, gave hints, reviewed their attempts].
  4. I [adjusted my approach based on their learning style / provided
     encouragement when they were frustrated / celebrated their wins].
  5. Over [timeframe], I [gradually reduced my involvement] as they [gained
     independence].

Result: [Colleague's growth -- they delivered X independently, got promoted,
became the go-to person for Y]. [Impact on the team -- knowledge sharing
improved, bus factor reduced]. [Impact on you -- learned teaching skills,
became a better communicator].

Learning: I learned that [insight about mentoring, teaching, leadership --
e.g., teaching is the best way to learn, investing in others multiplies
your impact].
```

### What to Emphasize
- That you invested time willingly, not resentfully
- That you empowered them rather than creating dependency
- Their growth and success (celebrate them, not yourself)
- The broader impact on the team
- Patience and empathy

### What NOT to Say
- "They could not do anything without me" (condescending)
- "I basically did their work for them" (not mentoring)
- "I was forced to mentor them" (shows resentment)
- Taking all credit for their success

### Example (Filled Version)

```
Situation: At my company, a junior engineer who had joined 3 months ago was
struggling with our distributed systems architecture. She was taking 3x longer
than expected to complete tasks because she did not understand the interaction
between our services, and I could see her confidence was declining.

Task: I noticed this during a sprint retrospective where she mentioned feeling
overwhelmed. I volunteered to mentor her because I had the most context on the
system architecture and remembered my own struggles when I joined.

Action:
  1. I set up twice-weekly 45-minute sessions with her. In the first session,
     I asked her what specifically felt confusing, and together we created a
     list of 8 knowledge gaps ranked by priority.
  2. Instead of lecturing, I created a series of small debugging exercises using
     real production scenarios. Each exercise forced her to trace a request
     through 3-4 services, teaching her the architecture through hands-on
     exploration.
  3. When she got stuck on tasks, I resisted the urge to give answers. Instead,
     I asked guiding questions: "What do you think happens when service A calls
     service B? What would you check first?" This built her debugging instincts.
  4. I paired with her on her next sprint task, but in "navigator" mode -- she
     drove, I guided. When she made good decisions, I explicitly praised them
     to build her confidence.
  5. After 6 weeks, I moved our sessions to weekly, then biweekly, as she
     needed less support.

Result: Within 2 months, she was completing tasks at the expected pace and had
become the go-to person for questions about our notification service (which she
had learned deeply through the exercises). She later onboarded two other
engineers herself using a similar exercise-based approach. She was promoted to
mid-level engineer within a year, and she mentioned me in her promotion
document.

Learning: I learned that great mentoring is about building independence, not
dependence. The exercises I created had more lasting impact than any amount
of explaining because she learned by doing.
```

### Questions This Story Can Answer
- "Tell me about a time you mentored someone"
- "Describe a time you helped a teammate grow"
- "Tell me about a time you developed talent"
- "How do you share knowledge with your team?"

---

## Story Bank Summary Sheet

Once you have filled in all 8 stories, use this quick-reference sheet during practice:

| # | Story Title | Key Metric | Competencies Covered |
|---|---|---|---|
| 1 | _____________ | _____________ | Leadership, Pressure, Decision-making |
| 2 | _____________ | _____________ | Conflict, Communication, Compromise |
| 3 | _____________ | _____________ | Failure, Accountability, Growth |
| 4 | _____________ | _____________ | Deadline, Prioritization, Execution |
| 5 | _____________ | _____________ | Disagree & Commit, Influence, Data |
| 6 | _____________ | _____________ | Initiative, Ownership, Impact |
| 7 | _____________ | _____________ | Ambiguity, Structured Thinking, Action |
| 8 | _____________ | _____________ | Mentoring, Teaching, Empathy |

---

## Practice Checklist

For each story, verify:

- [ ] Can you tell it in under 3 minutes?
- [ ] Does it have specific "I" actions (not "we")?
- [ ] Does it include at least one quantifiable result?
- [ ] Have you practiced it aloud at least 5 times?
- [ ] Can you adapt it for at least 3 different question types?
- [ ] Does it show a genuine lesson learned?
- [ ] Would YOU hire someone who told this story?
