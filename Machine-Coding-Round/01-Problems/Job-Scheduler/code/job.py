"""Job entity for the Job Scheduler."""

from enums import JobStatus, Priority, ScheduleType


class Job:
    """Represents a schedulable job with a command, priority, and status."""

    _counter = 0

    def __init__(self, name, command, priority=Priority.MEDIUM,
                 schedule_type=ScheduleType.ONE_TIME,
                 interval_seconds=0, max_runs=1):
        Job._counter += 1
        self.id = f"JOB-{Job._counter:03d}"
        self.name = name
        self.command = command         # Python callable
        self.priority = priority
        self.status = JobStatus.PENDING
        self.schedule_type = schedule_type
        self.interval_seconds = interval_seconds
        self.max_runs = max_runs
        self.current_runs = 0
        self._insertion_order = Job._counter  # For FIFO within same priority

    def is_pending(self):
        return self.status == JobStatus.PENDING

    def is_recurring(self):
        return self.schedule_type == ScheduleType.RECURRING

    def has_runs_remaining(self):
        return self.current_runs < self.max_runs

    def sort_key(self):
        """Sort key for priority queue: lower value = higher priority."""
        return (self.priority.value, self._insertion_order)

    def __str__(self):
        return (f"{self.id} {self.name:<25} [{self.priority.name:<6}] "
                f"{self.status.value}")

    def short_str(self):
        return f"{self.id}: {self.name}"
