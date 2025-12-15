# Phase II Skills - Full-Stack Development

This directory contains 5 reusable Claude Code Agent Skills for building full-stack applications efficiently.

## 📋 Skills Overview

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| **FastAPI Generator** | Generate FastAPI endpoints | Creating backend API routes |
| **Database Schema Generator** | Generate SQLModel models | Designing database schema |
| **Next.js Component Generator** | Generate React components | Building UI components |
| **Auth Integration Helper** | Setup Better Auth + JWT | Implementing authentication |
| **API Client Generator** | Generate type-safe API client | Connecting frontend to backend |

---

## 🚀 How to Use These Skills

### In Claude Code CLI:

When you need to use a skill, reference it in your conversation:

```bash
# Example: Generate a FastAPI endpoint
"Using the FastAPI Generator skill, create an endpoint for:
GET /api/{user_id}/tasks
- Returns list of tasks
- Requires JWT auth
- Filters by status (optional)"

# Example: Generate a database model
"Using the Database Schema Generator skill, create a Task model with:
- id (primary key)
- user_id (foreign key to users)
- title (required, max 200 chars)
- completed (boolean)"

# Example: Generate a React component
"Using the Next.js Component Generator skill, create a TaskCard component:
- Shows task title and description
- Toggle complete button
- Delete button
- Tailwind styling"
```

### In Agent Context:

Skills are automatically available to specialized agents when they're working on related tasks.

---

## 📦 Skill Details

### 1. FastAPI Generator
**File:** `fastapi-generator.md`

**What it does:**
- Generates complete FastAPI endpoints
- Creates Pydantic request/response models
- Adds proper error handling
- Includes type hints and documentation

**Example Request:**
```
Create a POST endpoint to add a new task:
- Route: /api/{user_id}/tasks
- Body: title (required), description (optional)
- Auth: JWT required
- Response: Created task object
```

**Example Output:**
```python
@router.post("/{user_id}/tasks", response_model=TaskResponse)
async def create_task(
    user_id: str,
    task_input: CreateTaskInput,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> TaskResponse:
    # ... implementation
```

---

### 2. Database Schema Generator
**File:** `database-schema-generator.md`

**What it does:**
- Generates SQLModel database models
- Creates relationships (one-to-many, many-to-many)
- Adds indexes and constraints
- Includes validation logic

**Example Request:**
```
Create database models for:
- User: id, email (unique), name, created_at
- Task: id, user_id (FK to user), title, description, completed, timestamps
- Relationship: User has many Tasks
```

**Example Output:**
```python
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(..., unique=True, index=True)
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    user: Optional[User] = Relationship(back_populates="tasks")
```

---

### 3. Next.js Component Generator
**File:** `nextjs-component-generator.md`

**What it does:**
- Generates TypeScript React components
- Adds Tailwind CSS styling
- Determines server vs client component
- Includes accessibility features

**Example Request:**
```
Create a TaskList component:
- Props: tasks array, onToggle, onDelete
- Display tasks in a grid (responsive)
- Show empty state when no tasks
- Client component (needs interactivity)
```

**Example Output:**
```typescript
'use client'

import { FC } from 'react'

interface TaskListProps {
  tasks: Task[]
  onToggle: (id: number) => void
  onDelete: (id: number) => void
}

export const TaskList: FC<TaskListProps> = ({
  tasks,
  onToggle,
  onDelete
}) => {
  // ... implementation with Tailwind
}
```

---

### 4. Auth Integration Helper
**File:** `auth-integration-helper.md`

**What it does:**
- Sets up Better Auth (frontend)
- Creates JWT verification middleware (backend)
- Generates login/signup forms
- Implements protected routes

**Example Request:**
```
Set up authentication with:
- Email/password login
- JWT tokens (7 day expiration)
- Protected backend routes
- Login and signup forms
```

**Example Output:**
```typescript
// Frontend: lib/auth.ts
export const auth = betterAuth({
  database: { url: process.env.DATABASE_URL },
  session: { cookieCache: { maxAge: 60 * 60 * 24 * 7 } },
  secret: process.env.BETTER_AUTH_SECRET,
})

// Backend: auth.py
def verify_token(credentials: HTTPAuthorizationCredentials):
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload
```

---

### 5. API Client Generator
**File:** `api-client-generator.md`

**What it does:**
- Generates type-safe TypeScript API client
- Adds authentication headers
- Creates error handling
- Optionally generates React Query hooks

**Example Request:**
```
Create API client for task endpoints:
- GET /api/{user_id}/tasks (with filters)
- POST /api/{user_id}/tasks
- PUT /api/{user_id}/tasks/{id}
- DELETE /api/{user_id}/tasks/{id}
Include auth token injection
```

**Example Output:**
```typescript
export const api = {
  tasks: {
    list: (userId: string, filters?: TaskFilters) =>
      apiClient.get<Task[]>(`/api/${userId}/tasks`, filters),

    create: (userId: string, input: CreateTaskInput) =>
      apiClient.post<Task>(`/api/${userId}/tasks`, input),

    // ... other methods
  }
}
```

---

## 🔄 Workflow Example

Here's how to use multiple skills together:

### Step 1: Design Database Schema
```
Use Database Schema Generator to create User and Task models
```

### Step 2: Generate Backend API
```
Use FastAPI Generator to create:
- POST /api/{user_id}/tasks (create)
- GET /api/{user_id}/tasks (list)
- DELETE /api/{user_id}/tasks/{id} (delete)
```

### Step 3: Setup Authentication
```
Use Auth Integration Helper to add:
- Better Auth setup
- JWT middleware
- Login/signup forms
```

### Step 4: Create API Client
```
Use API Client Generator to create type-safe frontend client
```

### Step 5: Build UI Components
```
Use Next.js Component Generator to create:
- TaskCard component
- TaskList component
- AddTaskForm component
```

---

## 💡 Tips for Best Results

1. **Be Specific:** Provide detailed requirements including field types, validation rules, and behavior
2. **Reference Specs:** Point to specification files when they exist
3. **Iterate:** Start with basic version, then refine
4. **Combine Skills:** Use multiple skills together for end-to-end features
5. **Test Generated Code:** Always review and test the output

---

## 🎯 Benefits

- **Consistency:** All code follows same patterns and best practices
- **Speed:** Generate boilerplate 10x faster
- **Type Safety:** Full TypeScript coverage
- **Documentation:** Auto-generated comments and docs
- **Best Practices:** Security, accessibility, error handling built-in
- **Reusability:** Same skills work across different projects

---

## 📝 Customization

Each skill file is a markdown document. You can:
- Edit the templates to match your preferences
- Add new patterns and examples
- Customize naming conventions
- Add project-specific requirements

---

## 🏆 Bonus Points

These skills qualify for the **Reusable Intelligence Bonus** (+200 points) in the hackathon!

To maximize points:
1. Document usage of each skill in your submission
2. Show before/after (manual vs skill-generated code)
3. Demonstrate time saved
4. Create additional custom skills if needed

---

## 📚 Next Steps

After creating these skills, you're ready to:

1. **Set up project structure** (monorepo)
2. **Write specifications** for features
3. **Use skills to generate code**
4. **Deploy to Vercel/production**

Good luck with Phase II! 🚀
