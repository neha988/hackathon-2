# Backend Development Guidelines - Phase II

This file provides context-specific instructions for the FastAPI backend application.

## Stack Overview

- **Framework**: FastAPI (Python 3.13+)
- **ORM**: SQLModel (combines SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification (tokens issued by Better Auth on frontend)
- **Testing**: pytest, pytest-asyncio, pytest-cov
- **Package Manager**: UV

## Project Structure

```
backend/
├── app/
│   ├── __init__.py           # Application package initialization
│   ├── main.py               # FastAPI app entry point, CORS, middleware
│   ├── db.py                 # Database connection and session management
│   ├── models/               # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py           # User model (Better Auth managed)
│   │   └── task.py           # Task model with user relationship
│   ├── routes/               # API route handlers
│   │   ├── __init__.py
│   │   ├── tasks.py          # Task CRUD endpoints
│   │   └── health.py         # Health check endpoint
│   ├── services/             # Business logic layer
│   │   ├── __init__.py
│   │   └── task_service.py   # Task business logic
│   ├── middleware/           # Custom middleware
│   │   ├── __init__.py
│   │   └── auth.py           # JWT verification middleware
│   └── schemas/              # Pydantic request/response schemas
│       ├── __init__.py
│       └── task.py           # Task request/response models
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_tasks.py         # Task API tests
│   └── test_auth.py          # Authentication tests
├── pyproject.toml            # UV/pip dependencies
├── .env                      # Environment variables (gitignored)
├── .env.example              # Environment template
└── CLAUDE.md                 # This file
```

## API Design Conventions

### Endpoint Patterns

All task endpoints follow the pattern: `/api/{user_id}/tasks/...`

| Method | Endpoint | Description | Request Body | Response |
|--------|----------|-------------|--------------|----------|
| GET | `/api/{user_id}/tasks` | List all tasks | - | `List[Task]` |
| POST | `/api/{user_id}/tasks` | Create task | `TaskCreate` | `Task` |
| GET | `/api/{user_id}/tasks/{id}` | Get task by ID | - | `Task` |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | `TaskUpdate` | `Task` |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | - | `{"message": "..."}` |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | - | `Task` |

### HTTP Status Codes

Use proper status codes consistently:

- **200 OK**: Successful GET, PUT, PATCH
- **201 Created**: Successful POST (task created)
- **204 No Content**: Successful DELETE (optional)
- **400 Bad Request**: Invalid input data (validation error)
- **401 Unauthorized**: Missing or invalid JWT token
- **403 Forbidden**: User ID mismatch (authenticated user != URL user_id)
- **404 Not Found**: Task doesn't exist or doesn't belong to user
- **500 Internal Server Error**: Unexpected server error

### Request/Response Models

Use Pydantic schemas for validation:

**Request Models:**
```python
# schemas/task.py
from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
```

**Response Models:**
```python
from datetime import datetime

class Task(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel
```

## Database Models with SQLModel

### Task Model Example

```python
# app/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Database Connection

```python
# app/db.py
from sqlmodel import SQLModel, create_engine, Session
from contextlib import contextmanager
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
```

## Authentication Middleware

### JWT Verification

```python
# app/middleware/auth.py
from fastapi import Depends, HTTPException, Header
import jwt
import os

SECRET = os.getenv("BETTER_AUTH_SECRET")

async def verify_jwt(authorization: str = Header(None)) -> str:
    """
    Verify JWT token and return user_id from payload.

    Args:
        authorization: Authorization header with "Bearer <token>"

    Returns:
        str: User ID from JWT payload

    Raises:
        HTTPException: 401 if token is missing or invalid
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### User Isolation Enforcement

Always validate that the authenticated user matches the user_id in the URL:

```python
# In route handler
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(verify_jwt)
):
    if user_id != authenticated_user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Proceed with query
```

## CORS Configuration

Configure CORS in `main.py` to allow frontend requests:

```python
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Todo API", version="1.0.0")

origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Testing Standards

### Test Structure

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from app.main import app
from app.db import get_session

# Use in-memory SQLite for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture
def client():
    SQLModel.metadata.create_all(test_engine)

    def override_get_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session

    with TestClient(app) as test_client:
        yield test_client

    SQLModel.metadata.drop_all(test_engine)
```

### API Endpoint Tests

```python
# tests/test_tasks.py
def test_create_task(client, auth_headers):
    response = client.post(
        "/api/user123/tasks",
        json={"title": "Test task", "description": "Test description"},
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False
```

## Error Handling

Implement consistent error handling:

```python
from fastapi import HTTPException
from sqlmodel.exc import NoResultFound

try:
    task = session.get(Task, task_id)
    if not task or task.user_id != authenticated_user_id:
        raise HTTPException(status_code=404, detail="Task not found")
except NoResultFound:
    raise HTTPException(status_code=404, detail="Task not found")
```

## Running the Backend

### Development

```bash
# Install dependencies with UV
uv pip install -e ".[dev]"

# Create .env file with DATABASE_URL and BETTER_AUTH_SECRET

# Run with uvicorn
uvicorn app.main:app --reload --port 8000
```

### Testing

```bash
# Run all tests with coverage
pytest

# Run specific test file
pytest tests/test_tasks.py

# Run with verbose output
pytest -v --cov=app --cov-report=html
```

## Code Style Guidelines

- **Type Hints**: Required on all function parameters and return values
- **Docstrings**: Google-style docstrings for all public functions
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Line Length**: Max 100 characters (enforced by Black)
- **Imports**: Organize with isort (stdlib, third-party, local)

## Security Checklist

- [ ] Never commit `.env` file (ensure in `.gitignore`)
- [ ] Always validate user_id matches authenticated user
- [ ] Use parameterized queries (SQLModel handles this)
- [ ] Validate all input data with Pydantic schemas
- [ ] Log errors without exposing sensitive data
- [ ] Use HTTPS in production (enforce secure cookies)
- [ ] Set proper CORS origins (no wildcards in production)

## References

- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **SQLModel Docs**: https://sqlmodel.tiangolo.com/
- **Better Auth Integration**: See root CLAUDE.md
- **Constitution**: `.specify/memory/constitution.md`
- **API Specs**: `specs/phase-2/api/`
