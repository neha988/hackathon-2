# Database Schema Specification

**Version**: 1.0.0
**Date**: 2025-12-15
**Database**: Neon Serverless PostgreSQL

---

## Overview

This specification defines the complete database schema for Phase II, including tables, relationships, indexes, constraints, and SQLModel implementation.

**Connection String** (already configured):
```
postgresql://neondb_owner:npg_le3dYHE1hOmt@ep-flat-sky-ad666q3a-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
```

---

## Tables

### 1. users table (Better Auth managed)

**Purpose**: Store user accounts (managed by Better Auth)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

**SQLModel Implementation**:
```python
# backend/app/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True)
    name: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Constraints**:
- `id`: UUID primary key (auto-generated)
- `email`: Unique, indexed for fast login lookups
- `name`: Required
- `password_hash`: Managed by Better Auth (bcrypt)
- Timestamps: UTC timezone

---

### 2. tasks table

**Purpose**: Store todo tasks for all users

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_created_at ON tasks(created_at DESC);
```

**SQLModel Implementation**:
```python
# backend/app/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from uuid import UUID

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200, min_length=1)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship (optional, for ORM convenience)
    # user: Optional[User] = Relationship(back_populates="tasks")
```

**Constraints**:
- `id`: Auto-increment integer primary key
- `user_id`: Foreign key to users.id, indexed, ON DELETE CASCADE
- `title`: Required, 1-200 characters
- `description`: Optional, max 1000 characters
- `completed`: Boolean, default FALSE, indexed
- Timestamps: Auto-generated, UTC timezone

---

## Indexes

| Index Name | Table | Columns | Purpose | Type |
|------------|-------|---------|---------|------|
| `users_pkey` | users | id | Primary key | B-tree |
| `users_email_key` | users | email | Unique constraint + fast login | B-tree |
| `tasks_pkey` | tasks | id | Primary key | B-tree |
| `idx_tasks_user_id` | tasks | user_id | User isolation queries | B-tree |
| `idx_tasks_completed` | tasks | completed | Filter by status | B-tree |
| `idx_tasks_created_at` | tasks | created_at DESC | Sort by date (newest first) | B-tree |

**Query Optimization**:
- Every task query filters by `user_id` → indexed
- Filtering by completion status → indexed
- Sorting by created date → indexed with DESC order

---

## Relationships

```
┌─────────────┐           ┌─────────────┐
│   users     │           │   tasks     │
│─────────────│           │─────────────│
│ id (PK)     │◄─────────┤ user_id (FK)│
│ email       │   1:N     │ id (PK)     │
│ name        │           │ title       │
│ password    │           │ description │
│ created_at  │           │ completed   │
│ updated_at  │           │ created_at  │
└─────────────┘           │ updated_at  │
                          └─────────────┘
```

**Relationship Rules**:
- One user can have many tasks (1:N)
- Each task belongs to exactly one user
- Deleting a user cascades to delete all their tasks
- Orphaned tasks are not allowed (foreign key constraint)

---

## Data Validation Rules

### User Table
| Field | Validation |
|-------|-----------|
| `email` | Valid email format, unique across system |
| `name` | 1-255 characters, no special validation |
| `password` | Min 8 characters (enforced by Better Auth) |

### Task Table
| Field | Validation |
|-------|-----------|
| `title` | Required, 1-200 characters, trimmed (no leading/trailing whitespace) |
| `description` | Optional, max 1000 characters |
| `completed` | Boolean only (true/false) |
| `user_id` | Must exist in users table (foreign key enforced) |

**Backend Validation** (Pydantic schemas):
```python
# backend/app/schemas/task.py
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    @field_validator('title')
    def title_must_not_be_empty(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace')
        return v.strip() if v else None
```

---

## Database Connection Setup

**Backend Configuration**:
```python
# backend/app/db.py
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

# Get connection URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL logging in development
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,  # Number of connections to maintain
    max_overflow=10,  # Max additional connections
)

def create_db_and_tables():
    """Create all tables (run once on startup)"""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency for FastAPI routes"""
    with Session(engine) as session:
        yield session
```

**Usage in FastAPI**:
```python
# backend/app/routes/tasks.py
from fastapi import Depends
from sqlmodel import Session
from app.db import get_session

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    session: Session = Depends(get_session)
):
    # Use session to query database
    tasks = session.exec(
        select(Task).where(Task.user_id == user_id)
    ).all()
    return tasks
```

---

## Sample Data (for Testing)

```sql
-- Sample user (for development/testing)
INSERT INTO users (id, email, name, password_hash, created_at, updated_at)
VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'test@example.com',
    'Test User',
    '$2b$12$hashedpasswordhere',
    NOW(),
    NOW()
);

-- Sample tasks
INSERT INTO tasks (user_id, title, description, completed, created_at, updated_at)
VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Buy groceries', 'Milk, eggs, bread', false, NOW(), NOW()),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Finish homework', 'Math chapter 5', false, NOW(), NOW()),
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'Call dentist', NULL, true, NOW(), NOW());
```

---

## Migration Strategy

### Option 1: SQLModel Auto-Create (Development)
```python
# backend/app/main.py
from app.db import create_db_and_tables

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
```

**Pros**: Simple, no migration files needed
**Cons**: Not suitable for production schema changes

### Option 2: Alembic Migrations (Production - Optional)
```bash
# Install Alembic
uv pip install alembic

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "create users and tasks tables"

# Apply migration
alembic upgrade head
```

**For Phase II**: Use Option 1 (SQLModel auto-create). Alembic is optional.

---

## Database Queries (Common Patterns)

### 1. Get all tasks for a user
```python
from sqlmodel import select

tasks = session.exec(
    select(Task)
    .where(Task.user_id == user_id)
    .order_by(Task.created_at.desc())
).all()
```

### 2. Create a task
```python
task = Task(
    user_id=user_id,
    title="New task",
    description="Optional description"
)
session.add(task)
session.commit()
session.refresh(task)  # Get auto-generated id and timestamps
```

### 3. Update a task
```python
task = session.get(Task, task_id)
if task and task.user_id == user_id:
    task.title = "Updated title"
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
```

### 4. Delete a task
```python
task = session.get(Task, task_id)
if task and task.user_id == user_id:
    session.delete(task)
    session.commit()
```

### 5. Toggle completion
```python
task = session.get(Task, task_id)
if task and task.user_id == user_id:
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()
    session.add(task)
    session.commit()
```

---

## Performance Considerations

### Indexing
- ✅ All foreign keys indexed
- ✅ Frequently filtered columns indexed (completed, created_at)
- ✅ Email indexed for login queries

### Connection Pooling
- Pool size: 5 connections (adjust based on load)
- Max overflow: 10 (burst capacity)
- Pre-ping: Enabled (verify connections)

### Query Optimization
- Always filter by `user_id` first (indexed)
- Use `select()` with specific columns for large datasets
- Limit results with `.limit()` if needed

---

## Security Considerations

### SQL Injection Prevention
- ✅ SQLModel uses parameterized queries (automatic protection)
- ✅ Never use string concatenation for queries
- ✅ Use ORM methods (session.exec, select, where)

### User Isolation
- ✅ Every query MUST filter by `user_id`
- ✅ Foreign key constraint prevents orphaned tasks
- ✅ CASCADE delete ensures data cleanup

### Data Protection
- ✅ Passwords hashed (Better Auth handles this)
- ✅ Connection encrypted (sslmode=require)
- ✅ No sensitive data in task table (safe to log)

---

## Acceptance Criteria

- [ ] `users` table created with UUID primary key
- [ ] `tasks` table created with foreign key to users
- [ ] All indexes created (user_id, completed, created_at)
- [ ] Foreign key cascade delete working
- [ ] SQLModel models match database schema exactly
- [ ] Database connection successful with Neon URL
- [ ] Sample data can be inserted and queried
- [ ] User isolation enforced (queries filter by user_id)
- [ ] Timestamps auto-generated in UTC
- [ ] Title validation (1-200 chars) enforced

---

## TypeScript Types (Frontend)

```typescript
// frontend/types/task.ts
export interface Task {
  id: number
  user_id: string  // UUID string
  title: string
  description: string | null
  completed: boolean
  created_at: string  // ISO 8601 format
  updated_at: string  // ISO 8601 format
}

export interface TaskCreate {
  title: string
  description?: string
}

export interface TaskUpdate {
  title?: string
  description?: string
}
```

---

**Status**: ✅ Complete
**Next**: Create API endpoints specification
