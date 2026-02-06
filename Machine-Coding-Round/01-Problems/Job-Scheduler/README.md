# Job Scheduler System

## Problem Statement

Design and implement a **Job Scheduler** that can schedule, execute, and track jobs.
The scheduler should support one-time and recurring jobs, priority-based execution,
and maintain a complete execution history.

**Time Limit**: 90 minutes

---

## Requirements

### Functional Requirements

1. **Job Management**
   - Create jobs with a name, command (callable), and priority
   - Jobs have statuses: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED
   - Cancel a pending job
   - List all jobs with their statuses

2. **Scheduling**
   - Schedule one-time jobs for immediate execution
   - Schedule recurring jobs (run every N seconds, with max_runs limit)
   - Jobs execute based on priority (HIGH > MEDIUM > LOW)

3. **Priority Queue**
   - Higher priority jobs execute before lower priority ones
   - Within the same priority, FIFO order is maintained
   - View the current execution queue

4. **Job Execution**
   - Execute the next job in the queue
   - Execute all pending jobs in priority order
   - Track execution result (success/failure) and duration
   - Jobs that raise exceptions are marked as FAILED

5. **Execution History**
   - Track all job executions with timestamps and results
   - View history for a specific job or all jobs
   - Show execution statistics (total, succeeded, failed)

6. **Edge Cases**
   - Cannot execute a cancelled job
   - Cannot cancel an already completed/running job
   - Recurring job stops after max_runs reached
   - Graceful handling of job execution failures

### Non-Functional Requirements
- In-memory storage
- Modular code with separate files
- Use enums for job status, priority, schedule type
- Simulated execution (jobs are Python callables)

---

## Sample Input/Output

```
=== Creating Jobs ===
[SUCCESS] Job JOB-001 created: Backup Database (Priority: HIGH)
[SUCCESS] Job JOB-002 created: Send Newsletter (Priority: MEDIUM)
[SUCCESS] Job JOB-003 created: Clean Temp Files (Priority: LOW)
[SUCCESS] Job JOB-004 created: Sync Inventory (Priority: HIGH)

=== Execution Queue (Priority Order) ===
  1. JOB-001 Backup Database     [HIGH]   PENDING
  2. JOB-004 Sync Inventory      [HIGH]   PENDING
  3. JOB-002 Send Newsletter     [MEDIUM] PENDING
  4. JOB-003 Clean Temp Files    [LOW]    PENDING

=== Execute Next ===
[RUNNING] JOB-001: Backup Database
[COMPLETED] JOB-001: Backup Database (took 0.5s)

=== Execute All Remaining ===
[RUNNING] JOB-004: Sync Inventory
[COMPLETED] JOB-004: Sync Inventory (took 0.3s)
[RUNNING] JOB-002: Send Newsletter
[FAILED] JOB-002: Send Newsletter (Error: SMTP connection failed)
[RUNNING] JOB-003: Clean Temp Files
[COMPLETED] JOB-003: Clean Temp Files (took 0.1s)

=== Recurring Job ===
[SUCCESS] Recurring Job JOB-005 created: Health Check (every 2s, max 3 runs)
[RUN 1/3] JOB-005: Health Check - OK
[RUN 2/3] JOB-005: Health Check - OK
[RUN 3/3] JOB-005: Health Check - OK
[COMPLETED] JOB-005: All recurring runs completed

=== Execution History ===
  JOB-001  Backup Database     COMPLETED  0.5s   2024-01-15 10:00:01
  JOB-004  Sync Inventory      COMPLETED  0.3s   2024-01-15 10:00:02
  JOB-002  Send Newsletter     FAILED     0.0s   2024-01-15 10:00:02
  JOB-003  Clean Temp Files    COMPLETED  0.1s   2024-01-15 10:00:03
  JOB-005  Health Check        COMPLETED  (3 runs)

=== Statistics ===
  Total Jobs:   5
  Completed:    4
  Failed:       1
  Success Rate: 80%
```

---

## Class Diagram

```
┌──────────────────┐
│     Job          │
│                  │
│ - id             │
│ - name           │
│ - command        │
│ - priority       │
│ - status         │
│ - schedule_type  │
│ - max_runs       │
│ - current_runs   │
└────────┬─────────┘
         │
         │ 0..*
┌────────┴─────────┐
│  JobExecution    │
│                  │
│ - id             │
│ - job_id         │
│ - start_time     │
│ - end_time       │
│ - result         │
│ - error          │
└──────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   Scheduler      │  │  PriorityQueue   │  │   JobHistory     │
│                  │  │                  │  │                  │
│ + schedule()     │  │ + enqueue()      │  │ + record()       │
│ + execute_next() │  │ + dequeue()      │  │ + get_history()  │
│ + execute_all()  │  │ + peek()         │  │ + get_stats()    │
│ + cancel()       │  │ + display()      │  │ + display()      │
└──────────────────┘  └──────────────────┘  └──────────────────┘

┌──────────────────┐
│  JobExecutor     │
│                  │
│ + execute(job)   │
│ + run_recurring()│
└──────────────────┘

Enums: JobStatus (PENDING, RUNNING, COMPLETED, FAILED, CANCELLED)
       Priority (HIGH, MEDIUM, LOW)
       ScheduleType (ONE_TIME, RECURRING)
```

---

## File Structure

```
code/
├── enums.py           # JobStatus, Priority, ScheduleType
├── job.py             # Job entity
├── priority_queue.py  # Priority-based job queue
├── job_executor.py    # Executes jobs and tracks results
├── job_history.py     # Execution history and statistics
├── recurring_job.py   # Recurring job execution
├── scheduler.py       # Main scheduler orchestrating everything
└── demo.py            # Full working demo
```

---

## Evaluation Criteria

| Criteria | Points | What They Look For |
|----------|--------|--------------------|
| Executable | 30 | demo.py runs, jobs execute correctly |
| Modularity | 25 | Scheduler, Executor, History separated |
| Extensibility | 15 | Easy to add new priority levels, schedule types |
| Edge Cases | 15 | Failed jobs, cancellation, max_runs |
| Patterns | 10 | Strategy for scheduling, clean priority queue |
| Bonus | 5 | Recurring jobs, execution stats |

---

## Hints

1. **Priority Queue**: Use a list sorted by (priority_order, insertion_order) or
   Python's heapq with a tuple key
2. **Job commands**: Use Python callables (lambdas or functions) as job commands
3. **Execution timing**: Use time.time() to measure duration
4. **Error handling**: Wrap job execution in try/except to catch failures
5. **Recurring jobs**: Use a loop with sleep for simulated recurring execution

---

## Extension Ideas (If You Finish Early)

- Cron-like scheduling (specific times/days)
- Job dependencies (Job B runs only after Job A completes)
- Job retry with exponential backoff
- Concurrent job execution with thread pool
- Job groups/tags for batch operations
