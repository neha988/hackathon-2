"""Validation utilities for user inputs."""

from typing import List, Optional

from src.models.priority import Priority
from src.models.recurrence import RecurrencePattern


def validate_title(title: str) -> str:
    """Validate task title.

    Args:
        title: Task title to validate

    Returns:
        Validated title

    Raises:
        ValueError: If title is empty or too long
    """
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty")

    title = title.strip()
    if len(title) > 200:
        raise ValueError("Task title cannot exceed 200 characters")

    return title


def validate_description(description: str) -> str:
    """Validate task description.

    Args:
        description: Task description to validate

    Returns:
        Validated description

    Raises:
        ValueError: If description is too long
    """
    description = description.strip()
    if len(description) > 1000:
        raise ValueError("Task description cannot exceed 1000 characters")

    return description


def validate_priority(priority: str) -> str:
    """Validate priority value.

    Args:
        priority: Priority string to validate

    Returns:
        Validated priority value

    Raises:
        ValueError: If priority is invalid
    """
    priority_upper = priority.upper()
    valid_priorities = [p.value for p in Priority]

    if priority_upper not in valid_priorities:
        raise ValueError(
            f"Invalid priority '{priority}'. Must be one of: {', '.join(valid_priorities)}"
        )

    return priority_upper


def validate_recurrence_pattern(pattern: str) -> str:
    """Validate recurrence pattern value.

    Args:
        pattern: Recurrence pattern string to validate

    Returns:
        Validated recurrence pattern value

    Raises:
        ValueError: If recurrence pattern is invalid
    """
    pattern_upper = pattern.upper()
    valid_patterns = [p.value for p in RecurrencePattern]

    if pattern_upper not in valid_patterns:
        raise ValueError(
            f"Invalid recurrence pattern '{pattern}'. Must be one of: {', '.join(valid_patterns)}"
        )

    return pattern_upper


def validate_categories(categories: Optional[List[str]]) -> List[str]:
    """Validate and normalize category tags.

    Args:
        categories: List of category tags to validate

    Returns:
        Validated and normalized category list

    Raises:
        ValueError: If any category is invalid
    """
    if not categories:
        return []

    validated = []
    for category in categories:
        category = category.strip()
        if not category:
            continue

        if len(category) > 50:
            raise ValueError(f"Category '{category}' exceeds 50 characters")

        if "," in category:
            raise ValueError(f"Category '{category}' cannot contain commas")

        validated.append(category.lower())

    return validated


def validate_task_id(task_id: str) -> int:
    """Validate and convert task ID.

    Args:
        task_id: Task ID string to validate

    Returns:
        Validated task ID as integer

    Raises:
        ValueError: If task ID is invalid
    """
    try:
        id_int = int(task_id)
        if id_int < 1:
            raise ValueError("Task ID must be a positive integer")
        return id_int
    except ValueError:
        raise ValueError(f"Invalid task ID '{task_id}'. Must be a positive integer")
