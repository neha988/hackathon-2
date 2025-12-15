# Data Model: Todo Console Application

**Feature**: 001-todo-app
**Phase**: 1 (Design & Contracts)
**Date**: 2025-12-10

## Overview

This document defines the data entities, their relationships, validation rules, and state transitions for the Todo Console Application.

## Entity Definitions

### 1. Task

**Purpose**: Represents a todo item with all associated metadata

**Attributes**:

| Field | Type | Required | Default | Validation Rules |
|-------|------|----------|---------|------------------|
| `id` | int | Yes (auto) | Auto-increment | Unique, positive integer |
| `title` | str | Yes | N/A | 1-200 characters, non-empty, no whitespace-only |
| `description` | str | No | "" | Max 1000 characters |
| `completed` | bool | Yes | False | True or False |
| `priority` | Priority (enum) | Yes | MEDIUM | Must be HIGH, MEDIUM, or LOW |
| `categories` | List[str] | Yes | [] | Each category: alphanumeric, max 50 chars |
| `due_date` | datetime | No | None | ISO format, must be future date at creation |
| `recurrence_pattern` | RecurrencePattern | No | None | DAILY, WEEKLY, or MONTHLY (if set) |
| `created_at` | datetime | Yes (auto) | datetime.now() | ISO format, automatically set |
| `updated_at` | datetime | Yes (auto) | datetime.now() | ISO format, auto-updated on modification |

**Pydantic Model Structure**:

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional
from enum import Enum

class Priority(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class RecurrencePattern(str, Enum):
    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"

class Task(BaseModel):
    id: int = Field(default=0, description="Unique task identifier (auto-assigned)")
    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: str = Field(default="", max_length=1000, description="Task description")
    completed: bool = Field(default=False, description="Completion status")
    priority: Priority = Field(default=Priority.MEDIUM, description="Task priority level")
    categories: List[str] = Field(default_factory=list, description="Category tags")
    due_date: Optional[datetime] = Field(default=None, description="Due date and time")
    recurrence_pattern: Optional[RecurrencePattern] = Field(default=None, description="Recurrence pattern")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update timestamp")

    @field_validator('title')
    @classmethod
    def title_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v.strip()

    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v: List[str]) -> List[str]:
        for category in v:
            if len(category) > 50:
                raise ValueError(f"Category '{category}' exceeds 50 characters")
            if not category.replace('_', '').replace('-', '').isalnum():
                raise ValueError(f"Category '{category}' must be alphanumeric (hyphens and underscores allowed)")
        return v

    @field_validator('due_date')
    @classmethod
    def due_date_future(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is not None and v < datetime.now():
            raise ValueError("Due date must be in the future")
        return v
```

**State Transitions**:

```
┌─────────┐                                ┌───────────┐
│ Pending │ ─── toggle_completion() ────→ │ Completed │
│         │                                │           │
└─────────┘ ←── toggle_completion() ───── └───────────┘
```

**Derived Properties** (computed, not stored):

- `is_overdue: bool` - True if due_date < now() and not completed
- `is_due_today: bool` - True if due_date.date() == today()
- `is_due_soon: bool` - True if 0 < (due_date - now()) < 24 hours
- `is_recurring: bool` - True if recurrence_pattern is not None

---

### 2. Priority (Enum)

**Purpose**: Categorize task urgency and importance

**Values**:

| Value | Display | Color (Rich) | Sort Order |
|-------|---------|--------------|------------|
| HIGH | HIGH | red | 1 (highest) |
| MEDIUM | MEDIUM | yellow | 2 |
| LOW | LOW | green | 3 (lowest) |

**Usage**:
- Assigned to tasks via `task.priority`
- Used for filtering (FR-016)
- Used for sorting (FR-018)
- Affects visual display color-coding (FR-013)

---

### 3. RecurrencePattern (Enum)

**Purpose**: Define how often a recurring task repeats

**Values**:

| Value | Description | Next Instance Logic |
|-------|-------------|---------------------|
| DAILY | Repeats every day | `due_date + timedelta(days=1)` |
| WEEKLY | Repeats every 7 days | `due_date + timedelta(weeks=1)` |
| MONTHLY | Repeats same day of month | `due_date + relativedelta(months=1)` |

**Behavior**:
- When a recurring task is marked complete (FR-022):
  1. Current task remains in storage with `completed=True`
  2. New task instance is created with:
     - Same title, description, priority, categories, recurrence_pattern
     - New `due_date` calculated using pattern logic
     - `completed=False`
     - New auto-assigned ID
     - New `created_at` timestamp

- When a recurring task is deleted (FR-024):
  - Task is removed from storage
  - NO new instance is created (only completion triggers recurrence)

**Implementation Note**: Use `dateutil.relativedelta` for MONTHLY pattern to handle varying month lengths.

---

### 4. Reminder (Transient)

**Purpose**: System-generated notification for approaching due dates

**Note**: This is NOT a stored entity - reminders are generated on-the-fly by ReminderService

**Properties**:

| Field | Type | Description |
|-------|------|-------------|
| task_id | int | ID of task being reminded |
| task_title | str | Title for display |
| due_at | datetime | When task is due |
| time_until_due | timedelta | Time remaining |

**Trigger Logic**:
- Check every 60 seconds when app is running
- Display reminder if: `0 < (due_date - now()) <= 1 hour` and task not completed
- Format: `⏰ REMINDER: "{task_title}" is due in {time_until_due.minutes} minutes`

---

## Entity Relationships

```
┌─────────────────────┐
│       Task          │
├─────────────────────┤
│ + id: int           │───┐
│ + title: str        │   │
│ + description: str  │   │
│ + completed: bool   │   │
│ + priority: ────────┼───┼──→ ┌──────────┐
│ + categories: list  │   │    │ Priority │
│ + due_date: dt      │   │    ├──────────┤
│ + recurrence: ──────┼───┼─→  │ HIGH     │
│ + created_at: dt    │   │    │ MEDIUM   │
│ + updated_at: dt    │   │    │ LOW      │
└─────────────────────┘   │    └──────────┘
                          │
                          └──→ ┌────────────────────┐
                               │ RecurrencePattern  │
                               ├────────────────────┤
                               │ DAILY              │
                               │ WEEKLY             │
                               │ MONTHLY            │
                               └────────────────────┘
```

**Cardinality**:
- **Task ↔ Priority**: Many-to-One (many tasks can have same priority)
- **Task ↔ RecurrencePattern**: Many-to-Optional-One (many tasks can have same pattern, or none)
- **Task ↔ Categories**: One-to-Many (one task can have multiple categories)

---

## Storage Schema

### In-Memory Storage Structure

```python
class InMemoryTaskStore:
    """Thread-safe in-memory task storage"""

    def __init__(self):
        self._tasks: Dict[int, Task] = {}  # task_id → Task object
        self._next_id: int = 1             # Auto-increment counter
        self._lock: threading.Lock = threading.Lock()  # Thread safety

    # Storage operations (all thread-safe)
    def add(self, task: Task) -> int: ...
    def get(self, task_id: int) -> Optional[Task]: ...
    def update(self, task_id: int, updates: Dict[str, Any]) -> bool: ...
    def delete(self, task_id: int) -> bool: ...
    def get_all(self) -> List[Task]: ...
    def get_by_filter(self, **filters) -> List[Task]: ...
```

### Indexes (Virtual - Implemented via Python)

For efficient querying, we maintain virtual indexes:

```python
# Search index (for FR-014)
def search(self, keyword: str) -> List[Task]:
    """O(n) search - acceptable for 10,000 tasks"""
    keyword_lower = keyword.lower()
    return [
        task for task in self._tasks.values()
        if keyword_lower in task.title.lower()
        or keyword_lower in task.description.lower()
    ]

# Filter index (for FR-015, FR-016, FR-017)
def filter_by(self, status=None, priority=None, category=None) -> List[Task]:
    """Multiple filter support"""
    results = list(self._tasks.values())

    if status == "pending":
        results = [t for t in results if not t.completed]
    elif status == "completed":
        results = [t for t in results if t.completed]

    if priority:
        results = [t for t in results if t.priority == priority]

    if category:
        results = [t for t in results if category in t.categories]

    return results
```

---

## Validation Rules Summary

### Title Validation (FR-037, FR-038)

```python
def validate_title(title: str) -> str:
    """Validates title according to spec"""
    if not title or not title.strip():
        raise ValueError("Title is required (1-200 characters)")
    if len(title) > 200:
        raise ValueError("Title maximum 200 characters")
    return title.strip()
```

### Description Validation (FR-038)

```python
def validate_description(description: str) -> str:
    """Validates description according to spec"""
    if len(description) > 1000:
        raise ValueError("Description maximum 1000 characters")
    return description
```

### Category Validation (FR-038)

```python
def validate_category(category: str) -> str:
    """Validates category tag according to spec"""
    if len(category) > 50:
        raise ValueError(f"Category '{category}' exceeds 50 characters")
    if not category.replace('_', '').replace('-', '').isalnum():
        raise ValueError("Category must be alphanumeric (hyphens/underscores allowed)")
    return category
```

### Due Date Validation (FR-026)

```python
def validate_due_date(due_date: datetime) -> datetime:
    """Validates due date is in future"""
    if due_date < datetime.now():
        raise ValueError("Due date must be in the future")
    return due_date
```

---

## Performance Considerations

| Operation | Time Complexity | Notes |
|-----------|-----------------|-------|
| Add task | O(1) | Dict insert with auto-increment ID |
| Get task by ID | O(1) | Dict lookup |
| Update task | O(1) | Dict update |
| Delete task | O(1) | Dict delete |
| List all tasks | O(n) | Iterate all tasks (n ≤ 10,000) |
| Search tasks | O(n) | String matching on title + description |
| Filter tasks | O(n) | Filter on status/priority/category |
| Sort tasks | O(n log n) | Python's Timsort algorithm |

**Scalability**: All operations meet performance goals for 10,000 tasks:
- Search/filter/sort: <1s for 1,000 tasks (constitution requirement)
- List 100 tasks: <2s (constitution requirement)

---

## Testing Strategy

### Model Tests (`tests/unit/test_models.py`)

```python
def test_task_validation():
    """Test Pydantic validation rules"""
    # Valid task
    task = Task(title="Buy groceries", priority=Priority.HIGH)
    assert task.title == "Buy groceries"

    # Invalid title (empty)
    with pytest.raises(ValidationError):
        Task(title="")

    # Invalid title (too long)
    with pytest.raises(ValidationError):
        Task(title="x" * 201)

    # Invalid due date (past)
    with pytest.raises(ValidationError):
        Task(title="Test", due_date=datetime(2020, 1, 1))
```

### Storage Tests (`tests/unit/test_task_store.py`)

```python
def test_concurrent_access():
    """Test thread-safe storage operations"""
    store = InMemoryTaskStore()
    # ... concurrent read/write tests with threading
```

---

## Migration Path (Future Phases)

**Phase II** (Full-Stack Web App):
- Replace InMemoryTaskStore with DatabaseTaskStore (SQLModel + PostgreSQL)
- Add `user_id: str` field to Task model
- Add relationship: User (1) ↔ Tasks (many)
- Keep all validation rules and Pydantic models

**Changes Required**:
```python
class Task(BaseModel):
    user_id: str  # Foreign key to users table
    # ... rest remains same
```

---

## Conclusion

Data model aligns with:
- ✅ All 5 key entities from spec (Task, Priority, Category, RecurrencePattern, Reminder)
- ✅ 40 functional requirements (FR-001 to FR-040)
- ✅ Validation rules from edge cases section
- ✅ Performance goals (10,000 tasks, <1s operations)
- ✅ Constitution principles (type safety, validation, testing)

Ready to proceed to contract definitions.
