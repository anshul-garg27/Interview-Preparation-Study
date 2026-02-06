"""Enumerations for the Job Scheduler."""

from enum import Enum


class JobStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class ScheduleType(Enum):
    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"
