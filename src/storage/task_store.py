"""In-memory task storage with thread safety."""

import threading
from datetime import datetime
from typing import Dict, List, Optional

from src.models.task import Task
from src.utils.validators import validate_categories


class InMemoryTaskStore:
    """Thread-safe in-memory task storage.

    Attributes:
        _tasks: Dictionary storing tasks by ID
        _next_id: Counter for generating unique task IDs
        _lock: Threading lock for thread safety
    """

    def __init__(self) -> None:
        """Initialize empty task store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def add_task(
        self,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        categories: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence_pattern: Optional[str] = None,
    ) -> Task:
        """Add a new task to the store.

        Args:
            title: Task title
            description: Task description
            priority: Task priority level
            categories: List of category tags
            due_date: Optional due date
            recurrence_pattern: Optional recurrence pattern

        Returns:
            The created task

        Raises:
            ValueError: If validation fails
        """
        with self._lock:
            now = datetime.now()
            # Normalize categories
            normalized_categories = validate_categories(categories)
            task = Task(
                id=self._next_id,
                title=title,
                description=description,
                priority=priority,
                categories=normalized_categories,
                due_date=due_date,
                recurrence_pattern=recurrence_pattern,
                created_at=now,
                updated_at=now,
            )
            self._tasks[self._next_id] = task
            self._next_id += 1
            return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: Task ID to retrieve

        Returns:
            Task if found, None otherwise
        """
        with self._lock:
            return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks
        """
        with self._lock:
            return list(self._tasks.values())

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update a task.

        Args:
            task_id: Task ID to update
            **kwargs: Fields to update

        Returns:
            Updated task if found, None otherwise

        Raises:
            ValueError: If validation fails
        """
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None

            # Update fields
            update_data = task.model_dump()
            update_data.update(kwargs)
            update_data["updated_at"] = datetime.now()

            # Create new task instance with updated data
            updated_task = Task(**update_data)
            self._tasks[task_id] = updated_task
            return updated_task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: Task ID to delete

        Returns:
            True if task was deleted, False if not found
        """
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def clear_all_tasks(self) -> None:
        """Clear all tasks (for testing)."""
        with self._lock:
            self._tasks.clear()
            self._next_id = 1
