"""Pytest configuration and shared fixtures."""

from datetime import datetime
from typing import Generator

import pytest
from freezegun import freeze_time

from src.models.priority import Priority
from src.models.recurrence import RecurrencePattern
from src.models.task import Task
from src.storage.task_store import InMemoryTaskStore


@pytest.fixture
def task_store() -> Generator[InMemoryTaskStore, None, None]:
    """Create a fresh task store for each test.

    Yields:
        Clean InMemoryTaskStore instance
    """
    store = InMemoryTaskStore()
    yield store
    store.clear_all_tasks()


@pytest.fixture
def frozen_time():
    """Freeze time at a specific datetime for testing.

    Yields:
        Frozen time at 2025-01-15 12:00:00
    """
    with freeze_time("2025-01-15 12:00:00"):
        yield


@pytest.fixture
def sample_task() -> Task:
    """Create a sample task for testing.

    Returns:
        Sample task with default values
    """
    return Task(
        id=1,
        title="Sample Task",
        description="This is a sample task",
        completed=False,
        priority=Priority.MEDIUM,
        categories=["work"],
        due_date=None,
        recurrence_pattern=None,
        created_at=datetime(2025, 1, 15, 12, 0, 0),
        updated_at=datetime(2025, 1, 15, 12, 0, 0),
    )


@pytest.fixture
def sample_tasks() -> list[Task]:
    """Create multiple sample tasks for testing.

    Returns:
        List of sample tasks with varying attributes
    """
    base_time = datetime(2025, 1, 15, 12, 0, 0)
    return [
        Task(
            id=1,
            title="High Priority Task",
            description="Urgent task",
            completed=False,
            priority=Priority.HIGH,
            categories=["work", "urgent"],
            due_date=datetime(2025, 1, 16, 9, 0, 0),
            recurrence_pattern=None,
            created_at=base_time,
            updated_at=base_time,
        ),
        Task(
            id=2,
            title="Medium Priority Task",
            description="Regular task",
            completed=False,
            priority=Priority.MEDIUM,
            categories=["personal"],
            due_date=None,
            recurrence_pattern=None,
            created_at=base_time,
            updated_at=base_time,
        ),
        Task(
            id=3,
            title="Low Priority Task",
            description="Can wait",
            completed=True,
            priority=Priority.LOW,
            categories=["personal", "later"],
            due_date=None,
            recurrence_pattern=None,
            created_at=base_time,
            updated_at=base_time,
        ),
        Task(
            id=4,
            title="Daily Recurring Task",
            description="Do this every day",
            completed=False,
            priority=Priority.MEDIUM,
            categories=["daily"],
            due_date=datetime(2025, 1, 16, 8, 0, 0),
            recurrence_pattern=RecurrencePattern.DAILY,
            created_at=base_time,
            updated_at=base_time,
        ),
    ]
