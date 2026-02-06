"""Job execution history and statistics."""

from datetime import datetime


class JobHistory:
    """Tracks execution history for all jobs."""

    def __init__(self):
        self._history = []  # List of JobExecutionResult

    def record(self, result):
        """Record a single execution result."""
        self._history.append(result)

    def record_all(self, results):
        """Record multiple execution results."""
        self._history.extend(results)

    def get_history(self, job_id=None):
        """Get execution history, optionally filtered by job_id."""
        if job_id:
            return [r for r in self._history if r.job_id == job_id]
        return list(self._history)

    def get_stats(self):
        """Get execution statistics."""
        total = len(self._history)
        succeeded = sum(1 for r in self._history if r.success)
        failed = total - succeeded
        rate = (succeeded / total * 100) if total > 0 else 0

        return {
            "total": total,
            "succeeded": succeeded,
            "failed": failed,
            "success_rate": rate,
        }

    def display_history(self, job_id=None):
        """Display execution history in formatted table."""
        history = self.get_history(job_id)
        title = f"Execution History for {job_id}" if job_id else "Execution History"

        print(f"\n  {title}")
        print(f"  {'=' * 70}")

        if not history:
            print("  (no execution history)")
        else:
            for result in history:
                ts = datetime.fromtimestamp(result.timestamp).strftime("%H:%M:%S")
                print(f"  [{ts}] {result}")

        print(f"  {'=' * 70}")

    def display_stats(self):
        """Display execution statistics."""
        stats = self.get_stats()
        print(f"\n  Execution Statistics")
        print(f"  {'-' * 35}")
        print(f"  Total Executions : {stats['total']}")
        print(f"  Succeeded        : {stats['succeeded']}")
        print(f"  Failed           : {stats['failed']}")
        print(f"  Success Rate     : {stats['success_rate']:.1f}%")
        print(f"  {'-' * 35}")
