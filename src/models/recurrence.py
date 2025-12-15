"""Recurrence pattern enum for recurring tasks."""

from enum import Enum


class RecurrencePattern(str, Enum):
    """Recurrence patterns for recurring tasks.

    Attributes:
        DAILY: Task recurs every day
        WEEKLY: Task recurs every week
        MONTHLY: Task recurs every month
    """

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
