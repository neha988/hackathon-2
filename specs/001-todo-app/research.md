# Technology Research: Todo Console Application

**Feature**: 001-todo-app
**Phase**: 0 (Outline & Research)
**Date**: 2025-12-10

## Purpose

Document technology choices, rationale, and alternatives considered for the Todo Console Application implementation.

## Key Technology Decisions

### 1. CLI Framework: Click

**Decision**: Use Click for command-line interface framework

**Rationale**:
- **Industry Standard**: Click is the most popular Python CLI framework (used by Flask, pip, AWS CLI)
- **Automatic Help**: Generates --help documentation automatically from decorators
- **Composability**: Supports command groups, subcommands, and nested commands
- **Type Safety**: Integrates well with type hints and provides parameter validation
- **Testing**: Excellent support for CLI testing via CliRunner
- **Documentation**: Extensive documentation and community support

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| argparse (stdlib) | Built-in, no dependencies | Verbose, manual help text | Requires more boilerplate code |
| Typer | Type-hint based, modern | Newer, smaller ecosystem | Click is more mature and widely adopted |
| docopt | Declarative syntax | Limited validation | Less flexible for complex CLIs |

**References**:
- https://click.palletsprojects.com/
- https://github.com/pallets/click

---

### 2. Output Formatting: Rich

**Decision**: Use Rich for formatted console output

**Rationale**:
- **Professional Tables**: Beautiful table rendering with borders, colors, alignment
- **Color Support**: Cross-platform color support with fallback for non-color terminals
- **Progress Indicators**: Built-in progress bars and spinners (useful for future features)
- **Markdown Rendering**: Can render markdown in console (useful for help text)
- **Theming**: Customizable color schemes for priority color-coding
- **Active Development**: Well-maintained, modern library

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| tabulate | Simple, lightweight | No colors, basic formatting | Insufficient for priority color-coding |
| colorama | Good color support | No table formatting | Requires manual table layout |
| prettytable | Table formatting | Outdated, limited styling | Rich provides superior output |

**References**:
- https://rich.readthedocs.io/
- https://github.com/Textualize/rich

---

### 3. Data Validation: Pydantic

**Decision**: Use Pydantic V2 for data models and validation

**Rationale**:
- **Type Safety**: Enforces type hints at runtime with automatic validation
- **Rich Validation**: Built-in validators for strings, enums, dates, constraints
- **Serialization**: Easy conversion to/from dict, JSON (useful for future persistence)
- **Performance**: V2 uses Rust core, extremely fast
- **Error Messages**: Clear, actionable validation error messages
- **Documentation**: Automatic schema generation from models

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| dataclasses (stdlib) | Built-in, simple | No validation, manual checks | Insufficient validation for constitution requirements |
| attrs | Good validation | Less popular than Pydantic | Pydantic has better ecosystem |
| marshmallow | Serialization focus | Verbose schema definitions | Pydantic is more Pythonic |

**References**:
- https://docs.pydantic.dev/latest/
- https://github.com/pydantic/pydantic

---

### 4. Date Parsing: python-dateutil

**Decision**: Use python-dateutil for natural language date parsing

**Rationale**:
- **Natural Language**: Parses "tomorrow", "next Monday", "in 2 hours" etc.
- **Robust Parsing**: Handles various date formats automatically
- **Timezone Support**: Comprehensive timezone handling (for future features)
- **Battle-Tested**: Mature library, widely used (pytest, pandas, etc.)
- **ISO Format**: Excellent support for ISO 8601 format validation

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| datetime (stdlib) | Built-in | Only handles ISO format | No natural language support (FR-030 requires it) |
| arrow | Modern API | Less widely adopted | python-dateutil more mature |
| pendulum | Nice API | Heavier dependency | Overkill for our needs |

**References**:
- https://dateutil.readthedocs.io/
- https://github.com/dateutil/dateutil

---

### 5. Testing: pytest + pytest-cov + freezegun

**Decision**: Use pytest as testing framework with coverage and time mocking

**Rationale**:
- **pytest**: Industry standard, powerful fixtures, excellent assertions
- **pytest-cov**: Integrated coverage reporting (constitution requires 80%)
- **freezegun**: Mock datetime.now() for deterministic reminder tests
- **Fixtures**: Reusable test data setup
- **Parametrization**: Test multiple scenarios with @pytest.mark.parametrize
- **Plugin Ecosystem**: Rich plugins for all testing needs

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| unittest (stdlib) | Built-in | Verbose, limited features | pytest is more powerful |
| nose2 | Similar to pytest | Less actively maintained | pytest is standard |
| coverage.py (alone) | Good coverage tool | Requires separate test runner | pytest-cov integrates better |

**References**:
- https://docs.pytest.org/
- https://pytest-cov.readthedocs.io/
- https://github.com/spulec/freezegun

---

### 6. Package Management: UV

**Decision**: Use UV for dependency management and project structure

**Rationale**:
- **Hackathon Requirement**: Explicitly required by Phase I specification
- **Performance**: 10-100x faster than pip for dependency resolution
- **Modern**: Latest tool from Astral (makers of Ruff)
- **Lock Files**: Automatic lock file generation for reproducible builds
- **Virtual Environments**: Automatic venv management
- **PEP 621**: Uses modern pyproject.toml standard

**Alternatives Considered**:
N/A - UV is a mandatory requirement for Phase I

**References**:
- https://docs.astral.sh/uv/
- https://github.com/astral-sh/uv

---

### 7. Code Formatting: Black

**Decision**: Use Black for automatic code formatting

**Rationale**:
- **Constitution Requirement**: PEP 8 compliance required
- **Deterministic**: No configuration needed, "opinionated" formatter
- **Industry Standard**: Most popular Python formatter
- **Integration**: Works with UV, pytest, all major editors
- **Time Saving**: Eliminates formatting discussions

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| autopep8 | PEP 8 focused | Less comprehensive | Black is more thorough |
| yapf | Configurable | Requires configuration | Black's opinionated approach is better |
| Manual formatting | No dependencies | Error-prone, time-consuming | Not practical for spec-driven development |

**References**:
- https://black.readthedocs.io/
- https://github.com/psf/black

---

### 8. Storage: In-Memory Dict with threading.Lock

**Decision**: Use Python dict with auto-increment IDs and threading.Lock for thread safety

**Rationale**:
- **Simplicity**: No external database dependencies (Phase I requirement)
- **Performance**: O(1) lookup by ID, fast iteration
- **Thread Safety**: threading.Lock prevents race conditions
- **Auto-Increment IDs**: Simple counter for unique IDs
- **Scalability**: Can handle 10,000 tasks easily (constitution requirement)

**Alternatives Considered**:
| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| SQLite in-memory | SQL capabilities | Overkill for in-memory requirement | Phase I explicitly prohibits databases |
| shelve (stdlib) | Persistent dict | File-based, not in-memory | Violates in-memory requirement |
| list-based storage | Simple | O(n) lookup by ID | Poor performance for 10,000 tasks |

**Implementation Approach**:
```python
class InMemoryTaskStore:
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def add(self, task: Task) -> int:
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            self._tasks[task_id] = task
            return task_id
```

---

## Dependencies Summary

### Production Dependencies

```toml
[project]
dependencies = [
    "click>=8.1.7",          # CLI framework
    "rich>=13.7.0",          # Console output formatting
    "pydantic>=2.5.0",       # Data validation
    "python-dateutil>=2.8.2" # Date parsing
]
```

### Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",         # Testing framework
    "pytest-cov>=4.1.0",     # Coverage reporting
    "freezegun>=1.4.0",      # Time mocking for tests
    "black>=23.12.0",        # Code formatting
    "mypy>=1.8.0",           # Static type checking
]
```

---

## Architecture Patterns

### Pattern 1: Service Layer Pattern

**Decision**: Separate business logic into service classes

**Rationale**:
- **Testability**: Services can be unit tested independently of CLI
- **Reusability**: Services can be used by future interfaces (web, API)
- **Single Responsibility**: Each service focuses on one domain
- **Constitution Alignment**: Clean separation of concerns (Principle III)

**Services**:
- `TaskService`: CRUD operations, search, filter, sort
- `ReminderService`: Due date checking and console notifications
- `RecurrenceService`: Automatic recurring task generation

---

### Pattern 2: Repository Pattern (Simplified)

**Decision**: Use InMemoryTaskStore abstraction over raw dict

**Rationale**:
- **Future-Proofing**: Easy to swap storage backend in Phase II
- **Testing**: Can mock storage layer for service tests
- **Encapsulation**: Storage implementation hidden from services
- **Thread Safety**: Centralized locking logic

---

### Pattern 3: Command Pattern (Click)

**Decision**: Each CLI command is a separate module

**Rationale**:
- **Separation**: Each command is independently testable
- **Maintainability**: Easy to add new commands without touching existing code
- **Click Integration**: Natural fit for Click's command group pattern

---

## Risk Mitigation

### Risk 1: Performance with 10,000 Tasks

**Mitigation**:
- Use dict-based storage for O(1) lookups
- Implement efficient filtering with generator expressions
- Benchmark search/filter/sort operations during testing
- Profile code with cProfile if performance issues arise

### Risk 2: Thread Safety for Concurrent Operations

**Mitigation**:
- Use threading.Lock for all storage operations
- Write concurrency tests (test_concurrency.py)
- Document thread-safety guarantees in code

### Risk 3: Date Parsing Ambiguity

**Mitigation**:
- python-dateutil handles most cases
- Provide clear error messages for unparseable dates
- Support both ISO and natural language (FR-030)
- Test edge cases extensively

---

## Development Workflow

1. **Setup**: `uv init`, configure pyproject.toml
2. **Install**: `uv sync` (installs all dependencies)
3. **Run**: `uv run python -m src.cli.main [command]`
4. **Test**: `uv run pytest --cov=src --cov-report=html`
5. **Format**: `uv run black src/ tests/`
6. **Type Check**: `uv run mypy src/`

---

## Conclusion

All technology choices align with:
- ✅ Phase I hackathon requirements (Python 3.13+, UV, in-memory storage)
- ✅ Constitution principles (clean architecture, testing, documentation)
- ✅ Functional requirements (40 FRs from spec)
- ✅ Success criteria (performance, usability, reliability)

Ready to proceed to Phase 1 (Design & Contracts).
