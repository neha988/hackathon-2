<!--
Sync Impact Report:
- Version Change: Initial → 1.0.0
- New Constitution Creation for Todo Console App Phase I
- Feature Scope: Basic + Intermediate + Advanced levels
- Templates Status: ✅ Initial constitution created
- Follow-up: Validate plan/spec/tasks templates align with principles
-->

# Todo Console App - Phase I Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)

**Every feature MUST be specified before implementation.**

- All features require a complete specification in `specs/` directory before coding
- Use Claude Code + Spec-Kit Plus for all development workflows
- Specification files must define: user stories, acceptance criteria, data structures, and edge cases
- Implementation MUST strictly follow specifications - no code written manually
- Refine specifications iteratively until Claude Code generates correct output
- Constitution changes require versioned documentation and rationale

**Rationale**: Spec-driven development ensures clear requirements, AI-native workflows, and reduces implementation ambiguity. This is a hackathon requirement and core project methodology.

### II. Feature Completeness - Three-Tier Architecture

**Phase I implements ALL feature levels: Basic, Intermediate, and Advanced.**

**Basic Level (Core Essentials) - REQUIRED:**
1. Add Task - Create new todo items with title and description
2. Delete Task - Remove tasks from list by ID
3. Update Task - Modify existing task details (title, description)
4. View Task List - Display all tasks with status indicators
5. Mark as Complete - Toggle task completion status

**Intermediate Level (Organization & Usability) - REQUIRED:**
1. Priorities - Assign priority levels (high, medium, low) to tasks
2. Tags/Categories - Label tasks with categories (work, home, personal, etc.)
3. Search & Filter - Search by keyword; filter by status, priority, category, or date
4. Sort Tasks - Reorder by due date, priority, creation date, or alphabetically

**Advanced Level (Intelligent Features) - REQUIRED:**
1. Recurring Tasks - Auto-generate recurring tasks (daily, weekly, monthly patterns)
2. Due Dates & Reminders - Set deadlines with date/time; console-based reminder notifications

**Rationale**: Implementing all three levels in Phase I demonstrates full capability, maximizes hackathon points, and creates reusable patterns for later phases. Advanced features showcase technical depth.

### III. Clean Python Architecture & Best Practices

**Code MUST follow Python 3.13+ standards and clean architecture patterns.**

- Use UV for dependency management and project structure
- Implement proper separation of concerns:
  - `models/` - Data classes (Task, Priority, Category, Recurrence)
  - `services/` - Business logic (TaskService, ReminderService)
  - `storage/` - In-memory data management with thread safety
  - `cli/` - Command-line interface handlers
  - `utils/` - Helper functions (validators, formatters, date handlers)
- Type hints REQUIRED for all functions and class methods
- Docstrings REQUIRED for all public functions and classes (Google style)
- Follow PEP 8 style guidelines strictly
- Use dataclasses or Pydantic models for data structures
- Error handling: explicit exceptions, never silent failures

**Rationale**: Clean architecture ensures maintainability, testability, and professional code quality. Type hints and documentation enable AI-assisted development and human understanding.

### IV. In-Memory Data Integrity & Thread Safety

**Data persistence MUST be reliable within session boundaries.**

- Use Python collections (dict, list, set) with proper indexing
- Implement unique ID generation (UUID or auto-increment)
- Ensure data consistency for all CRUD operations
- Handle concurrent access safely (if applicable)
- Implement data validation before storage:
  - Title: 1-200 characters, non-empty
  - Description: max 1000 characters
  - Dates: valid ISO format, future dates for due dates
  - Priorities: enum validation (HIGH, MEDIUM, LOW)
  - Categories: alphanumeric strings, max 50 chars
- Graceful degradation on invalid input with clear error messages

**Rationale**: In-memory storage requires strict validation since data is volatile. Thread safety prevents race conditions. Clear constraints prevent corrupt state.

### V. User Experience - Intuitive CLI Design

**CLI MUST be user-friendly, consistent, and accessible.**

- Use argparse or Click for command-line argument parsing
- Implement clear command structure:
  - `add` - Add new task
  - `list` - View tasks (with filters)
  - `update` - Modify task
  - `delete` - Remove task
  - `complete` - Toggle completion
  - `search` - Search tasks
  - `sort` - Display sorted tasks
- Rich output formatting:
  - Use tables (rich library or tabulate) for list views
  - Color-coded priorities and status indicators
  - Clear success/error messages
  - Progress indicators for reminders
- Interactive mode support for complex operations
- Help text for all commands with examples
- Keyboard interrupt (Ctrl+C) handling gracefully

**Rationale**: Professional CLI experience demonstrates polish and usability. Rich formatting improves readability and user satisfaction.

### VI. Testing & Validation (NON-NEGOTIABLE)

**Comprehensive testing REQUIRED before Phase I submission.**

- Unit tests for all business logic functions (pytest)
- Test coverage minimum: 80% for core features
- Test categories:
  - **Unit Tests**: Task CRUD, priority assignment, category tagging, search, filter, sort
  - **Integration Tests**: End-to-end command execution, data persistence within session
  - **Edge Cases**: Empty inputs, invalid dates, duplicate IDs, boundary values
  - **Recurring Logic Tests**: Pattern generation (daily, weekly, monthly)
  - **Reminder Tests**: Due date calculations, notification triggers
- Use pytest fixtures for test data setup
- Mock time-dependent functions (datetime.now) for deterministic tests
- Automated test execution in CI/CD (if applicable)

**Rationale**: Testing ensures reliability and catches regressions. High coverage demonstrates code quality and professionalism for hackathon evaluation.

### VII. Documentation & Deliverables

**Complete documentation REQUIRED for submission.**

**Required Files:**
- `README.md` - Project overview, setup instructions, usage examples, feature list
- `CLAUDE.md` - Claude Code instructions for development workflows
- `specs/` - All specification files (constitution, feature specs)
- `/src` - Python source code with proper structure
- `requirements.txt` or `pyproject.toml` - Dependency declarations
- `tests/` - All test files with clear naming

**README.md MUST include:**
- Feature list (Basic, Intermediate, Advanced) with checkboxes
- Installation steps (UV setup, Python 3.13+, dependencies)
- Usage examples for every command
- Screenshots or demo video link
- WSL 2 setup instructions for Windows users
- Project structure diagram
- License information

**Rationale**: Documentation ensures project is understandable, reproducible, and meets hackathon submission requirements.

## Technology Stack Constraints

**Mandatory Technologies:**
- Python 3.13+
- UV (dependency management)
- Claude Code (AI-assisted development)
- Spec-Kit Plus (specification management)

**Recommended Libraries:**
- `rich` or `tabulate` - Table formatting and colored output
- `click` or `argparse` - CLI argument parsing
- `python-dateutil` - Date parsing and manipulation
- `pydantic` - Data validation and type safety
- `pytest` - Testing framework
- `pytest-cov` - Code coverage reporting

**Prohibited:**
- External databases (PostgreSQL, SQLite) - Phase I is in-memory only
- Web frameworks (FastAPI, Flask) - Phase I is console-only
- Third-party AI APIs (OpenAI, Anthropic) - Phase I has no AI chatbot

## Development Workflow

**Standard Development Cycle:**

1. **Specification Phase**:
   - Write detailed spec in `specs/<feature-name>/spec.md`
   - Define user stories, acceptance criteria, data models
   - Review and refine spec with Claude Code

2. **Planning Phase**:
   - Create architectural plan in `specs/<feature-name>/plan.md`
   - Break down into implementation tasks
   - Identify dependencies and constraints

3. **Implementation Phase**:
   - Use Claude Code to generate code from specifications
   - Iterative refinement: spec → code → test → refine
   - Never write code manually - refine spec instead
   - Commit frequently with clear messages

4. **Testing Phase**:
   - Write tests for all features
   - Achieve minimum 80% coverage
   - Validate edge cases and error handling

5. **Documentation Phase**:
   - Update README with new features
   - Add usage examples
   - Create demo video (max 90 seconds for submission)

## Quality Standards

**Code Quality Gates:**
- ✅ All tests passing (pytest)
- ✅ Type hints on all functions
- ✅ Docstrings on all public APIs
- ✅ PEP 8 compliance (use black formatter)
- ✅ No hardcoded values (use constants/config)
- ✅ Error handling on all user inputs
- ✅ Logging for debugging (Python logging module)

**Feature Completeness Checklist:**
- ✅ All 5 Basic features implemented and tested
- ✅ All 4 Intermediate features implemented and tested
- ✅ All 2 Advanced features implemented and tested
- ✅ Help documentation for all commands
- ✅ Error messages are clear and actionable

**Submission Readiness:**
- ✅ Public GitHub repository created
- ✅ README.md complete with setup instructions
- ✅ Demo video recorded (under 90 seconds)
- ✅ All specs in `specs/` directory
- ✅ All source code in `/src` directory
- ✅ Test suite executable with single command

## Governance

**Constitutional Authority:**
- This constitution supersedes all other development practices
- All code reviews MUST verify compliance with these principles
- Amendments require:
  1. Documented rationale for change
  2. Version increment (semantic versioning)
  3. Update to dependent templates and specs
  4. Validation that existing code remains compliant

**Amendment Process:**
- MAJOR version: Breaking changes to core principles (e.g., removing spec-driven requirement)
- MINOR version: New principles added or substantial expansions
- PATCH version: Clarifications, typo fixes, non-semantic changes

**Compliance Verification:**
- Pre-submission checklist MUST validate all Quality Standards
- Spec-driven workflow MUST be demonstrable in commit history
- Test coverage MUST be measurable and reportable

**Runtime Development Guidance:**
- See `/CLAUDE.md` for Claude Code-specific instructions
- See `specs/` for feature-specific requirements
- See `README.md` for user-facing documentation

---

**Version**: 1.0.0 | **Ratified**: 2025-12-10 | **Last Amended**: 2025-12-10
