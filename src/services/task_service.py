"""Task service with business logic."""

from datetime import datetime, timedelta
from typing import List, Optional

from src.models.recurrence import RecurrencePattern
from src.models.task import Task
from src.storage.task_store import InMemoryTaskStore


class TaskService:
    """Service layer for task operations.

    Attributes:
        store: Task storage backend
    """

    def __init__(self, store: InMemoryTaskStore) -> None:
        """Initialize task service.

        Args:
            store: Task storage instance
        """
        self.store = store

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: str = "MEDIUM",
        categories: Optional[List[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence_pattern: Optional[str] = None,
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title
            description: Task description
            priority: Task priority
            categories: Category tags
            due_date: Optional due date
            recurrence_pattern: Optional recurrence pattern

        Returns:
            Created task

        Raises:
            ValueError: If validation fails
        """
        return self.store.add_task(
            title=title,
            description=description,
            priority=priority,
            categories=categories,
            due_date=due_date,
            recurrence_pattern=recurrence_pattern,
        )

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get task by ID.

        Args:
            task_id: Task ID

        Returns:
            Task if found, None otherwise
        """
        return self.store.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all tasks
        """
        return self.store.get_all_tasks()

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task fields.

        Args:
            task_id: Task ID to update
            **kwargs: Fields to update

        Returns:
            Updated task if found, None otherwise

        Raises:
            ValueError: If validation fails
        """
        return self.store.update_task(task_id, **kwargs)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: Task ID to delete

        Returns:
            True if deleted, False if not found
        """
        return self.store.delete_task(task_id)

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status.

        If task is recurring and being marked complete, creates next occurrence.

        Args:
            task_id: Task ID to toggle

        Returns:
            Updated task if found, None otherwise
        """
        task = self.store.get_task(task_id)
        if task is None:
            return None

        # Mark current task as complete
        updated_task = self.store.update_task(task_id, completed=not task.completed)

        # If task has recurrence and is being marked complete, create next occurrence
        if (
            updated_task
            and updated_task.completed
            and updated_task.recurrence_pattern is not None
        ):
            self._create_next_recurrence(updated_task)

        return updated_task

    def _create_next_recurrence(self, task: Task) -> Task:
        """Create next occurrence of recurring task.

        Args:
            task: Completed recurring task

        Returns:
            Newly created task for next occurrence
        """
        if task.recurrence_pattern is None or task.due_date is None:
            raise ValueError("Task must have recurrence pattern and due date")

        # Handle priority and recurrence (could be enum or string due to use_enum_values)
        priority_val = task.priority.value if hasattr(task.priority, 'value') else task.priority
        recurrence_val = task.recurrence_pattern.value if hasattr(task.recurrence_pattern, 'value') else task.recurrence_pattern

        # Calculate next due date
        if recurrence_val == "DAILY":
            next_due_date = task.due_date + timedelta(days=1)
        elif recurrence_val == "WEEKLY":
            next_due_date = task.due_date + timedelta(weeks=1)
        elif recurrence_val == "MONTHLY":
            # Approximate month as 30 days
            next_due_date = task.due_date + timedelta(days=30)
        else:
            next_due_date = task.due_date

        # Create new task with same properties but new due date
        return self.store.add_task(
            title=task.title,
            description=task.description,
            priority=priority_val,
            categories=task.categories,
            due_date=next_due_date,
            recurrence_pattern=recurrence_val,
        )

    def filter_tasks(
        self,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
        category: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by criteria.

        Args:
            completed: Filter by completion status
            priority: Filter by priority
            category: Filter by category

        Returns:
            Filtered list of tasks
        """
        tasks = self.store.get_all_tasks()

        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]

        if priority is not None:
            priority_val = lambda t: t.priority.value if hasattr(t.priority, 'value') else t.priority
            tasks = [t for t in tasks if priority_val(t) == priority.upper()]

        if category is not None:
            tasks = [t for t in tasks if category.lower() in [c.lower() for c in t.categories]]

        return tasks

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by keyword.

        Searches in title and description (case-insensitive).

        Args:
            keyword: Search keyword

        Returns:
            List of matching tasks
        """
        tasks = self.store.get_all_tasks()
        keyword_lower = keyword.lower()

        return [
            t
            for t in tasks
            if keyword_lower in t.title.lower() or keyword_lower in t.description.lower()
        ]

    def sort_tasks(
        self, tasks: List[Task], sort_by: str, reverse: bool = False
    ) -> List[Task]:
        """Sort tasks by specified field.

        Args:
            tasks: List of tasks to sort
            sort_by: Field to sort by (priority, due_date, created_at, title)
            reverse: Reverse sort order

        Returns:
            Sorted list of tasks

        Raises:
            ValueError: If sort_by field is invalid
        """
        # Helper to get priority value (handles both enum and string)
        def get_priority_val(t):
            priority = t.priority.value if hasattr(t.priority, 'value') else t.priority
            return ["LOW", "MEDIUM", "HIGH"].index(priority)

        sort_key_map = {
            "priority": get_priority_val,
            "due_date": lambda t: t.due_date or datetime.max,
            "created_at": lambda t: t.created_at,
            "title": lambda t: t.title.lower(),
        }

        if sort_by not in sort_key_map:
            raise ValueError(
                f"Invalid sort field '{sort_by}'. Must be one of: {', '.join(sort_key_map.keys())}"
            )

        return sorted(tasks, key=sort_key_map[sort_by], reverse=reverse)

    def get_overdue_tasks(self) -> List[Task]:
        """Get tasks that are overdue.

        Returns:
            List of overdue incomplete tasks
        """
        now = datetime.now()
        tasks = self.store.get_all_tasks()

        return [
            t
            for t in tasks
            if not t.completed and t.due_date is not None and t.due_date < now
        ]

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due within specified days.

        Args:
            days: Number of days to look ahead

        Returns:
            List of upcoming incomplete tasks
        """
        now = datetime.now()
        future = now + timedelta(days=days)
        tasks = self.store.get_all_tasks()

        return [
            t
            for t in tasks
            if not t.completed
            and t.due_date is not None
            and now <= t.due_date <= future
        ]
