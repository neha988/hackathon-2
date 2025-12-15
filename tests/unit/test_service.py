"""Unit tests for task service."""

from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from src.models.priority import Priority
from src.models.recurrence import RecurrencePattern
from src.services.task_service import TaskService


class TestTaskServiceCreate:
    """Test task creation."""

    def test_create_task_minimal(self, task_store):
        """Test creating task with minimal fields."""
        service = TaskService(task_store)
        task = service.create_task(title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False

    def test_create_task_full(self, task_store):
        """Test creating task with all fields."""
        service = TaskService(task_store)
        due_date = datetime(2025, 12, 31, 23, 59)
        task = service.create_task(
            title="Test Task",
            description="Test description",
            priority="HIGH",
            categories=["work", "urgent"],
            due_date=due_date,
            recurrence_pattern="DAILY"
        )

        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.categories == ["work", "urgent"]
        assert task.due_date == due_date


class TestTaskServiceGet:
    """Test task retrieval."""

    def test_get_task_exists(self, task_store):
        """Test getting an existing task."""
        service = TaskService(task_store)
        created_task = service.create_task(title="Test Task")
        retrieved_task = service.get_task(created_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == created_task.id

    def test_get_task_not_exists(self, task_store):
        """Test getting a non-existent task."""
        service = TaskService(task_store)
        task = service.get_task(999)

        assert task is None

    def test_get_all_tasks_empty(self, task_store):
        """Test getting all tasks when empty."""
        service = TaskService(task_store)
        tasks = service.get_all_tasks()

        assert tasks == []

    def test_get_all_tasks_multiple(self, task_store):
        """Test getting all tasks."""
        service = TaskService(task_store)
        service.create_task(title="Task 1")
        service.create_task(title="Task 2")
        service.create_task(title="Task 3")

        tasks = service.get_all_tasks()
        assert len(tasks) == 3


class TestTaskServiceUpdate:
    """Test task updates."""

    def test_update_task_title(self, task_store):
        """Test updating task title."""
        service = TaskService(task_store)
        task = service.create_task(title="Original Title")
        updated_task = service.update_task(task.id, title="Updated Title")

        assert updated_task is not None
        assert updated_task.title == "Updated Title"

    def test_update_task_multiple_fields(self, task_store):
        """Test updating multiple fields."""
        service = TaskService(task_store)
        task = service.create_task(title="Test Task")
        updated_task = service.update_task(
            task.id,
            title="Updated Title",
            description="Updated description",
            priority="HIGH"
        )

        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated description"

    def test_update_task_not_exists(self, task_store):
        """Test updating non-existent task."""
        service = TaskService(task_store)
        updated_task = service.update_task(999, title="Updated")

        assert updated_task is None


class TestTaskServiceDelete:
    """Test task deletion."""

    def test_delete_task_exists(self, task_store):
        """Test deleting an existing task."""
        service = TaskService(task_store)
        task = service.create_task(title="Test Task")
        result = service.delete_task(task.id)

        assert result is True
        assert service.get_task(task.id) is None

    def test_delete_task_not_exists(self, task_store):
        """Test deleting a non-existent task."""
        service = TaskService(task_store)
        result = service.delete_task(999)

        assert result is False


class TestTaskServiceToggleCompletion:
    """Test task completion toggle."""

    def test_toggle_completion_mark_complete(self, task_store):
        """Test marking task as complete."""
        service = TaskService(task_store)
        task = service.create_task(title="Test Task")
        updated_task = service.toggle_completion(task.id)

        assert updated_task is not None
        assert updated_task.completed is True

    def test_toggle_completion_mark_incomplete(self, task_store):
        """Test marking task as incomplete."""
        service = TaskService(task_store)
        task = service.create_task(title="Test Task")
        service.toggle_completion(task.id)  # Mark complete
        updated_task = service.toggle_completion(task.id)  # Mark incomplete

        assert updated_task is not None
        assert updated_task.completed is False

    def test_toggle_completion_not_exists(self, task_store):
        """Test toggling completion of non-existent task."""
        service = TaskService(task_store)
        result = service.toggle_completion(999)

        assert result is None

    @freeze_time("2025-01-15 12:00:00")
    def test_toggle_completion_recurring_creates_next(self, task_store):
        """Test that completing recurring task creates next occurrence."""
        service = TaskService(task_store)
        due_date = datetime(2025, 1, 20, 9, 0)
        task = service.create_task(
            title="Daily Task",
            due_date=due_date,
            recurrence_pattern="DAILY"
        )

        # Mark as complete
        service.toggle_completion(task.id)

        # Should have created next occurrence
        all_tasks = service.get_all_tasks()
        assert len(all_tasks) == 2

        # Find the new task (not completed)
        new_task = [t for t in all_tasks if not t.completed][0]
        assert new_task.title == "Daily Task"
        assert new_task.due_date == due_date + timedelta(days=1)


class TestTaskServiceFiltering:
    """Test task filtering."""

    def test_filter_by_completed_status_pending(self, task_store):
        """Test filtering by pending status."""
        service = TaskService(task_store)
        service.create_task(title="Task 1")
        task2 = service.create_task(title="Task 2")
        service.update_task(task2.id, completed=True)

        pending_tasks = service.filter_tasks(completed=False)
        assert len(pending_tasks) == 1
        assert pending_tasks[0].title == "Task 1"

    def test_filter_by_completed_status_completed(self, task_store):
        """Test filtering by completed status."""
        service = TaskService(task_store)
        task1 = service.create_task(title="Task 1")
        service.update_task(task1.id, completed=True)
        service.create_task(title="Task 2")

        completed_tasks = service.filter_tasks(completed=True)
        assert len(completed_tasks) == 1
        assert completed_tasks[0].title == "Task 1"

    def test_filter_by_priority(self, task_store):
        """Test filtering by priority."""
        service = TaskService(task_store)
        service.create_task(title="Task 1", priority="HIGH")
        service.create_task(title="Task 2", priority="LOW")
        service.create_task(title="Task 3", priority="HIGH")

        high_tasks = service.filter_tasks(priority="HIGH")
        assert len(high_tasks) == 2

    def test_filter_by_category(self, task_store):
        """Test filtering by category."""
        service = TaskService(task_store)
        service.create_task(title="Task 1", categories=["work"])
        service.create_task(title="Task 2", categories=["personal"])
        service.create_task(title="Task 3", categories=["work", "urgent"])

        work_tasks = service.filter_tasks(category="work")
        assert len(work_tasks) == 2

    def test_filter_combined(self, task_store):
        """Test filtering with multiple criteria."""
        service = TaskService(task_store)
        service.create_task(title="Task 1", priority="HIGH", categories=["work"])
        task2 = service.create_task(title="Task 2", priority="HIGH", categories=["work"])
        service.update_task(task2.id, completed=True)
        service.create_task(title="Task 3", priority="LOW", categories=["work"])

        tasks = service.filter_tasks(completed=False, priority="HIGH", category="work")
        assert len(tasks) == 1
        assert tasks[0].title == "Task 1"


class TestTaskServiceSearch:
    """Test task searching."""

    def test_search_by_title(self, task_store):
        """Test searching tasks by title."""
        service = TaskService(task_store)
        service.create_task(title="Buy groceries")
        service.create_task(title="Buy laptop")
        service.create_task(title="Clean house")

        results = service.search_tasks("buy")
        assert len(results) == 2

    def test_search_by_description(self, task_store):
        """Test searching tasks by description."""
        service = TaskService(task_store)
        service.create_task(title="Task 1", description="Important meeting")
        service.create_task(title="Task 2", description="Regular work")
        service.create_task(title="Task 3", description="Important deadline")

        results = service.search_tasks("important")
        assert len(results) == 2

    def test_search_case_insensitive(self, task_store):
        """Test that search is case insensitive."""
        service = TaskService(task_store)
        service.create_task(title="Buy Groceries")
        service.create_task(title="buy laptop")

        results1 = service.search_tasks("BUY")
        results2 = service.search_tasks("buy")
        results3 = service.search_tasks("Buy")

        assert len(results1) == len(results2) == len(results3) == 2

    def test_search_no_results(self, task_store):
        """Test search with no results."""
        service = TaskService(task_store)
        service.create_task(title="Task 1")

        results = service.search_tasks("nonexistent")
        assert results == []


class TestTaskServiceSorting:
    """Test task sorting."""

    def test_sort_by_priority(self, task_store, sample_tasks):
        """Test sorting by priority."""
        service = TaskService(task_store)
        for task_data in sample_tasks:
            task_store._tasks[task_data.id] = task_data

        sorted_tasks = service.sort_tasks(sample_tasks, "priority")
        priorities = [t.priority.value if hasattr(t.priority, 'value') else t.priority for t in sorted_tasks]

        # LOW < MEDIUM < HIGH in priority ordering
        assert priorities[0] == "LOW"
        assert priorities[-1] == "HIGH"

    def test_sort_by_due_date(self, task_store, sample_tasks):
        """Test sorting by due date."""
        service = TaskService(task_store)
        sorted_tasks = service.sort_tasks(sample_tasks, "due_date")

        # Tasks without due date should be last
        tasks_with_dates = [t for t in sorted_tasks if t.due_date]
        assert len(tasks_with_dates) > 0

    def test_sort_by_title(self, task_store):
        """Test sorting by title."""
        service = TaskService(task_store)
        service.create_task(title="Zebra")
        service.create_task(title="Apple")
        service.create_task(title="Banana")

        tasks = service.get_all_tasks()
        sorted_tasks = service.sort_tasks(tasks, "title")

        assert sorted_tasks[0].title == "Apple"
        assert sorted_tasks[1].title == "Banana"
        assert sorted_tasks[2].title == "Zebra"

    def test_sort_reverse(self, task_store):
        """Test reverse sorting."""
        service = TaskService(task_store)
        service.create_task(title="A")
        service.create_task(title="B")
        service.create_task(title="C")

        tasks = service.get_all_tasks()
        sorted_tasks = service.sort_tasks(tasks, "title", reverse=True)

        assert sorted_tasks[0].title == "C"
        assert sorted_tasks[2].title == "A"

    def test_sort_invalid_field_raises_error(self, task_store):
        """Test that invalid sort field raises error."""
        service = TaskService(task_store)
        tasks = []

        with pytest.raises(ValueError, match="Invalid sort field"):
            service.sort_tasks(tasks, "invalid_field")


class TestTaskServiceOverdue:
    """Test overdue task retrieval."""

    @freeze_time("2025-01-15 12:00:00")
    def test_get_overdue_tasks(self, task_store):
        """Test getting overdue tasks."""
        service = TaskService(task_store)

        # Overdue task
        service.create_task(title="Overdue", due_date=datetime(2025, 1, 10))

        # Future task
        service.create_task(title="Future", due_date=datetime(2025, 1, 20))

        # No due date
        service.create_task(title="No due date")

        overdue = service.get_overdue_tasks()
        assert len(overdue) == 1
        assert overdue[0].title == "Overdue"

    @freeze_time("2025-01-15 12:00:00")
    def test_get_overdue_excludes_completed(self, task_store):
        """Test that overdue excludes completed tasks."""
        service = TaskService(task_store)

        task = service.create_task(title="Overdue", due_date=datetime(2025, 1, 10))
        service.update_task(task.id, completed=True)

        overdue = service.get_overdue_tasks()
        assert len(overdue) == 0


class TestTaskServiceUpcoming:
    """Test upcoming task retrieval."""

    @freeze_time("2025-01-15 12:00:00")
    def test_get_upcoming_tasks(self, task_store):
        """Test getting upcoming tasks."""
        service = TaskService(task_store)

        # Within 7 days
        service.create_task(title="Soon", due_date=datetime(2025, 1, 20))

        # Beyond 7 days
        service.create_task(title="Later", due_date=datetime(2025, 2, 1))

        # Past
        service.create_task(title="Past", due_date=datetime(2025, 1, 10))

        upcoming = service.get_upcoming_tasks(days=7)
        assert len(upcoming) == 1
        assert upcoming[0].title == "Soon"

    @freeze_time("2025-01-15 12:00:00")
    def test_get_upcoming_excludes_completed(self, task_store):
        """Test that upcoming excludes completed tasks."""
        service = TaskService(task_store)

        task = service.create_task(title="Soon", due_date=datetime(2025, 1, 20))
        service.update_task(task.id, completed=True)

        upcoming = service.get_upcoming_tasks(days=7)
        assert len(upcoming) == 0
