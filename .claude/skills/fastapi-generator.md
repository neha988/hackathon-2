# FastAPI Generator Skill

## Purpose
Generate complete FastAPI endpoints from specifications - supports any endpoint type (CRUD, custom business logic, webhooks, etc.)

## Inputs
- **Endpoint Specification**: Route path, HTTP method, business logic description
- **Request Schema**: Input validation requirements (query params, body, path params)
- **Response Schema**: Output data structure and status codes
- **Dependencies**: Auth requirements, database access, external services

## Outputs
- FastAPI route handler with proper decorators
- Pydantic models for request/response validation
- Business logic implementation
- Error handling and status codes
- Type hints and documentation

## Instructions

You are a FastAPI code generation specialist. When given an endpoint specification:

### 1. Analyze the Specification
- Parse the route path, method, and purpose
- Identify all input parameters (path, query, body, headers)
- Determine response types and status codes
- Note any authentication/authorization requirements
- Identify database or external service dependencies

### 2. Generate Pydantic Models
```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RequestModel(BaseModel):
    """Generated based on input schema"""
    field_name: str = Field(..., description="Field description")
    # Add all required and optional fields with proper types

class ResponseModel(BaseModel):
    """Generated based on output schema"""
    # Add all response fields with proper types
```

### 3. Generate Route Handler
```python
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

router = APIRouter(prefix="/api", tags=["tag-name"])

@router.{method}("/{path}")
async def endpoint_name(
    # Path parameters
    # Query parameters
    # Request body (if applicable)
    # Dependencies (DB session, current user, etc.)
) -> ResponseModel:
    """
    Endpoint documentation

    Args:
        - parameter descriptions

    Returns:
        ResponseModel: Description of response

    Raises:
        HTTPException: Error conditions
    """
    try:
        # 1. Validate inputs
        # 2. Implement business logic
        # 3. Return response
        pass
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
```

### 4. Include Proper Error Handling
- Validate all inputs
- Handle common error cases (404, 400, 401, 403, 500)
- Return appropriate HTTP status codes
- Provide clear error messages

### 5. Add Type Hints and Documentation
- Full type hints for all parameters and returns
- Docstrings for endpoints and models
- OpenAPI documentation tags

### 6. Follow Best Practices
- Use async/await for I/O operations
- Dependency injection for DB sessions and auth
- Proper status code usage
- Input validation via Pydantic
- Error responses in consistent format

## Example Usage

**Input Specification:**
```markdown
Endpoint: GET /api/users/{user_id}/tasks
Purpose: Retrieve all tasks for a specific user with optional filtering
Auth: Required (JWT)
Query Params: status (optional), limit (optional, default 10)
Response: List of tasks with id, title, status, created_at
```

**Generated Output:**
```python
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlmodel import Session, select
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api", tags=["tasks"])

# Response Model
class TaskResponse(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

# Route Handler
@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_user_tasks(
    user_id: str = Path(..., description="User ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    limit: int = Query(10, ge=1, le=100, description="Max tasks to return"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
) -> List[TaskResponse]:
    """
    Retrieve all tasks for a specific user.

    Args:
        user_id: The ID of the user
        status: Optional status filter (pending/completed)
        limit: Maximum number of tasks to return
        db: Database session
        current_user: Authenticated user from JWT

    Returns:
        List[TaskResponse]: List of tasks matching criteria

    Raises:
        HTTPException 401: Unauthorized access
        HTTPException 404: User not found
    """
    # Verify user authorization
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this user's tasks"
        )

    # Build query
    query = select(Task).where(Task.user_id == user_id)
    if status:
        query = query.where(Task.status == status)
    query = query.limit(limit)

    # Execute query
    tasks = db.exec(query).all()

    return tasks
```

## Validation Checklist
Before returning generated code, verify:
- [ ] All input parameters are validated
- [ ] Proper HTTP methods and status codes
- [ ] Type hints on all functions
- [ ] Error handling for common cases
- [ ] Docstrings and OpenAPI documentation
- [ ] Follows FastAPI best practices
- [ ] Security considerations (auth, input sanitization)
- [ ] Code is properly formatted and readable

## Common Patterns

### CRUD Operations
- GET: Retrieve resources
- POST: Create resources
- PUT/PATCH: Update resources
- DELETE: Remove resources

### Authentication
```python
current_user: dict = Depends(get_current_user)
```

### Database Access
```python
db: Session = Depends(get_db)
```

### Pagination
```python
skip: int = Query(0, ge=0)
limit: int = Query(10, ge=1, le=100)
```

### File Uploads
```python
from fastapi import UploadFile, File
file: UploadFile = File(...)
```

## Notes
- Always use async/await for I/O operations
- Prefer dependency injection over global state
- Validate all user inputs
- Return meaningful error messages
- Keep business logic separate from route handlers when complex
- Use SQLModel/SQLAlchemy for database operations
- Follow RESTful conventions unless specified otherwise
