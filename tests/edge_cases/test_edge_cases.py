"""Edge case tests for todo application."""

from datetime import datetime

import pytest

from src.services.task_service import TaskService
from src.utils.validators import validate_categories, validate_title


class TestEdgeCases:
    """Test edge cases and boundary conditions."""

    def test_task_title_exactly_200_characters(self, task_store):
        """Test task title with exactly 200 characters."""
        service = TaskService(task_store)
        title = "x" * 200
        task = service.create_task(title=title)

        assert len(task.title) == 200

    def test_task_description_exactly_1000_characters(self, task_store):
        """Test task description with exactly 1000 characters."""
        service = TaskService(task_store)
        description = "x" * 1000
        task = service.create_task(title="Test", description=description)

        assert len(task.description) == 1000

    def test_task_with_many_categories(self, task_store):
        """Test task with many categories."""
        service = TaskService(task_store)
        categories = [f"category{i}" for i in range(50)]
        task = service.create_task(title="Test", categories=categories)

        assert len(task.categories) == 50

    def test_task_with_unicode_title(self, task_store):
        """Test task with unicode characters in title."""
        service = TaskService(task_store)
        title = "测试任务 🎉 Task Tâche"
        task = service.create_task(title=title)

        assert task.title == title

    def test_task_with_special_characters(self, task_store):
        """Test task with special characters."""
        service = TaskService(task_store)
        title = "Task @#$%^&*()[]{}|\\:;\"'<>?,./~`"
        task = service.create_task(title=title)

        assert title in task.title

    def test_task_with_newlines_in_description(self, task_store):
        """Test task with newlines in description."""
        service = TaskService(task_store)
        description = "Line 1\nLine 2\nLine 3"
        task = service.create_task(title="Test", description=description)

        assert "\n" in task.description

    def test_very_large_task_id(self, task_store):
        """Test handling very large task IDs."""
        service = TaskService(task_store)

        # Create many tasks to increment ID
        for i in range(100):
            service.create_task(title=f"Task {i}")

        task = service.get_task(100)
        assert task is not None
        assert task.id == 100

    def test_search_with_empty_string(self, task_store):
        """Test search with empty string."""
        service = TaskService(task_store)
        service.create_task(title="Task 1")
        service.create_task(title="Task 2")

        # Empty search should match all (since empty string is in all strings)
        results = service.search_tasks("")
        assert len(results) == 2

    def test_filter_with_no_matches(self, task_store):
        """Test filtering with no matches."""
        service = TaskService(task_store)
        service.create_task(title="Task", priority="LOW")

        results = service.filter_tasks(priority="HIGH")
        assert results == []

    def test_sort_empty_list(self, task_store):
        """Test sorting an empty list."""
        service = TaskService(task_store)
        sorted_tasks = service.sort_tasks([], "title")

        assert sorted_tasks == []

    def test_sort_single_task(self, task_store):
        """Test sorting a single task."""
        service = TaskService(task_store)
        task = service.create_task(title="Single Task")

        sorted_tasks = service.sort_tasks([task], "title")
        assert len(sorted_tasks) == 1

    def test_concurrent_task_creation(self, task_store):
        """Test concurrent task creation."""
        import threading

        service = TaskService(task_store)
        results = []

        def create_tasks():
            for i in range(10):
                task = service.create_task(title=f"Task {i}")
                results.append(task.id)

        threads = [threading.Thread(target=create_tasks) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        # All IDs should be unique
        assert len(results) == len(set(results))

    def test_update_non_existent_fields(self, task_store):
        """Test updating with non-existent fields (should not crash)."""
        service = TaskService(task_store)
        task = service.create_task(title="Test")

        # Try to update with a field that doesn't exist
        # This should not crash, but the field won't be updated
        try:
            service.update_task(task.id, nonexistent_field="value")
        except Exception:
            pass  # Expected to fail gracefully

    def test_task_with_due_date_in_past(self, task_store):
        """Test creating task with due date in the past."""
        service = TaskService(task_store)
        past_date = datetime(2020, 1, 1)
        task = service.create_task(title="Past Task", due_date=past_date)

        assert task.due_date == past_date

    def test_task_with_far_future_due_date(self, task_store):
        """Test creating task with far future due date."""
        service = TaskService(task_store)
        future_date = datetime(2099, 12, 31)
        task = service.create_task(title="Future Task", due_date=future_date)

        assert task.due_date == future_date

    def test_rapidly_toggle_completion(self, task_store):
        """Test rapidly toggling task completion."""
        service = TaskService(task_store)
        task = service.create_task(title="Test")

        # Toggle 10 times
        for _ in range(10):
            service.toggle_completion(task.id)

        # Should be complete (10 is even, so back to complete)
        final_task = service.get_task(task.id)
        assert final_task.completed is False  # Started as False, toggled even times

    def test_delete_already_deleted_task(self, task_store):
        """Test deleting an already deleted task."""
        service = TaskService(task_store)
        task = service.create_task(title="Test")

        # Delete once
        result1 = service.delete_task(task.id)
        assert result1 is True

        # Delete again
        result2 = service.delete_task(task.id)
        assert result2 is False

    def test_category_with_exactly_50_characters(self, task_store):
        """Test category with exactly 50 characters."""
        service = TaskService(task_store)
        category = "x" * 50
        task = service.create_task(title="Test", categories=[category])

        assert len(task.categories[0]) == 50

    def test_whitespace_handling_in_categories(self, task_store):
        """Test whitespace handling in categories."""
        service = TaskService(task_store)
        categories = ["  work  ", "urgent", "  personal  "]
        task = service.create_task(title="Test", categories=categories)

        # Categories should be stripped and lowercase
        assert task.categories == ["work", "urgent", "personal"]

    def test_duplicate_categories(self, task_store):
        """Test handling duplicate categories."""
        service = TaskService(task_store)
        categories = ["work", "work", "urgent"]
        task = service.create_task(title="Test", categories=categories)

        # Duplicates should be allowed (no deduplication in current impl)
        assert len(task.categories) == 3

    def test_empty_category_string(self):
        """Test that empty category strings are filtered."""
        categories = ["work", "", "urgent", "   "]
        result = validate_categories(categories)

        assert result == ["work", "urgent"]

    def test_title_with_only_whitespace_error(self):
        """Test that title with only whitespace raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            validate_title("     ")

    def test_search_special_regex_characters(self, task_store):
        """Test search with special regex characters."""
        service = TaskService(task_store)
        service.create_task(title="Task (1)")
        service.create_task(title="Task [2]")
        service.create_task(title="Task *3*")

        # These should not cause regex errors
        results1 = service.search_tasks("(1)")
        results2 = service.search_tasks("[2]")
        results3 = service.search_tasks("*3*")

        assert len(results1) == 1
        assert len(results2) == 1
        assert len(results3) == 1

    def test_overdue_tasks_at_exact_boundary(self, task_store):
        """Test overdue tasks at exact time boundary."""
        from freezegun import freeze_time

        service = TaskService(task_store)

        with freeze_time("2025-01-15 12:00:00"):
            # Task due at exact current time
            service.create_task(title="Exact", due_date=datetime(2025, 1, 15, 12, 0, 0))

            overdue = service.get_overdue_tasks()
            # Task at exact current time should not be overdue
            assert len(overdue) == 0
