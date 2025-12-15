# Phase II Specialized Agents

This directory contains 3 specialized agents for building full-stack applications efficiently. Each agent has expertise in a specific domain and uses dedicated skills.

## 🤖 Agent Overview

| Agent | Icon | Expertise | Skills Used | Slash Command |
|-------|------|-----------|-------------|---------------|
| **Backend Architect** | 🎯 | FastAPI, SQLModel, Database | FastAPI Generator, Schema Generator | `/backend` |
| **Frontend Builder** | 🎨 | Next.js, React, TypeScript | Component Generator, API Client Generator | `/frontend` |
| **Auth Specialist** | 🔐 | Better Auth, JWT, Security | Auth Integration Helper | `/auth` |

---

## 🚀 Quick Start

### Using Slash Commands (Recommended)

```bash
# Backend task
/backend Create API endpoints for task management with CRUD operations

# Frontend task
/frontend Build a TaskList component with add, complete, and delete actions

# Authentication task
/auth Set up email/password authentication with JWT tokens
```

### Using Natural Language

```bash
# The agents will be automatically invoked based on context
"I need database models for User and Task with a one-to-many relationship"
→ Backend Architect agent will be suggested

"Create a responsive task card component with Tailwind"
→ Frontend Builder agent will be suggested

"Set up user authentication with signup and login"
→ Auth Specialist agent will be suggested
```

---

## 📋 Agent Details

### 1. Backend Architect 🎯

**File:** `backend-architect.md`

**Responsibilities:**
- Design database schemas
- Create REST API endpoints
- Implement data validation
- Optimize database queries
- Handle business logic

**Technologies:**
- FastAPI (async web framework)
- SQLModel (type-safe ORM)
- Neon PostgreSQL (serverless database)
- Pydantic (data validation)
- Alembic (migrations)

**Skills:**
- **FastAPI Generator**: Generates FastAPI endpoints from specs
- **Database Schema Generator**: Creates SQLModel models with relationships

**When to Use:**
- Creating database models
- Building API endpoints
- Implementing backend business logic
- Optimizing database queries
- Adding data validation

**Example Task:**
```
Create an API for task management:
- GET /api/{user_id}/tasks - List tasks
- POST /api/{user_id}/tasks - Create task
- PUT /api/{user_id}/tasks/{id} - Update task
- DELETE /api/{user_id}/tasks/{id} - Delete task
All endpoints require JWT authentication
```

**Output:**
```python
# Complete database models
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    title: str = Field(..., max_length=200)
    # ... complete implementation

# Complete API routes
@router.get("/{user_id}/tasks")
async def get_tasks(...):
    # ... complete implementation with auth
```

---

### 2. Frontend Builder 🎨

**File:** `frontend-builder.md`

**Responsibilities:**
- Build React components
- Create Next.js pages
- Integrate with APIs
- Implement responsive design
- Ensure accessibility

**Technologies:**
- Next.js 16+ (App Router)
- React 19 (Server/Client Components)
- TypeScript (type safety)
- Tailwind CSS (styling)
- React Hook Form (forms)

**Skills:**
- **Next.js Component Generator**: Creates React/TypeScript components
- **API Client Generator**: Generates type-safe API clients

**When to Use:**
- Creating UI components
- Building pages and layouts
- Integrating with backend APIs
- Implementing responsive designs
- Adding user interactions

**Example Task:**
```
Create a task management interface:
- TaskList component (displays all tasks)
- TaskCard component (individual task with actions)
- AddTaskForm component (create new tasks)
- Responsive design with Tailwind
- Integrate with backend API
```

**Output:**
```typescript
// Type-safe API client
export const api = {
  tasks: {
    list: (userId: string) => apiClient.get<Task[]>(...),
    create: (userId: string, data: CreateTaskInput) => ...
  }
}

// React components
export const TaskCard: FC<TaskCardProps> = ({ task, onToggle, onDelete }) => {
  // Complete implementation with Tailwind styling
}
```

---

### 3. Auth Specialist 🔐

**File:** `auth-specialist.md`

**Responsibilities:**
- Set up Better Auth
- Configure JWT verification
- Create signup/login flows
- Protect API routes
- Enforce authorization

**Technologies:**
- Better Auth (Next.js auth library)
- JWT (JSON Web Tokens)
- FastAPI Security (auth middleware)
- Python-JOSE (JWT for Python)
- Bcrypt (password hashing)

**Skills:**
- **Auth Integration Helper**: Complete auth setup (frontend + backend)

**When to Use:**
- Setting up authentication
- Creating signup/login forms
- Protecting backend routes
- Implementing session management
- Adding authorization checks

**Example Task:**
```
Set up complete authentication:
- Email/password signup and login
- JWT tokens with 7-day expiration
- Protected API endpoints
- Users can only access their own data
- Logout functionality
```

**Output:**
```typescript
// Frontend: Better Auth setup
export const auth = betterAuth({
  emailAndPassword: { enabled: true },
  session: { cookieCache: { maxAge: 60 * 60 * 24 * 7 } },
  // ... complete config
})

// Backend: JWT verification
def get_current_user(token: str = Depends(verify_token)):
    # ... complete implementation
```

---

## 🔄 Agent Collaboration Workflow

Here's how the agents work together on a feature:

### Example: Building "Task Management Feature"

#### Phase 1: Database & API (Backend Architect)
```
/backend Create database models and API for tasks:
- Task model with user_id, title, description, completed
- CRUD endpoints at /api/{user_id}/tasks
- All endpoints require authentication
```

**Output:**
- ✅ SQLModel Task and User models
- ✅ Complete CRUD API endpoints
- ✅ Request/response validation
- ✅ Authorization checks

#### Phase 2: Authentication (Auth Specialist)
```
/auth Set up authentication:
- Email/password signup and login
- JWT tokens (7 days)
- Protect all /api/* endpoints
```

**Output:**
- ✅ Better Auth configured
- ✅ JWT middleware in FastAPI
- ✅ Signup/login forms
- ✅ Protected routes

#### Phase 3: Frontend UI (Frontend Builder)
```
/frontend Create task management UI:
- API client for task endpoints
- TaskList component
- TaskCard component with complete/delete actions
- AddTaskForm component
- Responsive design
```

**Output:**
- ✅ Type-safe API client
- ✅ All React components
- ✅ Tailwind styling
- ✅ Responsive + accessible

---

## 💡 Best Practices

### When to Use Which Agent

| Task Type | Use This Agent |
|-----------|----------------|
| "Create database model for..." | Backend Architect 🎯 |
| "Build API endpoint for..." | Backend Architect 🎯 |
| "Create a component for..." | Frontend Builder 🎨 |
| "Build a page that shows..." | Frontend Builder 🎨 |
| "Set up authentication..." | Auth Specialist 🔐 |
| "Protect this route..." | Auth Specialist 🔐 |

### Collaboration Tips

1. **Start with Backend:** Create database and API first
2. **Add Auth Second:** Set up authentication if needed
3. **Build Frontend Last:** Create UI that consumes the API

4. **Sequential for New Features:**
   ```
   Backend → Auth (if needed) → Frontend
   ```

5. **Parallel for Independent Changes:**
   ```
   Backend (new endpoint) || Frontend (new component)
   ```

### Communication Between Agents

Agents share information through:
- **API Specifications:** Backend defines, Frontend consumes
- **Type Definitions:** Shared TypeScript/Python types
- **Auth Contracts:** JWT token format and verification

---

## 🎯 Example End-to-End Feature

### Feature: "Add Priority to Tasks"

#### Step 1: Backend Changes
```bash
/backend Add priority field to tasks:
- Update Task model with priority field (high/medium/low)
- Update POST /api/{user_id}/tasks to accept priority
- Update PUT /api/{user_id}/tasks/{id} to update priority
- Add GET /api/{user_id}/tasks with priority filter
```

#### Step 2: Frontend Changes
```bash
/frontend Update UI for task priority:
- Update API client types with priority field
- Add priority dropdown to AddTaskForm
- Display priority badge in TaskCard
- Add priority filter to TaskList
```

**Result:** Complete feature implemented across full stack!

---

## 🏆 Bonus Points Strategy

These agents maximize your hackathon score:

### Reusable Intelligence (+200 points)
- ✅ 3 specialized agents created
- ✅ 5 reusable skills used by agents
- ✅ Documented workflow and collaboration

### Documentation
- Show before/after (manual vs agent-generated code)
- Demonstrate time saved (hours → minutes)
- Document agent usage in README

### Submission Tips
```markdown
## AI-Powered Development

This project was built using 3 specialized Claude Code agents:
- Backend Architect (database + API)
- Frontend Builder (UI components)
- Auth Specialist (authentication)

Each agent uses reusable skills to generate production-ready code:
- FastAPI Generator
- Database Schema Generator
- Next.js Component Generator
- API Client Generator
- Auth Integration Helper

**Time Savings:**
- Manual: ~20 hours
- With Agents: ~4 hours
- **Efficiency Gain: 5x faster**
```

---

## 📁 File Structure

```
.claude/
├── agents/
│   ├── README.md                    # This file
│   ├── backend-architect.md         # Backend agent definition
│   ├── frontend-builder.md          # Frontend agent definition
│   └── auth-specialist.md           # Auth agent definition
├── skills/
│   ├── README.md                    # Skills overview
│   ├── fastapi-generator.md         # FastAPI endpoint generation
│   ├── database-schema-generator.md # SQLModel model generation
│   ├── nextjs-component-generator.md# React component generation
│   ├── api-client-generator.md      # API client generation
│   └── auth-integration-helper.md   # Auth setup
└── commands/
    ├── backend.md                   # /backend command
    ├── frontend.md                  # /frontend command
    └── auth.md                      # /auth command
```

---

## 🚦 Getting Started

### 1. Understand Your Task
```
"I need to build a task management system with user authentication"
```

### 2. Break Down by Domain
```
Backend: Database models + API endpoints
Auth: User signup/login + JWT protection
Frontend: UI components + API integration
```

### 3. Invoke Agents Sequentially
```bash
# Step 1
/backend Create Task and User models with API endpoints

# Step 2
/auth Set up authentication with Better Auth and JWT

# Step 3
/frontend Build task management UI with all components
```

### 4. Review & Integrate
- Test each piece as it's built
- Ensure agents' outputs work together
- Refine as needed

---

## ⚠️ Important Notes

### Agent Constraints

**Backend Architect:**
- ✅ Creates database models and API
- ❌ Does NOT do frontend work

**Frontend Builder:**
- ✅ Builds UI components and pages
- ❌ Does NOT do backend/database work

**Auth Specialist:**
- ✅ Sets up authentication flow
- ❌ Does NOT implement full features (just auth part)

### When to Use Multiple Agents

**Use All 3:**
- New full-stack features with auth
- Complete application setup

**Use Backend + Frontend:**
- Features that don't need auth changes
- Adding new resources

**Use Single Agent:**
- Simple component updates
- Individual API endpoint changes
- Auth configuration tweaks

---

## 🎓 Learning Resources

### Agent Definitions
Each agent file contains:
- Role and expertise
- Available skills
- Best practices
- Code patterns
- Example workflows

### Skills Documentation
Each skill file contains:
- Purpose and inputs/outputs
- Detailed instructions
- Code templates
- Examples
- Validation checklists

### Read These First
1. `.claude/agents/backend-architect.md`
2. `.claude/agents/frontend-builder.md`
3. `.claude/agents/auth-specialist.md`
4. `.claude/skills/README.md`

---

## 🆘 Troubleshooting

### "Agent not generating code"
→ Check that you're using the slash command or clear task description

### "Skills not being used"
→ Agents should auto-use skills; if not, explicitly mention: "Use [Skill Name] skill"

### "Agents conflict"
→ Use one agent at a time for a specific task

### "Missing dependencies"
→ Check that skills are referenced correctly in agent files

---

## 📞 Support

If agents aren't working as expected:
1. Check agent definition files for constraints
2. Verify skills are in `.claude/skills/`
3. Use slash commands for consistent invocation
4. Provide clear, specific task descriptions

---

## 🎉 Success!

You now have a powerful agent system for Phase II development!

**Next Steps:**
1. Try each agent with a simple task
2. Build a complete feature using all 3
3. Document your workflow
4. Maximize those bonus points! 🏆

Good luck with Phase II! 🚀
