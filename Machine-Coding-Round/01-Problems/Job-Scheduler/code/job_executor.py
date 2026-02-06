"""Job executor for the Job Scheduler."""

import time
from enums import JobStatus


class JobExecutionResult:
    """Result of a single job execution."""

    def __init__(self, job_id, job_name, success, duration, error=None, run_number=0):
        self.job_id = job_id
        self.job_name = job_name
        self.success = success
        self.duration = duration
        self.error = error
        self.run_number = run_number
        self.timestamp = time.time()

    def __str__(self):
        status = "COMPLETED" if self.success else "FAILED"
        run_info = f" (run {self.run_number})" if self.run_number > 0 else ""
        duration_str = f"{self.duration:.3f}s"
        if self.error:
            return (f"{self.job_id}  {self.job_name:<25} {status:<10} "
                    f"{duration_str:<8} Error: {self.error}{run_info}")
        return (f"{self.job_id}  {self.job_name:<25} {status:<10} "
                f"{duration_str}{run_info}")


class JobExecutor:
    """Executes jobs and captures results."""

    def execute(self, job):
        """
        Execute a single job.
        Returns a JobExecutionResult.
        """
        print(f"[RUNNING] {job.short_str()}")
        job.status = JobStatus.RUNNING
        job.current_runs += 1

        start_time = time.time()
        try:
            job.command()
            duration = time.time() - start_time
            job.status = JobStatus.COMPLETED
            print(f"[COMPLETED] {job.short_str()} (took {duration:.3f}s)")
            return JobExecutionResult(
                job.id, job.name, success=True, duration=duration
            )
        except Exception as e:
            duration = time.time() - start_time
            job.status = JobStatus.FAILED
            print(f"[FAILED] {job.short_str()} (Error: {e})")
            return JobExecutionResult(
                job.id, job.name, success=False, duration=duration, error=str(e)
            )

    def execute_recurring(self, job):
        """
        Execute a recurring job for all its remaining runs.
        Returns a list of JobExecutionResults.
        """
        results = []
        while job.has_runs_remaining():
            run_num = job.current_runs + 1
            print(f"[RUN {run_num}/{job.max_runs}] {job.short_str()}")
            job.status = JobStatus.RUNNING
            job.current_runs += 1

            start_time = time.time()
            try:
                job.command()
                duration = time.time() - start_time
                result = JobExecutionResult(
                    job.id, job.name, success=True, duration=duration,
                    run_number=run_num
                )
                results.append(result)
                print(f"  Result: OK ({duration:.3f}s)")
            except Exception as e:
                duration = time.time() - start_time
                result = JobExecutionResult(
                    job.id, job.name, success=False, duration=duration,
                    error=str(e), run_number=run_num
                )
                results.append(result)
                print(f"  Result: FAILED ({e})")
                job.status = JobStatus.FAILED
                print(f"[STOPPED] {job.short_str()} after failure on run {run_num}")
                return results

            # Simulate interval wait (shortened for demo)
            if job.has_runs_remaining() and job.interval_seconds > 0:
                wait = min(job.interval_seconds, 0.5)  # Cap at 0.5s for demo
                time.sleep(wait)

        job.status = JobStatus.COMPLETED
        print(f"[COMPLETED] {job.short_str()} (all {job.max_runs} recurring runs done)")
        return results
