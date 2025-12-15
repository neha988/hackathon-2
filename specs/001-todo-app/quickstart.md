# Quickstart Guide: Todo Console Application

**Feature**: 001-todo-app
**Phase**: 1 (Design & Contracts)
**Date**: 2025-12-10

## Overview

This guide helps you get started with developing and using the Todo Console Application. For detailed specifications, see [spec.md](./spec.md). For implementation details, see [plan.md](./plan.md).

---

## Prerequisites

### Required Software

| Software | Version | Purpose | Installation |
|----------|---------|---------|--------------|
| Python | 3.13+ | Runtime | https://www.python.org/downloads/ |
| UV | Latest | Package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Git | Latest | Version control | https://git-scm.com/downloads |

### For Windows Users

**You MUST use WSL 2** (Windows Subsystem for Linux):

```bash
# Install WSL 2
wsl --install

# Set WSL 2 as default
wsl --set-default-version 2

# Install Ubuntu
wsl --install -d Ubuntu-22.04

# Verify installation
wsl -l -v
```

All development commands below should be run in WSL terminal.

---

## Project Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd hacathon2

# Verify you're on the correct branch
git branch
# Should show: * 001-todo-app
```

### 2. Initialize UV Project

```bash
# Initialize UV project (if not already done)
uv init

# Sync dependencies (install all packages)
uv sync

# Verify installation
uv run python --version
# Should show: Python 3.13.x
```

### 3. Install Dependencies

The `pyproject.toml` contains all dependencies:

**Production Dependencies**:
```toml
dependencies = [
    "click>=8.1.7",          # CLI framework
    "rich>=13.7.0",          # Console formatting
    "pydantic>=2.5.0",       # Data validation
    "python-dateutil>=2.8.2" # Date parsing
]
```

**Development Dependencies**:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",         # Testing
    "pytest-cov>=4.1.0",     # Coverage
    "freezegun>=1.4.0",      # Time mocking
    "black>=23.12.0",        # Formatting
    "mypy>=1.8.0",           # Type checking
]
```

Install dev dependencies:
```bash
uv sync --extra dev
```

---

## Development Workflow

### Running the Application

```bash
# Run the CLI application
uv run python -m src.cli.main --help

# Examples (once implemented)
uv run python -m src.cli.main add "Buy groceries"
uv run python -m src.cli.main list
uv run python -m src.cli.main complete 1
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run tests with coverage
uv run pytest --cov=src --cov-report=html

# View coverage report (opens in browser)
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux

# Run specific test file
uv run pytest tests/unit/test_models.py

# Run tests matching a pattern
uv run pytest -k "test_add"

# Run with verbose output
uv run pytest -v

# Run with print statements visible
uv run pytest -s
```

### Code Quality

```bash
# Format code with Black
uv run black src/ tests/

# Check formatting (without modifying files)
uv run black --check src/ tests/

# Type check with mypy
uv run mypy src/

# Run all quality checks
uv run black src/ tests/ && uv run mypy src/ && uv run pytest --cov=src
```

---

## Project Structure

```
hacathon2/
├── .specify/
│   ├── memory/
│   │   └── constitution.md       # Project principles
│   ├── templates/                # Spec-Kit Plus templates
│   └── scripts/                  # Automation scripts
├── specs/
│   └── 001-todo-app/
│       ├── spec.md               # Feature specification
│       ├── plan.md               # Implementation plan
│       ├── research.md           # Technology decisions
│       ├── data-model.md         # Entity definitions
│       ├── quickstart.md         # This file
│       ├── contracts/
│       │   └── cli-commands.md   # CLI interface spec
│       └── checklists/
│           └── requirements.md   # Quality checklist
├── src/                          # Source code
│   ├── models/                   # Pydantic data models
│   ├── services/                 # Business logic
│   ├── storage/                  # In-memory storage
│   ├── cli/                      # Click CLI commands
│   └── utils/                    # Helper functions
├── tests/                        # Test files
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   └── edge_cases/               # Edge case tests
├── pyproject.toml                # UV project config
├── README.md                     # User documentation
├── CLAUDE.md                     # Claude Code instructions
└── .gitignore                    # Git ignore rules
```

---

## Quick Command Reference

### UV Commands

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Update all dependencies
uv sync --upgrade

# Run a command in the virtual environment
uv run <command>

# Activate virtual environment manually
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

### Git Workflow

```bash
# Check current status
git status

# Add changes
git add .

# Commit changes
git commit -m "feat: implement basic task CRUD operations"

# Push to remote
git push origin 001-todo-app

# Pull latest changes
git pull origin 001-todo-app
```

### pytest Commands

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term --cov-report=html

# Run specific test
uv run pytest tests/unit/test_models.py::test_task_validation

# Run tests in parallel (faster)
uv run pytest -n auto  # Requires pytest-xdist

# Stop on first failure
uv run pytest -x

# Show local variables on failure
uv run pytest -l
```

---

## Development Tips

### Using Claude Code

This project uses spec-driven development with Claude Code:

1. **Specification First**: All features defined in specs before coding
2. **AI-Assisted**: Use Claude Code to generate code from specifications
3. **Iterative Refinement**: Refine spec if generated code is incorrect
4. **No Manual Coding**: Constitution requires AI-generated code only

**Workflow**:
```bash
# 1. Specify feature
/sp.specify "Add search functionality"

# 2. Plan implementation
/sp.plan

# 3. Generate tasks
/sp.tasks

# 4. Implement
/sp.implement
```

See [CLAUDE.md](../../CLAUDE.md) for detailed Claude Code instructions.

### Type Hints

**Always use type hints** (constitution requirement):

```python
# Good ✅
def add_task(title: str, description: str = "") -> int:
    """Add a new task and return its ID."""
    pass

# Bad ❌
def add_task(title, description=""):
    pass
```

### Docstrings

**Use Google-style docstrings** (constitution requirement):

```python
def calculate_next_due_date(current: datetime, pattern: RecurrencePattern) -> datetime:
    """Calculate next due date for recurring task.

    Args:
        current: Current due date
        pattern: Recurrence pattern (DAILY/WEEKLY/MONTHLY)

    Returns:
        Next due date based on pattern

    Raises:
        ValueError: If pattern is invalid
    """
    pass
```

### Testing Best Practices

1. **Test Organization**: Unit → Integration → Edge Cases
2. **Use Fixtures**: Define reusable test data in `conftest.py`
3. **Parametrize**: Use `@pytest.mark.parametrize` for multiple scenarios
4. **Mock Time**: Use `freezegun` for time-dependent tests
5. **Coverage**: Aim for 80% minimum (constitution requirement)

**Example**:
```python
import pytest
from freezegun import freeze_time

@pytest.mark.parametrize("priority,expected_color", [
    (Priority.HIGH, "red"),
    (Priority.MEDIUM, "yellow"),
    (Priority.LOW, "green"),
])
def test_priority_colors(priority, expected_color):
    assert get_priority_color(priority) == expected_color

@freeze_time("2025-12-10 10:00:00")
def test_reminder_timing():
    # Time is frozen at 2025-12-10 10:00:00
    task = Task(title="Test", due_date=datetime(2025, 12, 10, 11, 0))
    assert should_send_reminder(task) is True  # 1 hour before
```

---

## Common Tasks

### Add a New Command

1. Create command module in `src/cli/`:
   ```python
   # src/cli/export.py
   import click

   @click.command()
   @click.argument('format', type=click.Choice(['json', 'csv']))
   def export(format: str):
       """Export tasks to file."""
       click.echo(f"Exporting to {format}...")
   ```

2. Register in `src/cli/main.py`:
   ```python
   from .export import export

   cli.add_command(export)
   ```

3. Add tests in `tests/integration/`:
   ```python
   def test_export_command():
       runner = CliRunner()
       result = runner.invoke(cli, ['export', 'json'])
       assert result.exit_code == 0
   ```

### Add a New Model Field

1. Update Pydantic model:
   ```python
   class Task(BaseModel):
       new_field: Optional[str] = None
   ```

2. Update validation if needed:
   ```python
   @field_validator('new_field')
   @classmethod
   def validate_new_field(cls, v):
       # validation logic
       return v
   ```

3. Update tests:
   ```python
   def test_new_field_validation():
       task = Task(title="Test", new_field="value")
       assert task.new_field == "value"
   ```

### Debug Issues

```bash
# Run with verbose output
uv run pytest -vv

# Show print statements
uv run pytest -s

# Drop into debugger on failure
uv run pytest --pdb

# Use Python debugger in code
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

---

## Troubleshooting

### Issue: UV command not found

**Solution**:
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"

# Restart terminal
```

### Issue: Python version mismatch

**Solution**:
```bash
# Check Python version
python --version

# Install Python 3.13 if needed
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.13

# On macOS with Homebrew:
brew install python@3.13
```

### Issue: Tests failing with import errors

**Solution**:
```bash
# Ensure you're in project root
pwd

# Reinstall dependencies
uv sync

# Run tests with Python path
PYTHONPATH=. uv run pytest
```

### Issue: Coverage report not generating

**Solution**:
```bash
# Install coverage dev dependencies
uv sync --extra dev

# Run with explicit coverage
uv run pytest --cov=src --cov-report=html --cov-report=term

# Check htmlcov/ directory was created
ls htmlcov/
```

---

## Next Steps

1. **Read Specifications**:
   - [spec.md](./spec.md) - Feature requirements
   - [plan.md](./plan.md) - Implementation plan
   - [data-model.md](./data-model.md) - Entity definitions
   - [contracts/cli-commands.md](./contracts/cli-commands.md) - CLI interface

2. **Generate Implementation Tasks**:
   ```bash
   /sp.tasks
   ```

3. **Start Implementation**:
   ```bash
   /sp.implement
   ```

4. **Run Tests Frequently**:
   ```bash
   uv run pytest --cov=src
   ```

5. **Review Constitution**:
   - Read `.specify/memory/constitution.md` for project principles
   - Ensure all code follows clean architecture patterns
   - Maintain 80% test coverage
   - Use type hints and docstrings

---

## Getting Help

### Documentation

- **Project Constitution**: `.specify/memory/constitution.md`
- **Feature Spec**: `specs/001-todo-app/spec.md`
- **Implementation Plan**: `specs/001-todo-app/plan.md`
- **CLI Reference**: `specs/001-todo-app/contracts/cli-commands.md`

### External Resources

- **Click Documentation**: https://click.palletsprojects.com/
- **Rich Documentation**: https://rich.readthedocs.io/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **pytest Documentation**: https://docs.pytest.org/
- **UV Documentation**: https://docs.astral.sh/uv/

### Command Help

Every CLI command has built-in help:
```bash
todo --help
todo add --help
todo list --help
```

---

## Quick Reference Card

| Task | Command |
|------|---------|
| Install dependencies | `uv sync` |
| Run application | `uv run python -m src.cli.main` |
| Run tests | `uv run pytest` |
| Run tests with coverage | `uv run pytest --cov=src --cov-report=html` |
| Format code | `uv run black src/ tests/` |
| Type check | `uv run mypy src/` |
| Add dependency | `uv add package-name` |
| View coverage | `open htmlcov/index.html` |
| Git status | `git status` |
| Commit changes | `git add . && git commit -m "message"` |

---

**Happy coding! 🚀**

For questions or issues, refer to the specification documents or run `/sp.clarify` with Claude Code.
