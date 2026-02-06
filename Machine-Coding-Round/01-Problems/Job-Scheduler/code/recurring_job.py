"""Recurring job support for the Job Scheduler."""

from enums import ScheduleType, Priority
from job import Job


def create_recurring_job(name, command, interval_seconds, max_runs,
                         priority=Priority.MEDIUM):
    """
    Factory function to create a recurring job.

    Args:
        name: Job name
        command: Python callable to execute
        interval_seconds: Seconds between each run
        max_runs: Maximum number of times to run
        priority: Job priority (default MEDIUM)

    Returns:
        A Job configured for recurring execution.
    """
    job = Job(
        name=name,
        command=command,
        priority=priority,
        schedule_type=ScheduleType.RECURRING,
        interval_seconds=interval_seconds,
        max_runs=max_runs,
    )

    recurrence_info = f"every {interval_seconds}s, max {max_runs} runs"
    print(f"[SUCCESS] Recurring Job {job.id} created: {name} ({recurrence_info})")
    return job
