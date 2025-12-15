<!--
Sync Impact Report:
- Version Change: Initial → 1.0.0
- New Constitution Creation for Todo Console App Phase I
- Feature Scope: Basic + Intermediate + Advanced levels
- Templates Status: ✅ Initial constitution created
- Follow-up: Validate plan/spec/tasks templates align with principles
-->

# Todo App - Multi-Phase Constitution

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

---

## Phase II: Full-Stack Web Application Principles

### VIII. Monorepo Architecture (NON-NEGOTIABLE)

**Phase II MUST use a monorepo structure with clear separation between frontend and backend.**

- Root-level `frontend/` directory for Next.js 16+ application
- Root-level `backend/` directory for Python FastAPI application
- Phase I code remains in `src/` directory as reference (legacy)
- Shared specifications in `specs/` directory at root level
- Each subdirectory has its own `CLAUDE.md` with context-specific instructions

**Directory Structure:**
```
hacathon2/
├── .specify/                 # Spec-Kit configuration
├── specs/                    # Shared specifications
│   ├── phase-2/              # Phase II specifications
│   │   ├── architecture.md
│   │   ├── features/
│   │   ├── api/
│   │   ├── database/
│   │   └── ui/
├── frontend/                 # Next.js 16+ App Router
│   ├── CLAUDE.md
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── package.json
├── backend/                  # FastAPI Application
│   ├── CLAUDE.md
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── db.py
│   │   └── main.py
│   ├── pyproject.toml
│   └── requirements.txt
├── src/                      # Phase I legacy (console app)
├── docker-compose.yml
├── CLAUDE.md                 # Root-level instructions
└── README.md
```

**Rationale**: Monorepo enables Claude Code to see entire project context, make cross-cutting changes, and maintain consistency between frontend and backend while preserving Phase I work as reference.

### IX. RESTful API Design & Multi-User Architecture

**Backend MUST implement secure, multi-user RESTful API following OpenAPI standards.**

**API Endpoint Standards:**
- All endpoints under `/api/{user_id}/` namespace
- User isolation enforced at database query level
- JWT-based authentication using Better Auth
- Proper HTTP status codes (200, 201, 400, 401, 404, 500)
- Request/response validation using Pydantic models
- CORS configuration for frontend-backend communication

**Required Endpoints (Phase II - Basic Level):**
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/{user_id}/tasks` | List all user tasks | Yes |
| POST | `/api/{user_id}/tasks` | Create new task | Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get task details | Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | Yes |

**Security Requirements:**
- JWT tokens issued by Better Auth on frontend
- Backend verifies JWT signature using shared `BETTER_AUTH_SECRET`
- User ID in URL MUST match authenticated user in JWT payload
- Return 401 Unauthorized for missing/invalid tokens
- Return 403 Forbidden for mismatched user IDs
- Return 404 Not Found (not 403) for non-existent resources owned by other users

**Rationale**: Proper REST design ensures API is scalable, testable, and follows industry standards. User isolation prevents data leaks and security vulnerabilities.

### X. Database-Driven Persistence with SQLModel

**Phase II MUST use Neon Serverless PostgreSQL with SQLModel ORM for data persistence.**

**Database Schema Requirements:**

**users table** (managed by Better Auth):
- `id`: string (UUID, primary key)
- `email`: string (unique, not null)
- `name`: string
- `created_at`: timestamp
- `updated_at`: timestamp

**tasks table**:
- `id`: integer (auto-increment, primary key)
- `user_id`: string (foreign key → users.id, not null)
- `title`: string (1-200 chars, not null)
- `description`: text (max 1000 chars, nullable)
- `completed`: boolean (default false)
- `created_at`: timestamp (auto-generated)
- `updated_at`: timestamp (auto-updated)

**Indexes:**
- `tasks.user_id` (for efficient user filtering)
- `tasks.completed` (for status filtering)
- `tasks.created_at` (for sorting)

**Data Validation:**
- Title: 1-200 characters, non-empty, no leading/trailing whitespace
- Description: max 1000 characters, optional
- User ID: valid UUID format, exists in users table
- Completed: boolean only
- Timestamps: UTC timezone, ISO 8601 format

**Connection Management:**
- Use SQLModel engine with connection pooling
- Store `DATABASE_URL` in `.env` file (never in code)
- Handle connection failures gracefully with retries
- Implement proper session management (create/close)

**Rationale**: Neon Serverless PostgreSQL provides production-grade persistence with auto-scaling. SQLModel combines SQLAlchemy's power with Pydantic's validation for type-safe database operations.

### XI. Frontend Architecture with Next.js 16 App Router

**Frontend MUST use Next.js 16+ with App Router, TypeScript, and Tailwind CSS.**

**Architecture Requirements:**
- **Server Components by default** - use `'use client'` only when needed
- **Client Components** only for interactivity (forms, buttons, real-time updates)
- **API calls** through centralized client (`lib/api.ts`)
- **Authentication** handled by Better Auth with JWT storage
- **State management** using React Context or Zustand (minimal)
- **Styling** with Tailwind CSS utility classes (no inline styles)

**Directory Structure:**
```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx            # Root layout with auth provider
│   ├── page.tsx              # Home page
│   ├── tasks/                # Tasks pages
│   │   ├── page.tsx          # Task list
│   │   └── [id]/page.tsx     # Task detail/edit
│   ├── auth/                 # Auth pages
│   │   ├── signin/page.tsx
│   │   └── signup/page.tsx
├── components/               # Reusable UI components
│   ├── TaskList.tsx
│   ├── TaskCard.tsx
│   ├── TaskForm.tsx
│   └── ui/                   # shadcn/ui components
├── lib/                      # Utilities
│   ├── api.ts                # API client (fetch wrapper)
│   ├── auth.ts               # Better Auth configuration
│   └── utils.ts              # Helper functions
├── types/                    # TypeScript types
│   └── task.ts
└── public/                   # Static assets
```

**Component Standards:**
- TypeScript for all components (strict mode)
- Props typed with interfaces
- Error boundaries for async operations
- Loading states for all data fetching
- Accessible forms (ARIA labels, keyboard navigation)
- Responsive design (mobile-first approach)

**Rationale**: Next.js 16 App Router provides modern React architecture with server-side rendering, automatic code splitting, and excellent developer experience. TypeScript ensures type safety across frontend codebase.

### XII. Authentication & Authorization with Better Auth

**Phase II MUST implement secure user authentication using Better Auth with JWT tokens.**

**Authentication Flow:**
1. User signs up/signs in on Next.js frontend
2. Better Auth creates session and issues JWT token
3. Frontend stores JWT in secure HTTP-only cookies (or localStorage as fallback)
4. Frontend includes JWT in `Authorization: Bearer <token>` header for all API calls
5. Backend FastAPI middleware verifies JWT signature
6. Backend extracts user ID from JWT payload
7. Backend validates user ID matches `{user_id}` in request URL
8. Backend filters all database queries by authenticated user ID

**Shared Secret Configuration:**
- Both frontend and backend MUST use same `BETTER_AUTH_SECRET` environment variable
- Secret MUST be at least 32 characters (use crypto-random string)
- Secret stored in `.env` files (frontend and backend)
- `.env` files MUST be in `.gitignore` (never committed)

**Frontend Better Auth Setup:**
```typescript
// lib/auth.ts
import { createAuthClient } from "better-auth/client"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  plugins: [jwtPlugin()],
})
```

**Backend JWT Verification:**
```python
# app/middleware/auth.py
from fastapi import Depends, HTTPException, Header
import jwt
import os

SECRET = os.getenv("BETTER_AUTH_SECRET")

async def verify_jwt(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")

    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

**Security Requirements:**
- Token expiry: 7 days (refresh before expiration)
- HTTPS only in production (enforce secure cookies)
- CORS properly configured (allow frontend origin only)
- Rate limiting on auth endpoints (prevent brute force)
- Password hashing (Better Auth handles this automatically)

**Rationale**: Better Auth provides production-ready authentication with minimal setup. JWT tokens enable stateless authentication, allowing backend to scale horizontally without session storage.

### XIII. Cross-Stack Testing Strategy

**Phase II MUST implement comprehensive testing across frontend, backend, and integration layers.**

**Backend Testing (pytest):**
- **Unit Tests**: Models, services, utilities (80% coverage minimum)
- **API Tests**: All endpoints with FastAPI TestClient
- **Database Tests**: SQLModel queries with test database
- **Auth Tests**: JWT verification, user isolation
- **Edge Cases**: Invalid inputs, unauthorized access, race conditions

**Frontend Testing:**
- **Component Tests**: React Testing Library for UI components
- **Integration Tests**: API client mocking with MSW (Mock Service Worker)
- **E2E Tests**: Playwright for critical user flows (optional but recommended)
- **Type Checking**: `tsc --noEmit` as part of CI

**Integration Testing:**
- Test complete user flows: signup → create task → list tasks → delete task
- Mock external services (Neon DB uses test instance)
- Validate API contracts match frontend expectations

**Test Infrastructure:**
- Backend: `pytest`, `pytest-cov`, `pytest-asyncio`
- Frontend: Jest, React Testing Library, Playwright
- CI/CD: GitHub Actions running all tests on push
- Test database: Separate Neon branch or local PostgreSQL

**Rationale**: Multi-layer testing ensures reliability at component, API, and system levels. High coverage prevents regressions during rapid development.

### XIV. Environment Configuration & Secrets Management

**Phase II MUST use environment variables for all configuration and secrets.**

**Required Environment Variables:**

**Backend (.env):**
```bash
DATABASE_URL=postgresql://neondb_owner:npg_...@ep-flat-sky-ad666q3a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=your-32-char-secret-here
CORS_ORIGINS=http://localhost:3000,https://yourdomain.vercel.app
ENVIRONMENT=development  # development | production
```

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-32-char-secret-here
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Security Best Practices:**
- `.env` and `.env.local` MUST be in `.gitignore`
- Provide `.env.example` templates with placeholder values
- Document all required environment variables in README
- Use different secrets for development and production
- Never log or expose secrets in error messages

**Rationale**: Environment variables keep secrets out of code, enable different configurations per environment, and follow 12-factor app principles.

---

## Technology Stack Constraints

### Phase I: Console Application

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

### Phase II: Full-Stack Web Application

**Mandatory Technologies:**
- **Frontend**: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- **Backend**: Python 3.13+, FastAPI, SQLModel, UV
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT
- **Deployment**: Vercel (frontend), Railway/Render/Fly.io (backend)
- **Spec-Driven**: Claude Code + Spec-Kit Plus

**Required Libraries:**

**Backend:**
- `fastapi` - Web framework
- `sqlmodel` - ORM (combines SQLAlchemy + Pydantic)
- `uvicorn` - ASGI server
- `python-jose[cryptography]` - JWT handling
- `passlib[bcrypt]` - Password hashing (via Better Auth)
- `python-dotenv` - Environment variable loading
- `pytest`, `pytest-asyncio`, `httpx` - Testing
- `alembic` - Database migrations (optional for Phase II)

**Frontend:**
- `next` (v16+) - React framework
- `react` (v19+) - UI library
- `typescript` - Type safety
- `tailwindcss` - Styling
- `better-auth` - Authentication library
- `swr` or `@tanstack/react-query` - Data fetching
- `zod` - Runtime validation
- `lucide-react` - Icons

**Prohibited:**
- Phase I code CANNOT be deleted (keep as reference in `src/`)
- No manual SQL queries (use SQLModel ORM)
- No plain JavaScript (TypeScript required for frontend)
- No session-based auth (JWT only)

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

## Phase II Development Workflow

**Phase II Development Cycle (follows same pattern as Phase I with additions):**

1. **Specification Phase**:
   - Create Phase II specs in `specs/phase-2/` directory
   - Define user stories, API contracts, database schema, UI mockups
   - Review and refine specs with Claude Code

2. **Planning Phase**:
   - Create architectural plan in `specs/phase-2/architecture.md`
   - Break down into backend and frontend tasks
   - Identify integration points and dependencies

3. **Backend Implementation**:
   - Set up FastAPI structure in `backend/` directory
   - Implement database models with SQLModel
   - Create API endpoints with authentication middleware
   - Write backend tests (pytest)

4. **Frontend Implementation**:
   - Set up Next.js 16 App Router in `frontend/` directory
   - Implement UI components with TypeScript + Tailwind
   - Configure Better Auth for authentication
   - Connect to backend API
   - Write frontend tests (Jest + React Testing Library)

5. **Integration Phase**:
   - Test end-to-end user flows
   - Validate API contracts between frontend and backend
   - Fix cross-origin and authentication issues

6. **Deployment Phase**:
   - Deploy frontend to Vercel
   - Deploy backend to Railway/Render/Fly.io
   - Configure environment variables in production
   - Test production deployment

7. **Documentation Phase**:
   - Update README with Phase II setup instructions
   - Document API endpoints (OpenAPI/Swagger)
   - Create demo video (max 90 seconds)

---

**Version**: 2.0.0 | **Ratified**: 2025-12-10 | **Phase II Added**: 2025-12-15 | **Last Amended**: 2025-12-15
