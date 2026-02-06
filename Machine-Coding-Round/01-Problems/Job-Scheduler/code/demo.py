"""
Job Scheduler System - Demo
==============================
Run: python demo.py
"""

import time
from enums import Priority
from scheduler import Scheduler


def print_header(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


# ── Sample Job Commands (callables) ─────────────────────────────────────

def backup_database():
    """Simulates a database backup."""
    time.sleep(0.2)
    # Simulate work

def send_newsletter():
    """Simulates sending newsletter - will fail."""
    raise RuntimeError("SMTP connection failed")

def clean_temp_files():
    """Simulates cleaning temp files."""
    time.sleep(0.1)

def sync_inventory():
    """Simulates inventory sync."""
    time.sleep(0.15)

def generate_report():
    """Simulates report generation."""
    time.sleep(0.1)

def health_check():
    """Simulates a system health check."""
    time.sleep(0.05)

def process_payments():
    """Simulates payment processing."""
    time.sleep(0.1)

_log_counter = 0
def rotate_logs():
    """Simulates log rotation - fails on 3rd run."""
    global _log_counter
    _log_counter += 1
    if _log_counter == 3:
        raise RuntimeError("Disk full")
    time.sleep(0.05)


def main():
    scheduler = Scheduler()

    print_header("JOB SCHEDULER SYSTEM")

    # =========================================================================
    # FEATURE 1: Create Jobs with Different Priorities
    # =========================================================================
    print_header("Feature 1: Create Jobs")

    j1 = scheduler.schedule("Backup Database", backup_database, Priority.HIGH)
    j2 = scheduler.schedule("Send Newsletter", send_newsletter, Priority.MEDIUM)
    j3 = scheduler.schedule("Clean Temp Files", clean_temp_files, Priority.LOW)
    j4 = scheduler.schedule("Sync Inventory", sync_inventory, Priority.HIGH)
    j5 = scheduler.schedule("Generate Report", generate_report, Priority.MEDIUM)

    # =========================================================================
    # FEATURE 2: View Execution Queue (Priority Order)
    # =========================================================================
    print_header("Feature 2: Execution Queue (Priority Order)")

    scheduler.show_queue()

    # =========================================================================
    # FEATURE 3: Execute Next (Highest Priority)
    # =========================================================================
    print_header("Feature 3: Execute Next Job")

    scheduler.execute_next()

    # Show updated queue
    scheduler.show_queue()

    # =========================================================================
    # FEATURE 4: Cancel a Job
    # =========================================================================
    print_header("Feature 4: Cancel a Job")

    scheduler.cancel_job(j5.id)

    # Try to cancel an already-completed job
    scheduler.cancel_job(j1.id)

    scheduler.show_queue()

    # =========================================================================
    # FEATURE 5: Execute All Remaining
    # =========================================================================
    print_header("Feature 5: Execute All Remaining Jobs")

    scheduler.execute_all()

    # =========================================================================
    # FEATURE 6: View All Jobs
    # =========================================================================
    print_header("Feature 6: All Jobs Status")

    scheduler.show_all_jobs()

    # =========================================================================
    # FEATURE 7: Recurring Job
    # =========================================================================
    print_header("Feature 7: Recurring Job - Health Check")

    j6 = scheduler.schedule_recurring(
        "Health Check", health_check,
        interval_seconds=2, max_runs=3, priority=Priority.HIGH
    )
    scheduler.execute_recurring(j6.id)

    # =========================================================================
    # FEATURE 8: Recurring Job with Failure
    # =========================================================================
    print_header("Feature 8: Recurring Job - Failure Handling")

    j7 = scheduler.schedule_recurring(
        "Log Rotation", rotate_logs,
        interval_seconds=1, max_runs=5, priority=Priority.MEDIUM
    )
    scheduler.execute_recurring(j7.id)

    # =========================================================================
    # FEATURE 9: Execution History
    # =========================================================================
    print_header("Feature 9: Execution History")

    # Full history
    scheduler.show_history()

    # History for specific job
    scheduler.show_history(j6.id)

    # =========================================================================
    # FEATURE 10: Statistics
    # =========================================================================
    print_header("Feature 10: Execution Statistics")

    scheduler.show_stats()

    # =========================================================================
    # FEATURE 11: More Jobs - Demonstrating Priority
    # =========================================================================
    print_header("Feature 11: Priority Demo with New Jobs")

    j8 = scheduler.schedule("Process Payments", process_payments, Priority.HIGH)
    j9 = scheduler.schedule("Low Priority Task", lambda: time.sleep(0.05), Priority.LOW)
    j10 = scheduler.schedule("Medium Priority Task", lambda: time.sleep(0.05), Priority.MEDIUM)

    print("\n  Queue after adding 3 new jobs:")
    scheduler.show_queue()

    print("\n  Executing all (observe priority order):")
    scheduler.execute_all()

    # =========================================================================
    # FEATURE 12: Edge Cases
    # =========================================================================
    print_header("Feature 12: Edge Cases")

    # Execute when queue is empty
    scheduler.execute_next()

    # Cancel non-existent job
    scheduler.cancel_job("JOB-999")

    # Execute non-existent recurring job
    scheduler.execute_recurring("JOB-999")

    # =========================================================================
    # FINAL STATE
    # =========================================================================
    print_header("Final State: All Jobs")

    scheduler.show_all_jobs()
    scheduler.show_stats()

    print_header("DEMO COMPLETE")


if __name__ == "__main__":
    main()
