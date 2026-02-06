"""Main scheduler - orchestrates job creation, queuing, and execution."""

from enums import JobStatus, Priority, ScheduleType
from job import Job
from priority_queue import PriorityQueue
from job_executor import JobExecutor
from job_history import JobHistory
from recurring_job import create_recurring_job


class Scheduler:
    """
    Main scheduler that coordinates job creation, priority queuing,
    execution, and history tracking.
    """

    def __init__(self):
        self._jobs = {}             # job_id -> Job
        self._queue = PriorityQueue()
        self._executor = JobExecutor()
        self._history = JobHistory()

    # ── Job Creation ────────────────────────────────────────────────────

    def schedule(self, name, command, priority=Priority.MEDIUM):
        """Schedule a one-time job."""
        job = Job(name, command, priority)
        self._jobs[job.id] = job
        self._queue.enqueue(job)
        print(f"[SUCCESS] Job {job.id} created: {name} (Priority: {priority.name})")
        return job

    def schedule_recurring(self, name, command, interval_seconds, max_runs,
                           priority=Priority.MEDIUM):
        """Schedule a recurring job."""
        job = create_recurring_job(name, command, interval_seconds, max_runs, priority)
        self._jobs[job.id] = job
        # Recurring jobs are not put in the main queue; they run separately.
        return job

    # ── Job Execution ───────────────────────────────────────────────────

    def execute_next(self):
        """Execute the next job in the priority queue."""
        job = self._queue.dequeue()
        if not job:
            print("[INFO] No pending jobs in queue")
            return None

        result = self._executor.execute(job)
        self._history.record(result)
        return result

    def execute_all(self):
        """Execute all pending jobs in priority order."""
        results = []
        while not self._queue.is_empty():
            result = self.execute_next()
            if result:
                results.append(result)
        if not results:
            print("[INFO] No jobs to execute")
        return results

    def execute_recurring(self, job_id):
        """Execute all runs of a recurring job."""
        job = self._jobs.get(job_id)
        if not job:
            print(f"[ERROR] Job '{job_id}' not found")
            return []

        if not job.is_recurring():
            print(f"[ERROR] Job '{job_id}' is not a recurring job")
            return []

        if not job.is_pending():
            print(f"[ERROR] Job '{job_id}' is not in PENDING state ({job.status.value})")
            return []

        results = self._executor.execute_recurring(job)
        self._history.record_all(results)
        return results

    # ── Job Management ──────────────────────────────────────────────────

    def cancel_job(self, job_id):
        """Cancel a pending job."""
        job = self._jobs.get(job_id)
        if not job:
            print(f"[ERROR] Job '{job_id}' not found")
            return False

        if not job.is_pending():
            print(f"[ERROR] Cannot cancel job '{job_id}' - "
                  f"status is {job.status.value} (must be PENDING)")
            return False

        job.status = JobStatus.CANCELLED
        self._queue.remove(job_id)
        print(f"[SUCCESS] Job {job.id} cancelled: {job.name}")
        return True

    def get_job(self, job_id):
        """Get a job by ID."""
        job = self._jobs.get(job_id)
        if not job:
            print(f"[ERROR] Job '{job_id}' not found")
        return job

    # ── Display ─────────────────────────────────────────────────────────

    def show_queue(self):
        """Display the current execution queue."""
        print(f"\n  Execution Queue ({self._queue.size()} pending)")
        print(f"  {'=' * 60}")
        self._queue.display()
        print(f"  {'=' * 60}")

    def show_all_jobs(self):
        """Display all jobs and their statuses."""
        print(f"\n  All Jobs")
        print(f"  {'=' * 65}")
        if not self._jobs:
            print("  (no jobs)")
        else:
            for job in self._jobs.values():
                extra = ""
                if job.is_recurring():
                    extra = f" (runs: {job.current_runs}/{job.max_runs})"
                print(f"  {job}{extra}")
        print(f"  {'=' * 65}")

    def show_history(self, job_id=None):
        """Display execution history."""
        self._history.display_history(job_id)

    def show_stats(self):
        """Display execution statistics."""
        self._history.display_stats()
