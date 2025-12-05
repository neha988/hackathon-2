<!-- Sync Impact Report:
Version change: None → 1.0.0
Modified principles: None
Added sections: Project Overview, Technology Stack and Standards, Development Practices, Governance
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md: ⚠ pending - Constitution Check section needs to be updated with specific principles.
- .specify/templates/spec-template.md: ✅ updated (no direct changes needed, but will be guided by constitution)
- .specify/templates/tasks-template.md: ✅ updated (no direct changes needed, but will be guided by constitution)
- .specify/templates/commands/*.md: ✅ updated (no command files found, so no updates needed)
- README.md: ⚠ pending - README.md does not exist, so cannot be updated.
Follow-up TODOs:
- Update the "Constitution Check" section in .specify/templates/plan-template.md to reflect the new principles.
- Create README.md and ensure it aligns with the constitution's principles for documentation.
-->
# Todo Console Application Constitution

## Core Principles

### Simplicity First
Keep code simple and readable.

### User-Centric
Prioritize user experience in CLI interactions.

### Reliability
Handle errors gracefully, never crash.

### Maintainability
Write self-documenting code with clear structure.

### Extensibility
Design for future feature additions.


## Technology Stack and Standards

### Technology Stack
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Data Storage**: JSON file (tasks.json)
- **Standard Library**: datetime, json, os
- **External Dependencies**: No external dependencies for Phase I

### Code Standards
- **File Structure**:
  - `/src`
    - `main.py`          # Entry point, main menu
    - `tasks.py`         # Task data structure and operations
    - `persistence.py`   # File I/O operations
    - `utils.py`         # Helper functions
- **Naming Conventions**:
  - Functions: `snake_case` (e.g., `add_task`, `view_all_tasks`)
  - Variables: `snake_case` (e.g., `task_list`, `user_input`)
  - Constants: `UPPER_SNAKE_CASE` (e.g., `TASKS_FILE`, `DEFAULT_PRIORITY`)
  - Classes: `PascalCase` (if needed)
- **Function Guidelines**:
  - Each function does ONE thing
  - Maximum 50 lines per function
  - Clear function names that describe action
  - Include docstrings for all functions
  - Return values instead of printing (separation of concerns)

### Data Structure Standards
- **Task Dictionary**:
  ```python
  {
      "id": int,              # Unique identifier
      "title": str,           # Required, non-empty
      "description": str,     # Optional, can be empty
      "status": bool,         # False = incomplete, True = complete
      "priority": str,        # 'H', 'M', or 'L'
      "category": str,        # 'Work', 'Personal', etc.
      "due_date": str|None,   # 'YYYY-MM-DD' or None
      "recurrence": str       # 'none', 'daily', 'weekly', 'monthly'
  }
  ```

### Error Handling Philosophy
- Never crash the application
- Always validate user input
- Provide clear, helpful error messages
- Use try-except blocks for file operations
- Default to safe values when possible

### Input Validation Rules
- Validate before processing
- Trim whitespace from inputs
- Case-insensitive where appropriate
- Provide default values
- Clear error messages with retry option

### File Operations
- Auto-save after each modification
- Handle missing files gracefully
- UTF-8 encoding always
- Pretty-print JSON (indented)
- Backup before overwriting (optional)

## Development Practices

### User Experience Guidelines
- Clear prompts with examples
- Consistent menu formatting
- Confirmation messages after actions
- Visual separators between sections
- Show current values when updating
- Allow "press Enter to skip/keep" patterns

### Testing Approach
- Test each feature independently
- Test error cases explicitly
- Test with empty task list
- Test with large task lists (100+ tasks)
- Test edge cases (invalid dates, special characters)

### Code Documentation
- Docstrings for all public functions
- Inline comments for complex logic only
- README with setup and usage instructions
- CLAUDE.md with AI development notes

### Version Control Practices
- Meaningful commit messages
- One feature per commit
- Keep specs in specs_history/ folder
- Update README with new features

### Prohibited Practices
- No global variables (except constants)
- No hardcoded values (use constants)
- No print statements in business logic functions
- No nested functions beyond 3 levels
- No functions over 50 lines

### AI Development Notes
- Each spec should be implemented independently
- Refine specs if generated code doesn't meet requirements
- Test immediately after implementation
- Document any deviations from spec in CLAUDE.md

## Governance
The constitution serves as the foundational rulebook for AI-assisted development, ensuring Claude Code generates consistent, high-quality code that follows established patterns and principles.
- All PRs/reviews must verify compliance.
- Complexity must be justified.
- Use CLAUDE.md for runtime development guidance.

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
