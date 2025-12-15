"""Unit tests for task storage."""

from datetime import datetime

import pytest

from src.models.priority import Priority
from src.models.recurrence import RecurrencePattern
from src.storage.task_store import InMemoryTaskStore


class TestInMemoryTaskStore:
    """Test InMemoryTaskStore."""

    def test_add_task_minimal(self, task_store):
        """Test adding task with minimal fields."""
        task = task_store.add_task(title="Test Task")

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == ""
        assert task.completed is False
        assert task.categories == []
        assert task.due_date is None
        assert task.recurrence_pattern is None

    def test_add_task_full(self, task_store):
        """Test adding task with all fields."""
        due_date = datetime(2025, 12, 31, 23, 59)
        task = task_store.add_task(
            title="Test Task",
            description="Test description",
            priority="HIGH",
            categories=["work", "urgent"],
            due_date=due_date,
            recurrence_pattern="DAILY"
        )

        assert task.id == 1
        assert task.title == "Test Task"
        assert task.description == "Test description"
        assert task.categories == ["work", "urgent"]
        assert task.due_date == due_date

    def test_add_multiple_tasks_increments_id(self, task_store):
        """Test that task IDs increment correctly."""
        task1 = task_store.add_task(title="Task 1")
        task2 = task_store.add_task(title="Task 2")
        task3 = task_store.add_task(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_get_task_exists(self, task_store):
        """Test getting an existing task."""
        added_task = task_store.add_task(title="Test Task")
        retrieved_task = task_store.get_task(added_task.id)

        assert retrieved_task is not None
        assert retrieved_task.id == added_task.id
        assert retrieved_task.title == added_task.title

    def test_get_task_not_exists(self, task_store):
        """Test getting a non-existent task."""
        task = task_store.get_task(999)
        assert task is None

    def test_get_all_tasks_empty(self, task_store):
        """Test getting all tasks when store is empty."""
        tasks = task_store.get_all_tasks()
        assert tasks == []

    def test_get_all_tasks_multiple(self, task_store):
        """Test getting all tasks."""
        task_store.add_task(title="Task 1")
        task_store.add_task(title="Task 2")
        task_store.add_task(title="Task 3")

        tasks = task_store.get_all_tasks()
        assert len(tasks) == 3
        assert [t.title for t in tasks] == ["Task 1", "Task 2", "Task 3"]

    def test_update_task_title(self, task_store):
        """Test updating task title."""
        task = task_store.add_task(title="Original Title")
        updated_task = task_store.update_task(task.id, title="Updated Title")

        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.id == task.id

    def test_update_task_multiple_fields(self, task_store):
        """Test updating multiple task fields."""
        task = task_store.add_task(title="Test Task")
        updated_task = task_store.update_task(
            task.id,
            title="Updated Title",
            description="Updated description",
            priority="HIGH",
            completed=True
        )

        assert updated_task is not None
        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated description"
        assert updated_task.completed is True

    def test_update_task_updates_timestamp(self, task_store):
        """Test that update updates the updated_at timestamp."""
        task = task_store.add_task(title="Test Task")
        original_updated_at = task.updated_at

        # Small delay to ensure timestamp difference
        import time
        time.sleep(0.01)

        updated_task = task_store.update_task(task.id, title="Updated Title")

        assert updated_task is not None
        assert updated_task.updated_at > original_updated_at

    def test_update_task_not_exists(self, task_store):
        """Test updating a non-existent task."""
        updated_task = task_store.update_task(999, title="Updated Title")
        assert updated_task is None

    def test_delete_task_exists(self, task_store):
        """Test deleting an existing task."""
        task = task_store.add_task(title="Test Task")
        result = task_store.delete_task(task.id)

        assert result is True
        assert task_store.get_task(task.id) is None

    def test_delete_task_not_exists(self, task_store):
        """Test deleting a non-existent task."""
        result = task_store.delete_task(999)
        assert result is False

    def test_delete_task_removes_from_all_tasks(self, task_store):
        """Test that deleted task is removed from get_all_tasks."""
        task1 = task_store.add_task(title="Task 1")
        task2 = task_store.add_task(title="Task 2")
        task3 = task_store.add_task(title="Task 3")

        task_store.delete_task(task2.id)

        all_tasks = task_store.get_all_tasks()
        assert len(all_tasks) == 2
        assert task2.id not in [t.id for t in all_tasks]

    def test_clear_all_tasks(self, task_store):
        """Test clearing all tasks."""
        task_store.add_task(title="Task 1")
        task_store.add_task(title="Task 2")
        task_store.add_task(title="Task 3")

        task_store.clear_all_tasks()

        tasks = task_store.get_all_tasks()
        assert tasks == []

    def test_clear_all_tasks_resets_id_counter(self, task_store):
        """Test that clear_all_tasks resets the ID counter."""
        task_store.add_task(title="Task 1")
        task_store.add_task(title="Task 2")

        task_store.clear_all_tasks()

        new_task = task_store.add_task(title="New Task")
        assert new_task.id == 1

    def test_thread_safety_add_tasks(self, task_store):
        """Test thread safety when adding tasks concurrently."""
        import threading

        def add_tasks():
            for i in range(10):
                task_store.add_task(title=f"Task {i}")

        threads = [threading.Thread(target=add_tasks) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        tasks = task_store.get_all_tasks()
        assert len(tasks) == 50  # 5 threads * 10 tasks each
        # Check that all task IDs are unique
        task_ids = [t.id for t in tasks]
        assert len(task_ids) == len(set(task_ids))
