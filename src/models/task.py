"""Task model for todo application."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .priority import Priority
from .recurrence import RecurrencePattern


class Task(BaseModel):
    """Task model with validation.

    Attributes:
        id: Unique task identifier
        title: Task title (1-200 characters)
        description: Task description (0-1000 characters)
        completed: Completion status
        priority: Task priority level
        categories: List of category tags
        due_date: Optional due date/time
        recurrence_pattern: Optional recurrence pattern for recurring tasks
        created_at: Task creation timestamp
        updated_at: Task last update timestamp
    """

    id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    priority: Priority = Field(default=Priority.MEDIUM)
    categories: List[str] = Field(default_factory=list)
    due_date: Optional[datetime] = Field(default=None)
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None)
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic model configuration."""

        use_enum_values = True
        json_encoders = {datetime: lambda v: v.isoformat()}
