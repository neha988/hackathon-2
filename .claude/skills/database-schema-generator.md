# Database Schema Generator Skill

## Purpose
Generate SQLModel database models from schema specifications with proper relationships, constraints, and type safety.

## Inputs
- **Schema Specification**: Markdown or structured description of database tables
- **Table Definitions**: Table names, columns, types, constraints
- **Relationships**: Foreign keys, one-to-many, many-to-many relationships
- **Indexes**: Performance optimization requirements

## Outputs
- SQLModel model classes with proper type hints
- Relationship definitions (Foreign Keys, relationships)
- Indexes and constraints
- Migration-ready code
- Pydantic validation integration

## Instructions

You are a database schema generation specialist. When given a schema specification:

### 1. Analyze the Schema Specification
- Identify all tables and their columns
- Determine column types and constraints
- Map relationships between tables
- Note indexes and unique constraints
- Identify required vs optional fields

### 2. Generate SQLModel Classes

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class TableName(SQLModel, table=True):
    """Table documentation"""
    __tablename__ = "table_name"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # Regular columns
    column_name: str = Field(..., max_length=200, index=True)
    optional_column: Optional[str] = Field(default=None, max_length=500)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Foreign keys
    foreign_id: Optional[int] = Field(default=None, foreign_key="other_table.id")

    # Relationships
    related_items: List["RelatedModel"] = Relationship(back_populates="parent")
```

### 3. Implement Relationships

**One-to-Many:**
```python
# Parent
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="user")

# Child
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="tasks")
```

**Many-to-Many:**
```python
# Link table
class TaskTagLink(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)

# Models with relationships
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTagLink)

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)
```

### 4. Add Constraints and Validation

```python
from pydantic import validator

class Task(SQLModel, table=True):
    title: str = Field(..., min_length=1, max_length=200)
    status: str = Field(default="pending")

    @validator("status")
    def validate_status(cls, v):
        allowed = ["pending", "in_progress", "completed"]
        if v not in allowed:
            raise ValueError(f"Status must be one of {allowed}")
        return v
```

### 5. Create Indexes

```python
from sqlmodel import Field, Index

class Task(SQLModel, table=True):
    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_created_at", "created_at"),
    )

    user_id: int = Field(foreign_key="user.id", index=True)
    status: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 6. Type Mapping

| Spec Type | SQLModel/Python Type |
|-----------|---------------------|
| string | `str` |
| integer | `int` |
| boolean | `bool` |
| timestamp/datetime | `datetime` |
| text (long) | `str` (no max_length) |
| decimal/float | `float` |
| uuid | `uuid.UUID` |
| json | `dict` or custom Pydantic model |

### 7. Best Practices Checklist
- [ ] All models inherit from `SQLModel` with `table=True`
- [ ] Primary keys are `Optional[int]` with `primary_key=True`
- [ ] Foreign keys reference correct table and column
- [ ] Timestamps use `default_factory=datetime.utcnow`
- [ ] Required fields use `...`, optional use `Optional` and `default=None`
- [ ] String fields have appropriate `max_length`
- [ ] Indexes on frequently queried columns
- [ ] Relationships use proper `back_populates`
- [ ] Table names are lowercase with underscores
- [ ] Docstrings for all models

## Example Usage

**Input Schema Specification:**
```markdown
## Users Table
- id: integer (primary key)
- email: string (unique, required)
- name: string (required)
- created_at: timestamp

## Tasks Table
- id: integer (primary key)
- user_id: integer (foreign key -> users.id)
- title: string (required, max 200)
- description: text (optional)
- status: string (default: "pending", enum: pending/completed)
- completed: boolean (default: false)
- created_at: timestamp
- updated_at: timestamp

Relationships:
- User has many Tasks
- Task belongs to User

Indexes:
- tasks.user_id
- tasks.status
- tasks.created_at
```

**Generated Output:**
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from pydantic import EmailStr, validator

# User Model
class User(SQLModel, table=True):
    """User account model"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(..., unique=True, index=True)
    name: str = Field(..., max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="user")

# Task Model
class Task(SQLModel, table=True):
    """Task/Todo item model"""
    __tablename__ = "tasks"

    __table_args__ = (
        Index("idx_user_status", "user_id", "status"),
        Index("idx_created_at", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", max_length=20)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")

    @validator("status")
    def validate_status(cls, v):
        allowed_statuses = ["pending", "completed"]
        if v not in allowed_statuses:
            raise ValueError(f"Status must be one of {allowed_statuses}")
        return v

# Database initialization
from sqlmodel import create_engine, Session

def get_engine():
    """Create database engine"""
    DATABASE_URL = "postgresql://user:password@host:port/dbname"
    return create_engine(DATABASE_URL, echo=True)

def init_db():
    """Create all tables"""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session for dependency injection"""
    engine = get_engine()
    with Session(engine) as session:
        yield session
```

## Advanced Patterns

### Soft Deletes
```python
class Task(SQLModel, table=True):
    is_deleted: bool = Field(default=False)
    deleted_at: Optional[datetime] = Field(default=None)
```

### Audit Fields
```python
class AuditMixin(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
```

### Enum Types
```python
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(SQLModel, table=True):
    status: TaskStatus = Field(default=TaskStatus.PENDING)
```

### JSON Fields
```python
from typing import Dict, Any

class Task(SQLModel, table=True):
    metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
```

## Validation Rules

### Always Include:
1. Primary key as `Optional[int]`
2. Timestamps for created/updated tracking
3. Foreign keys with proper `foreign_key` constraint
4. Indexes on columns used in WHERE clauses
5. `__tablename__` for explicit table naming
6. Docstrings explaining the model purpose

### Avoid:
1. Circular imports (use string forward references: `"ModelName"`)
2. Mutable defaults (use `default_factory` instead)
3. Missing `back_populates` in relationships
4. Forgetting `table=True` flag
5. Using `None` without `Optional` type hint

## Database Connection Helper

```python
from sqlmodel import create_engine, Session, select
from contextlib import contextmanager

class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, echo=True)

    def init_db(self):
        """Create all tables"""
        SQLModel.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self):
        """Context manager for database sessions"""
        with Session(self.engine) as session:
            yield session

    def get_session_dependency(self):
        """For FastAPI dependency injection"""
        with Session(self.engine) as session:
            yield session
```

## Notes
- Always use `Optional[int]` for auto-increment primary keys
- Use `default_factory=datetime.utcnow` NOT `default=datetime.utcnow()`
- Foreign keys must reference actual table names (lowercase)
- For Neon/PostgreSQL, use `postgresql://` connection string
- Relationships are optional - only add if specified in schema
- Index frequently queried columns (user_id, status, dates)
- Use proper Pydantic validators for business logic constraints
