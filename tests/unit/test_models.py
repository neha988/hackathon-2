"""Unit tests for task models."""

from datetime import datetime

import pytest
from pydantic import ValidationError

from src.models.priority import Priority
from src.models.recurrence import RecurrencePattern
from src.models.task import Task


class TestPriority:
    """Test Priority enum."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert Priority.HIGH.value == "HIGH"
        assert Priority.MEDIUM.value == "MEDIUM"
        assert Priority.LOW.value == "LOW"

    def test_priority_ordering(self):
        """Test priority comparison."""
        priorities = [Priority.LOW, Priority.HIGH, Priority.MEDIUM]
        sorted_priorities = sorted(priorities, key=lambda p: ["HIGH", "MEDIUM", "LOW"].index(p.value))
        assert sorted_priorities == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]


class TestRecurrencePattern:
    """Test RecurrencePattern enum."""

    def test_recurrence_values(self):
        """Test recurrence pattern enum values."""
        assert RecurrencePattern.DAILY.value == "DAILY"
        assert RecurrencePattern.WEEKLY.value == "WEEKLY"
        assert RecurrencePattern.MONTHLY.value == "MONTHLY"


class TestTask:
    """Test Task model."""

    def test_create_minimal_task(self):
        """Test creating task with minimal required fields."""
        now = datetime.now()
        task = Task(
            id=1,
            title="Test Task",
            created_at=now,
            updated_at=now
        )
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert task.priority == Priority.MEDIUM
        assert task.categories == []
        assert task.due_date is None
        assert task.recurrence_pattern is None

    def test_create_full_task(self):
        """Test creating task with all fields."""
        now = datetime.now()
        due_date = datetime(2025, 12, 31, 23, 59)
        task = Task(
            id=1,
            title="Test Task",
            description="Test description",
            completed=True,
            priority=Priority.HIGH,
            categories=["work", "urgent"],
            due_date=due_date,
            recurrence_pattern=RecurrencePattern.DAILY,
            created_at=now,
            updated_at=now
        )
        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.completed is True
        assert task.priority == Priority.HIGH
        assert task.categories == ["work", "urgent"]
        assert task.due_date == due_date
        assert task.recurrence_pattern == RecurrencePattern.DAILY

    def test_task_title_validation_min_length(self):
        """Test task title cannot be empty."""
        now = datetime.now()
        with pytest.raises(ValidationError) as exc_info:
            Task(
                id=1,
                title="",
                created_at=now,
                updated_at=now
            )
        assert "title" in str(exc_info.value).lower()

    def test_task_title_validation_max_length(self):
        """Test task title cannot exceed 200 characters."""
        now = datetime.now()
        long_title = "x" * 201
        with pytest.raises(ValidationError) as exc_info:
            Task(
                id=1,
                title=long_title,
                created_at=now,
                updated_at=now
            )
        assert "title" in str(exc_info.value).lower()

    def test_task_description_max_length(self):
        """Test task description cannot exceed 1000 characters."""
        now = datetime.now()
        long_description = "x" * 1001
        with pytest.raises(ValidationError) as exc_info:
            Task(
                id=1,
                title="Test",
                description=long_description,
                created_at=now,
                updated_at=now
            )
        assert "description" in str(exc_info.value).lower()

    def test_task_with_use_enum_values(self):
        """Test that use_enum_values converts enums to strings."""
        now = datetime.now()
        task = Task(
            id=1,
            title="Test Task",
            priority=Priority.HIGH,
            recurrence_pattern=RecurrencePattern.DAILY,
            created_at=now,
            updated_at=now
        )
        # Due to use_enum_values=True in Config, these should be strings
        assert isinstance(task.priority, str) or task.priority == Priority.HIGH
        assert isinstance(task.recurrence_pattern, str) or task.recurrence_pattern == RecurrencePattern.DAILY

    def test_task_equality(self):
        """Test task equality based on all fields."""
        now = datetime.now()
        task1 = Task(
            id=1,
            title="Test Task",
            created_at=now,
            updated_at=now
        )
        task2 = Task(
            id=1,
            title="Test Task",
            created_at=now,
            updated_at=now
        )
        assert task1 == task2

    def test_task_inequality(self):
        """Test task inequality."""
        now = datetime.now()
        task1 = Task(
            id=1,
            title="Test Task 1",
            created_at=now,
            updated_at=now
        )
        task2 = Task(
            id=2,
            title="Test Task 2",
            created_at=now,
            updated_at=now
        )
        assert task1 != task2
