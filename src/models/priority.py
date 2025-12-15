"""Priority enum for task prioritization."""

from enum import Enum


class Priority(str, Enum):
    """Task priority levels.

    Attributes:
        HIGH: Highest priority tasks
        MEDIUM: Standard priority tasks (default)
        LOW: Lowest priority tasks
    """

    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
