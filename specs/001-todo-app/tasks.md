# Tasks: Todo Console Application

**Input**: Design documents from `/specs/001-todo-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-commands.md

**Tests**: Included - Constitution requires 80% minimum test coverage

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (per plan.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize UV project with Python 3.13+ in repository root
- [x] T002 Configure pyproject.toml with dependencies (click, rich, pydantic, python-dateutil, pytest, pytest-cov, freezegun, black, mypy)
- [x] T003 Create project directory structure (src/, tests/, src/models/, src/services/, src/storage/, src/cli/, src/utils/, tests/unit/, tests/integration/, tests/edge_cases/)
- [x] T004 [P] Create __init__.py files in all Python packages
- [x] T005 [P] Configure .gitignore for Python project (.venv/, __pycache__/, *.pyc, .pytest_cache/, htmlcov/, .coverage)
- [x] T006 [P] Configure Black formatter in pyproject.toml
- [x] T007 [P] Configure mypy type checker in pyproject.toml

**Checkpoint**: Project structure initialized, ready for foundational components

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 [P] Create Priority enum in src/models/priority.py
- [ ] T009 [P] Create RecurrencePattern enum in src/models/recurrence.py
- [ ] T010 Create base Task model skeleton in src/models/task.py (basic fields only: id, title, description, completed, created_at, updated_at)
- [ ] T011 Create InMemoryTaskStore class in src/storage/task_store.py with thread safety (threading.Lock)
- [ ] T012 Implement basic storage methods (add, get, get_all, update, delete) in src/storage/task_store.py
- [ ] T013 [P] Create Click CLI group in src/cli/main.py with entry point
- [ ] T014 [P] Create pytest conftest.py with fixtures (sample tasks, task store, CLI runner)
- [ ] T015 [P] Create base validators in src/utils/validators.py (validate_title, validate_description)
- [ ] T016 [P] Create Rich table formatter in src/utils/formatters.py (format_task_table function)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, update, delete, and mark tasks as complete via CLI

**Independent Test**: User can add a task, view it in list, update title, mark complete, and delete it without any other features

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T017 [P] [US1] Create unit test for Task model validation in tests/unit/test_models.py
- [ ] T018 [P] [US1] Create unit test for TaskService CRUD operations in tests/unit/test_task_service.py
- [ ] T019 [P] [US1] Create unit test for InMemoryTaskStore in tests/unit/test_task_store.py
- [ ] T020 [P] [US1] Create integration test for add command in tests/integration/test_cli_add.py
- [ ] T021 [P] [US1] Create integration test for list command in tests/integration/test_cli_list.py
- [ ] T022 [P] [US1] Create integration test for update command in tests/integration/test_cli_update.py
- [ ] T023 [P] [US1] Create integration test for delete command in tests/integration/test_cli_delete.py
- [ ] T024 [P] [US1] Create integration test for complete command in tests/integration/test_cli_complete.py

### Implementation for User Story 1

- [ ] T025 [US1] Complete Task model in src/models/task.py with Pydantic validation (title, description, completed fields)
- [ ] T026 [US1] Create TaskService class in src/services/task_service.py with CRUD methods (create_task, get_task, get_all_tasks, update_task, delete_task, toggle_completion)
- [ ] T027 [US1] Implement add command in src/cli/add.py (title argument, --description option)
- [ ] T028 [US1] Implement list command in src/cli/list.py (display all tasks in Rich table)
- [ ] T029 [US1] Implement update command in src/cli/update.py (task_id argument, --title and --description options)
- [ ] T030 [US1] Implement delete command in src/cli/delete.py (task_id argument, confirmation prompt)
- [ ] T031 [US1] Implement complete command in src/cli/complete.py (task_id argument, toggle completion status)
- [ ] T032 [US1] Register all commands in src/cli/main.py CLI group
- [ ] T033 [US1] Add error handling for task not found in all CLI commands
- [ ] T034 [US1] Add success messages with task details in all CLI commands

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Run all US1 tests and validate CRUD operations work.

---

## Phase 4: User Story 2 - Task Organization with Priorities and Tags (Priority: P2)

**Goal**: Enable users to assign priority levels and category tags to organize tasks

**Independent Test**: User can create tasks with HIGH/MEDIUM/LOW priorities and multiple category tags, then view them with color-coded priorities

### Tests for User Story 2

- [ ] T035 [P] [US2] Create unit test for Priority enum validation in tests/unit/test_models.py
- [ ] T036 [P] [US2] Create unit test for category validation in tests/unit/test_validators.py
- [ ] T037 [P] [US2] Create integration test for priority assignment in tests/integration/test_cli_add.py
- [ ] T038 [P] [US2] Create integration test for category tags in tests/integration/test_cli_add.py

### Implementation for User Story 2

- [ ] T039 [P] [US2] Add priority field to Task model in src/models/task.py (with Priority enum, default MEDIUM)
- [ ] T040 [P] [US2] Add categories field to Task model in src/models/task.py (List[str] with validation)
- [ ] T041 [US2] Add category validator in src/utils/validators.py (validate_category: alphanumeric, max 50 chars)
- [ ] T042 [US2] Update TaskService in src/services/task_service.py to handle priority and categories
- [ ] T043 [US2] Add priority color mapping in src/utils/formatters.py (HIGH=red, MEDIUM=yellow, LOW=green)
- [ ] T044 [US2] Update format_task_table in src/utils/formatters.py to display color-coded priorities
- [ ] T045 [US2] Update add command in src/cli/add.py to accept --priority and --category options
- [ ] T046 [US2] Update update command in src/cli/update.py to support --priority, --add-category, --remove-category options
- [ ] T047 [US2] Update list command in src/cli/list.py to display priorities and categories with colors

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Tasks can be created and organized by priority/category.

---

## Phase 5: User Story 3 - Advanced Search, Filter, and Sort (Priority: P2)

**Goal**: Enable users to search tasks by keyword, filter by attributes, and sort by various criteria

**Independent Test**: User can search for "meeting", filter by HIGH priority + pending status, and sort by due date

### Tests for User Story 3

- [ ] T048 [P] [US3] Create unit test for search functionality in tests/unit/test_task_service.py
- [ ] T049 [P] [US3] Create unit test for filter operations in tests/unit/test_task_service.py
- [ ] T050 [P] [US3] Create unit test for sort operations in tests/unit/test_task_service.py
- [ ] T051 [P] [US3] Create integration test for search command in tests/integration/test_cli_search.py
- [ ] T052 [P] [US3] Create integration test for list filters in tests/integration/test_cli_list.py

### Implementation for User Story 3

- [ ] T053 [P] [US3] Implement search_tasks method in src/services/task_service.py (case-insensitive keyword search in title/description)
- [ ] T054 [P] [US3] Implement filter_tasks method in src/services/task_service.py (filter by status, priority, category with combination support)
- [ ] T055 [P] [US3] Implement sort_tasks method in src/services/task_service.py (sort by due_date, priority, created, title)
- [ ] T056 [US3] Create search command in src/cli/search.py (keyword argument, --sort-by option)
- [ ] T057 [US3] Create sort command in src/cli/sort.py (sort_by argument, --reverse flag)
- [ ] T058 [US3] Update list command in src/cli/list.py with filter options (--status, --priority, --category, --sort-by)
- [ ] T059 [US3] Add "No tasks match filters" message in list/search commands
- [ ] T060 [US3] Register search and sort commands in src/cli/main.py

**Checkpoint**: All search, filter, and sort operations working. User Stories 1, 2, and 3 all independently functional.

---

## Phase 6: User Story 4 - Recurring Tasks (Priority: P3)

**Goal**: Enable automatic generation of recurring tasks (daily, weekly, monthly) when current instance is marked complete

**Independent Test**: User creates weekly recurring task, marks it complete, and new instance is auto-generated for next week

### Tests for User Story 4

- [ ] T061 [P] [US4] Create unit test for RecurrencePattern enum in tests/unit/test_models.py
- [ ] T062 [P] [US4] Create unit test for RecurrenceService in tests/unit/test_recurrence_service.py
- [ ] T063 [P] [US4] Create integration test for recurring task creation in tests/integration/test_recurring.py
- [ ] T064 [P] [US4] Create integration test for recurrence trigger on completion in tests/integration/test_recurring.py

### Implementation for User Story 4

- [ ] T065 [P] [US4] Add recurrence_pattern field to Task model in src/models/task.py (Optional[RecurrencePattern])
- [ ] T066 [US4] Create RecurrenceService class in src/services/recurrence_service.py
- [ ] T067 [US4] Implement calculate_next_due_date method in src/services/recurrence_service.py (handle DAILY, WEEKLY, MONTHLY)
- [ ] T068 [US4] Implement generate_next_instance method in src/services/recurrence_service.py (create new task with updated due_date)
- [ ] T069 [US4] Update TaskService.toggle_completion in src/services/task_service.py to check for recurrence and generate next instance
- [ ] T070 [US4] Add --recurring option to add command in src/cli/add.py (DAILY/WEEKLY/MONTHLY choices)
- [ ] T071 [US4] Add --recurring and --no-recurring options to update command in src/cli/update.py
- [ ] T072 [US4] Update complete command in src/cli/complete.py to display "Next instance created" message when recurrence triggered
- [ ] T073 [US4] Ensure delete command does NOT trigger recurrence (FR-024 compliance)

**Checkpoint**: Recurring tasks working. New instances auto-generate on completion. User Stories 1-4 all functional.

---

## Phase 7: User Story 5 - Due Dates and Reminders (Priority: P3)

**Goal**: Enable due dates with natural language parsing and console-based reminders for approaching deadlines

**Independent Test**: User sets due date "tomorrow at 2pm", system displays reminder 1 hour before, and task shows as "due today" in list

### Tests for User Story 5

- [ ] T074 [P] [US5] Create unit test for date parsing in tests/unit/test_date_parser.py (ISO format and natural language)
- [ ] T075 [P] [US5] Create unit test for ReminderService in tests/unit/test_reminder_service.py
- [ ] T076 [P] [US5] Create integration test for due date assignment in tests/integration/test_cli_add.py
- [ ] T077 [P] [US5] Create integration test for reminder display in tests/integration/test_reminders.py (using freezegun)

### Implementation for User Story 5

- [ ] T078 [P] [US5] Add due_date field to Task model in src/models/task.py (Optional[datetime] with future validation)
- [ ] T079 [P] [US5] Add derived properties to Task model in src/models/task.py (is_overdue, is_due_today, is_due_soon)
- [ ] T080 [US5] Create date_parser utility in src/utils/date_parser.py using python-dateutil (parse_date function supporting ISO and natural language)
- [ ] T081 [US5] Create ReminderService class in src/services/reminder_service.py
- [ ] T082 [US5] Implement check_reminders method in src/services/reminder_service.py (find tasks due within 1 hour)
- [ ] T083 [US5] Implement display_reminder method in src/services/reminder_service.py (format console reminder message)
- [ ] T084 [US5] Add --due option to add command in src/cli/add.py (accepts ISO or natural language)
- [ ] T085 [US5] Add --due option to update command in src/cli/update.py
- [ ] T086 [US5] Update format_task_table in src/utils/formatters.py to highlight overdue (red background), due today (yellow background)
- [ ] T087 [US5] Update list command in src/cli/list.py to sort overdue tasks first when sorting by due date
- [ ] T088 [US5] Add background reminder check in src/cli/main.py (optional: thread that checks every 60 seconds)

**Checkpoint**: All features complete. User Stories 1-5 all independently functional. Full MVP ready.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final touches, documentation, and quality validation

- [ ] T089 [P] Create README.md with installation instructions, usage examples, feature list, WSL 2 setup for Windows
- [ ] T090 [P] Create CLAUDE.md with Claude Code development instructions and spec-driven workflow
- [ ] T091 [P] Add comprehensive docstrings (Google style) to all public functions and classes
- [ ] T092 Run Black formatter on entire codebase (src/ and tests/)
- [ ] T093 Run mypy type checker and fix any type errors
- [ ] T094 Run pytest with coverage and validate 80% minimum coverage
- [ ] T095 [P] Create edge case tests in tests/edge_cases/test_boundaries.py (empty input, max length, boundary values)
- [ ] T096 [P] Create edge case tests in tests/edge_cases/test_invalid_input.py (invalid dates, priorities, categories)
- [ ] T097 [P] Create edge case tests in tests/edge_cases/test_concurrency.py (thread safety validation)
- [ ] T098 Add LICENSE file (choose appropriate open source license)
- [ ] T099 Create demo video script (max 90 seconds for hackathon submission)
- [ ] T100 Final validation: Run all tests, check coverage report, verify all commands work

**Checkpoint**: Project complete and ready for submission. All quality gates passed.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User Story 1 (P1): MVP - complete first
  - User Story 2 (P2): Can run in parallel with US3 after US1 completes (shares some CLI code)
  - User Story 3 (P2): Can run in parallel with US2 after US1 completes (extends TaskService)
  - User Story 4 (P3): Depends on US5 (needs due_date field for recurrence)
  - User Story 5 (P3): Can start after US1 completes
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1) - Basic CRUD**: No dependencies on other stories ✅ Start here
- **User Story 2 (P2) - Priorities/Tags**: Extends US1 Task model ⚠️ Needs US1 Task model
- **User Story 3 (P2) - Search/Filter/Sort**: Extends US1 TaskService ⚠️ Needs US1 TaskService
- **User Story 4 (P3) - Recurring**: Depends on US5 due_date field ⚠️ Needs US5 first
- **User Story 5 (P3) - Due Dates**: Extends US1 Task model ✅ Can start after US1

### Recommended Execution Order

1. **Phase 1: Setup** (T001-T007)
2. **Phase 2: Foundational** (T008-T016) ⚠️ CRITICAL BLOCKER
3. **Phase 3: User Story 1** (T017-T034) 🎯 MVP
4. **Phase 7: User Story 5** (T074-T088) - Do before US4 since US4 needs due_date
5. **Phase 4: User Story 2** (T035-T047) and **Phase 5: User Story 3** (T048-T060) in parallel
6. **Phase 6: User Story 4** (T061-T073) - After US5 completes
7. **Phase 8: Polish** (T089-T100)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before CLI commands
- Core CLI commands before integration
- Validate story independently before moving to next

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T004, T005, T006, T007 can run in parallel

**Foundational Phase (Phase 2)**:
- T008, T009 (enums) can run in parallel
- T014, T015, T016 (tests, validators, formatters) can run in parallel after T010-T013

**User Story 1 Tests**:
- T017, T018, T019, T020, T021, T022, T023, T024 can all run in parallel

**User Story 2 Implementation**:
- T039, T040 (model fields) can run in parallel
- T043 (color mapping) can run in parallel with T041, T042

**User Story 3 Implementation**:
- T053, T054, T055 (service methods) can run in parallel

**User Story 4 Tests**:
- T061, T062, T063, T064 can run in parallel

**User Story 5 Implementation**:
- T078, T079 (model changes) can run in parallel
- T080, T081 (utilities and services) can run in parallel

**Polish Phase**:
- T089, T090, T091, T095, T096, T097 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for Task model in tests/unit/test_models.py" [T017]
Task: "Unit test for TaskService in tests/unit/test_task_service.py" [T018]
Task: "Unit test for InMemoryTaskStore in tests/unit/test_task_store.py" [T019]
Task: "Integration test for add command in tests/integration/test_cli_add.py" [T020]
Task: "Integration test for list command in tests/integration/test_cli_list.py" [T021]
Task: "Integration test for update command in tests/integration/test_cli_update.py" [T022]
Task: "Integration test for delete command in tests/integration/test_cli_delete.py" [T023]
Task: "Integration test for complete command in tests/integration/test_cli_complete.py" [T024]

# After tests fail, implement core components (sequential due to dependencies):
Task: "Complete Task model with validation" [T025]
Task: "Create TaskService with CRUD methods" [T026]

# Then implement CLI commands (can run in parallel):
Task: "Implement add command in src/cli/add.py" [T027]
Task: "Implement list command in src/cli/list.py" [T028]
Task: "Implement update command in src/cli/update.py" [T029]
Task: "Implement delete command in src/cli/delete.py" [T030]
Task: "Implement complete command in src/cli/complete.py" [T031]
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T016) - CRITICAL
3. Complete Phase 3: User Story 1 (T017-T034)
4. **STOP and VALIDATE**: Run all US1 tests, verify CRUD operations work independently
5. Deploy/demo MVP

**Estimated MVP**: ~34 tasks to basic working todo app

### Incremental Delivery

1. Complete Setup + Foundational (T001-T016) → Foundation ready
2. Add User Story 1 (T017-T034) → Test independently → MVP ready! 🎯
3. Add User Story 5 (T074-T088) → Due dates working
4. Add User Stories 2 & 3 in parallel (T035-T060) → Organization features
5. Add User Story 4 (T061-T073) → Recurring tasks
6. Polish (T089-T100) → Production ready
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

1. **Developer A**: User Story 1 (T017-T034) - Priority 1
2. **Developer B**: User Story 5 (T074-T088) - Needed for US4
3. **Developer C**: Setup documentation (T089-T090) in parallel

Then:
4. **Developer A**: User Story 2 (T035-T047)
5. **Developer B**: User Story 3 (T048-T060)
6. **Developer C**: User Story 4 (T061-T073) - After US5 completes

Finally:
7. **All**: Polish tasks (T091-T100) together

---

## Task Count Summary

| Phase | Task Count | Parallelizable |
|-------|------------|----------------|
| Phase 1: Setup | 7 | 4 tasks (T004-T007) |
| Phase 2: Foundational | 9 | 6 tasks (T008-T009, T014-T016) |
| Phase 3: User Story 1 (P1) | 18 | 8 tests (T017-T024) |
| Phase 4: User Story 2 (P2) | 13 | 4 tests (T035-T038), 2 impl (T039-T040) |
| Phase 5: User Story 3 (P2) | 13 | 5 tests (T048-T052), 3 impl (T053-T055) |
| Phase 6: User Story 4 (P3) | 13 | 4 tests (T061-T064), 2 impl (T065-T066) |
| Phase 7: User Story 5 (P3) | 15 | 4 tests (T074-T077), 3 impl (T078-T080) |
| Phase 8: Polish | 12 | 7 tasks (T089-T091, T095-T097) |
| **TOTAL** | **100 tasks** | **45 parallelizable** |

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Write tests first, verify they fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitution requires 80% test coverage - extensive testing included
- All tasks include exact file paths for Claude Code implementation
- MVP = Phases 1, 2, 3 (34 tasks) = Basic working todo app
- Full feature set = All 100 tasks
