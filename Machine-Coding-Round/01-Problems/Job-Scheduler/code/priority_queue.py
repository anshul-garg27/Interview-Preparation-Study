"""Priority queue for the Job Scheduler."""


class PriorityQueue:
    """
    A priority queue for jobs.
    Higher priority (lower enum value) jobs come first.
    Within the same priority, FIFO order is maintained.
    """

    def __init__(self):
        self._queue = []

    def enqueue(self, job):
        """Add a job to the queue and maintain sorted order."""
        self._queue.append(job)
        self._queue.sort(key=lambda j: j.sort_key())

    def dequeue(self):
        """Remove and return the highest priority job, or None if empty."""
        # Find the first pending job
        for i, job in enumerate(self._queue):
            if job.is_pending():
                return self._queue.pop(i)
        return None

    def peek(self):
        """View the next job without removing it."""
        for job in self._queue:
            if job.is_pending():
                return job
        return None

    def is_empty(self):
        """Check if there are any pending jobs."""
        return not any(j.is_pending() for j in self._queue)

    def size(self):
        """Number of pending jobs."""
        return sum(1 for j in self._queue if j.is_pending())

    def remove(self, job_id):
        """Remove a job from the queue by ID."""
        self._queue = [j for j in self._queue if j.id != job_id]

    def display(self):
        """Display the current queue in priority order."""
        pending = [j for j in self._queue if j.is_pending()]
        if not pending:
            print("  (queue is empty)")
            return

        print(f"  {'#':<4} {'ID':<10} {'Name':<25} {'Priority':<10} {'Status'}")
        print(f"  {'-' * 60}")
        for i, job in enumerate(pending, 1):
            print(f"  {i:<4} {job}")
