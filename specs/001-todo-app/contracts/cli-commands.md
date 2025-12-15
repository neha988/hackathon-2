# CLI Command Contracts: Todo Console Application

**Feature**: 001-todo-app
**Phase**: 1 (Design & Contracts)
**Date**: 2025-12-10

## Overview

This document defines the command-line interface contracts for the Todo Console Application. All commands use Click framework and follow consistent patterns.

## Global Command Structure

```bash
todo [GLOBAL_OPTIONS] COMMAND [COMMAND_OPTIONS] [ARGUMENTS]
```

**Global Options** (apply to all commands):
- `--help` - Show help message and exit
- `--version` - Show version and exit

---

## Command Index

| Command | Purpose | Functional Requirements |
|---------|---------|-------------------------|
| `add` | Create new task | FR-001, FR-002, FR-010, FR-012, FR-021, FR-025 |
| `list` | View all tasks (with filters) | FR-003, FR-015, FR-016, FR-017, FR-018, FR-035 |
| `update` | Modify existing task | FR-004, FR-010, FR-012, FR-023, FR-025 |
| `delete` | Remove task | FR-005 |
| `complete` | Toggle task completion status | FR-006, FR-022 (triggers recurrence) |
| `search` | Search tasks by keyword | FR-014 |
| `sort` | Display tasks sorted by criteria | FR-018 |

---

## Command Specifications

### 1. `add` - Create New Task

**Purpose**: Add a new task to the list (FR-001, FR-002)

**Syntax**:
```bash
todo add "TITLE" [OPTIONS]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| TITLE | str | Yes | Task title (1-200 chars) |

**Options**:
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--description` | `-d` | str | "" | Task description (max 1000 chars) |
| `--priority` | `-p` | choice | MEDIUM | Priority level (HIGH/MEDIUM/LOW) |
| `--category` | `-c` | str (multiple) | [] | Category tags (can specify multiple times) |
| `--due` | | str | None | Due date/time (ISO or natural language) |
| `--recurring` | `-r` | choice | None | Recurrence pattern (DAILY/WEEKLY/MONTHLY) |

**Examples**:
```bash
# Basic task
todo add "Buy groceries"

# Task with description and priority
todo add "Submit report" -d "Q4 financial report" -p HIGH

# Task with categories
todo add "Team meeting" -c work -c meetings

# Task with due date (ISO format)
todo add "Pay bills" --due "2025-12-15 14:00"

# Task with due date (natural language)
todo add "Call mom" --due "tomorrow at 3pm"

# Recurring task
todo add "Daily standup" -r DAILY --due "tomorrow at 9am"
```

**Success Output**:
```
✓ Task created successfully
  ID: 5
  Title: Buy groceries
  Priority: MEDIUM
  Status: Pending
```

**Error Cases**:
| Error Condition | Exit Code | Error Message |
|-----------------|-----------|---------------|
| Empty title | 1 | "Error: Title is required (1-200 characters)" |
| Title too long (>200) | 1 | "Error: Title maximum 200 characters" |
| Description too long (>1000) | 1 | "Error: Description maximum 1000 characters" |
| Invalid priority | 1 | "Error: Priority must be HIGH, MEDIUM, or LOW" |
| Invalid category | 1 | "Error: Category must be alphanumeric (max 50 chars)" |
| Invalid due date format | 1 | "Error: Could not parse due date. Use ISO format (YYYY-MM-DD HH:MM) or natural language" |
| Due date in past | 1 | "Error: Due date must be in the future" |
| Invalid recurrence pattern | 1 | "Error: Recurrence must be DAILY, WEEKLY, or MONTHLY" |

**Mapping to Spec**:
- FR-001: Allow users to add task with title and description
- FR-002: Assign unique ID automatically
- FR-010: Allow priority assignment
- FR-012: Allow category tags
- FR-021: Allow recurring tasks
- FR-025: Allow due date/time

---

### 2. `list` - View Tasks

**Purpose**: Display all tasks in formatted table (FR-003)

**Syntax**:
```bash
todo list [OPTIONS]
```

**Options**:
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--status` | `-s` | choice | all | Filter by status (all/pending/completed) |
| `--priority` | `-p` | choice | None | Filter by priority (HIGH/MEDIUM/LOW) |
| `--category` | `-c` | str | None | Filter by category tag |
| `--sort-by` | | choice | created | Sort by (created/due/priority/title) |
| `--limit` | `-n` | int | None | Limit number of results |

**Examples**:
```bash
# List all tasks
todo list

# List only pending tasks
todo list --status pending

# List HIGH priority tasks
todo list -p HIGH

# List work-related tasks
todo list -c work

# List tasks sorted by due date
todo list --sort-by due

# Combine filters
todo list -s pending -p HIGH --sort-by due

# Limit results
todo list -n 10
```

**Success Output** (Rich formatted table):
```
┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Status   ┃ Priority ┃ Categories ┃ Due Date           ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 1  │ Buy groceries  │ Pending  │ MEDIUM   │ home       │ -                  │
│ 2  │ Submit report  │ Pending  │ HIGH     │ work       │ 2025-12-15 14:00   │
│ 3  │ Call mom       │ Complete │ LOW      │ personal   │ -                  │
└────┴────────────────┴──────────┴──────────┴────────────┴────────────────────┘

Showing 3 of 10 tasks
```

**Color Coding** (FR-013):
- HIGH priority: Red text
- MEDIUM priority: Yellow text
- LOW priority: Green text
- Overdue tasks: Red background
- Due today: Yellow background

**Empty Result**:
```
No tasks match current filters
```

**Mapping to Spec**:
- FR-003: View all tasks in formatted table
- FR-013: Color-coded priority indicators
- FR-015: Filter by status
- FR-016: Filter by priority
- FR-017: Filter by category
- FR-018: Sort by various criteria
- FR-019: Combine multiple filters
- FR-020: Show "no match" message
- FR-035: Display task counts

---

### 3. `update` - Modify Task

**Purpose**: Update existing task details (FR-004)

**Syntax**:
```bash
todo update TASK_ID [OPTIONS]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| TASK_ID | int | Yes | ID of task to update |

**Options**:
| Option | Short | Type | Description |
|--------|-------|------|-------------|
| `--title` | `-t` | str | New title |
| `--description` | `-d` | str | New description |
| `--priority` | `-p` | choice | New priority (HIGH/MEDIUM/LOW) |
| `--add-category` | `-c` | str (multiple) | Add category tags |
| `--remove-category` | | str (multiple) | Remove category tags |
| `--due` | | str | New due date/time |
| `--recurring` | `-r` | choice | New recurrence pattern |
| `--no-recurring` | | flag | Remove recurrence pattern |

**Examples**:
```bash
# Update title
todo update 5 -t "Buy groceries and fruits"

# Update priority
todo update 3 -p HIGH

# Add categories
todo update 2 -c urgent -c important

# Remove category
todo update 2 --remove-category urgent

# Update due date
todo update 1 --due "next Monday at 2pm"

# Change recurrence pattern
todo update 4 -r WEEKLY

# Remove recurrence
todo update 4 --no-recurring
```

**Success Output**:
```
✓ Task updated successfully
  ID: 5
  Title: Buy groceries and fruits (updated)
  Priority: HIGH (updated)
```

**Error Cases**:
| Error Condition | Exit Code | Error Message |
|-----------------|-----------|---------------|
| Task not found | 1 | "Error: Task with ID {id} not found" |
| Invalid task ID | 1 | "Error: Task ID must be a positive integer" |
| No updates provided | 1 | "Error: No updates specified. Use --help to see available options" |
| Same validation errors as `add` command for respective fields |

**Mapping to Spec**:
- FR-004: Update task title and description
- FR-010: Update priority
- FR-012: Update categories
- FR-023: Update or remove recurrence pattern
- FR-025: Update due date

---

### 4. `delete` - Remove Task

**Purpose**: Delete a task from the list (FR-005)

**Syntax**:
```bash
todo delete TASK_ID [OPTIONS]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| TASK_ID | int | Yes | ID of task to delete |

**Options**:
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--confirm` | `-y` | flag | False | Skip confirmation prompt |

**Examples**:
```bash
# Delete with confirmation
todo delete 5
> Are you sure you want to delete task 5 "Buy groceries"? [y/N]: y

# Delete without confirmation
todo delete 5 -y
```

**Success Output**:
```
✓ Task deleted successfully
  ID: 5
  Title: Buy groceries
```

**Error Cases**:
| Error Condition | Exit Code | Error Message |
|-----------------|-----------|---------------|
| Task not found | 1 | "Error: Task with ID {id} not found" |
| User cancels | 0 | "Deletion cancelled" |

**Mapping to Spec**:
- FR-005: Delete task by ID
- FR-024: Deleting recurring task does NOT generate next instance

---

### 5. `complete` - Toggle Completion

**Purpose**: Mark task as complete or incomplete (FR-006)

**Syntax**:
```bash
todo complete TASK_ID
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| TASK_ID | int | Yes | ID of task to toggle |

**Examples**:
```bash
# Mark as complete
todo complete 3

# Toggle back to pending (if already complete)
todo complete 3
```

**Success Output (Pending → Complete)**:
```
✓ Task marked as complete
  ID: 3
  Title: Call mom
  Status: Complete → Pending
```

**Success Output (Pending → Complete, Recurring Task)**:
```
✓ Task marked as complete
  ID: 3
  Title: Daily standup
  Status: Complete

✓ Next instance created
  ID: 15
  Title: Daily standup
  Due: 2025-12-11 09:00
  Recurrence: DAILY
```

**Error Cases**:
| Error Condition | Exit Code | Error Message |
|-----------------|-----------|---------------|
| Task not found | 1 | "Error: Task with ID {id} not found" |

**Mapping to Spec**:
- FR-006: Toggle completion status
- FR-022: Auto-generate next recurring task instance on completion

---

### 6. `search` - Search Tasks

**Purpose**: Search tasks by keyword (FR-014)

**Syntax**:
```bash
todo search KEYWORD [OPTIONS]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| KEYWORD | str | Yes | Search term (case-insensitive) |

**Options**:
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--sort-by` | | choice | created | Sort results (created/due/priority/title) |

**Examples**:
```bash
# Search for tasks containing "meeting"
todo search meeting

# Search with sorting
todo search report --sort-by due
```

**Success Output** (same table format as `list`):
```
Search results for "meeting" (2 tasks found)

┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Status   ┃ Priority ┃ Categories ┃ Due Date           ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 4  │ Team meeting   │ Pending  │ MEDIUM   │ work       │ 2025-12-12 10:00   │
│ 7  │ Meeting prep   │ Pending  │ HIGH     │ work       │ 2025-12-11 09:00   │
└────┴────────────────┴──────────┴──────────┴────────────┴────────────────────┘
```

**No Results**:
```
No tasks found for "nonexistent"
```

**Mapping to Spec**:
- FR-014: Case-insensitive keyword search in title and description
- FR-018: Sort search results

---

### 7. `sort` - Display Sorted Tasks

**Purpose**: Display tasks sorted by specified criteria (FR-018)

**Syntax**:
```bash
todo sort SORT_BY [OPTIONS]
```

**Arguments**:
| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| SORT_BY | choice | Yes | Sort criteria (due/priority/created/title) |

**Options**:
| Option | Short | Type | Default | Description |
|--------|-------|------|---------|-------------|
| `--reverse` | `-r` | flag | False | Reverse sort order |

**Sort Orders**:
- `due`: Overdue first, then due today, then future (ascending)
- `priority`: HIGH → MEDIUM → LOW
- `created`: Oldest first (use --reverse for newest first)
- `title`: Alphabetical (A-Z)

**Examples**:
```bash
# Sort by due date
todo sort due

# Sort by priority
todo sort priority

# Sort by title (reverse alphabetical)
todo sort title --reverse
```

**Success Output** (same table format as `list` with sort indicator):
```
Tasks sorted by: Due Date

┏━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ ID ┃ Title          ┃ Status   ┃ Priority ┃ Categories ┃ Due Date           ┃
┡━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ 2  │ Submit report  │ Pending  │ HIGH     │ work       │ 2025-12-10 14:00 ⚠ │
│ 3  │ Call mom       │ Pending  │ LOW      │ personal   │ 2025-12-11 15:00   │
│ 1  │ Buy groceries  │ Pending  │ MEDIUM   │ home       │ 2025-12-15 10:00   │
└────┴────────────────┴──────────┴──────────┴────────────┴────────────────────┘

⚠ = Overdue or due today
```

**Mapping to Spec**:
- FR-018: Sort by due date, priority, creation date, title

---

## Global Behaviors

### Help Documentation (FR-031)

Every command supports `--help`:

```bash
todo --help
todo add --help
todo list --help
# ... etc
```

Output includes:
- Command description
- Usage syntax
- All options with descriptions
- Examples

### Error Handling (FR-009, FR-033)

**Consistent Error Format**:
```
Error: [Clear, actionable error message]

Use 'todo COMMAND --help' for more information.
```

**Keyboard Interrupt (Ctrl+C)**:
```bash
^C
Exiting gracefully. Your tasks are safe!
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (invalid input, task not found, validation failure) |
| 130 | Interrupted by user (Ctrl+C) |

---

## Testing Contracts

### CLI Testing Strategy

Use Click's `CliRunner` for integration tests:

```python
from click.testing import CliRunner
from src.cli.main import cli

def test_add_command():
    runner = CliRunner()
    result = runner.invoke(cli, ['add', 'Buy groceries', '-p', 'HIGH'])

    assert result.exit_code == 0
    assert 'Task created successfully' in result.output
    assert 'ID: 1' in result.output
```

### Contract Compliance Tests

Each command must have tests verifying:
- [x] Help text is displayed with `--help`
- [x] Success output matches format specification
- [x] Error messages match specification
- [x] Exit codes are correct
- [x] All options work as documented
- [x] Examples from this document work

---

## Future Extensions (Phase II+)

**Potential New Commands**:
- `todo login` - Authenticate user (Phase II with Better Auth)
- `todo sync` - Sync with cloud database (Phase II+)
- `todo export` - Export tasks to JSON/CSV
- `todo import` - Import tasks from file

**API Surface** (for future integration):
- All CLI commands will wrap TaskService methods
- Services can be reused by web API, chatbot, etc.
- Storage abstraction allows swapping backends

---

## Conclusion

CLI contract aligns with:
- ✅ All 40 functional requirements (FR-001 to FR-040)
- ✅ User scenarios from spec (5 user stories)
- ✅ Success criteria (intuitive commands, clear feedback)
- ✅ Constitution principles (help docs, error handling, UX)

Ready for implementation via `/sp.tasks` and `/sp.implement`.
