# Authentication Specification

**Version**: 1.0.0
**Date**: 2025-12-15
**Authentication Method**: Better Auth + JWT

---

## Overview

This specification defines the complete authentication and authorization system using **Better Auth** on the frontend for user management and **JWT (JSON Web Tokens)** for stateless API authentication between frontend and backend.

**Key Principles**:
- Frontend manages user sessions with Better Auth
- Backend verifies JWT tokens (stateless authentication)
- Shared secret between frontend and backend
- User isolation enforced on every API request
- Secure password hashing (bcrypt via Better Auth)

---

## Authentication Flow

### Complete Authentication Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SIGNUP FLOW                                  │
└─────────────────────────────────────────────────────────────────┘

1. User submits signup form (email, password, name) → Frontend
2. Frontend validates input (Zod schema)
3. Frontend calls Better Auth signup API
4. Better Auth:
   - Validates email format
   - Hashes password (bcrypt)
   - Creates user in database
   - Generates JWT token with payload: { user_id, email, exp }
   - Signs token with BETTER_AUTH_SECRET
5. Frontend stores JWT in HTTP-only cookie (or localStorage)
6. User is redirected to dashboard/tasks page

┌─────────────────────────────────────────────────────────────────┐
│                    SIGNIN FLOW                                  │
└─────────────────────────────────────────────────────────────────┘

1. User submits signin form (email, password) → Frontend
2. Frontend validates input
3. Frontend calls Better Auth signin API
4. Better Auth:
   - Looks up user by email
   - Verifies password hash (bcrypt compare)
   - Generates JWT token with same payload structure
   - Signs token with BETTER_AUTH_SECRET
5. Frontend stores JWT in HTTP-only cookie
6. User is redirected to dashboard/tasks page

┌─────────────────────────────────────────────────────────────────┐
│                    API REQUEST FLOW                             │
└─────────────────────────────────────────────────────────────────┘

1. Frontend makes API request to backend
2. Frontend includes JWT in Authorization header: "Bearer <token>"
3. Backend middleware intercepts request
4. Middleware extracts token from header
5. Middleware verifies JWT signature using BETTER_AUTH_SECRET
6. Middleware decodes JWT payload to extract user_id
7. Middleware validates user_id in URL matches JWT user_id
   - Match → Continue to route handler
   - Mismatch → Return 403 Forbidden
8. Route handler receives authenticated_user_id via dependency
9. Route handler queries database filtered by user_id (user isolation)
```

---

## Frontend: Better Auth Setup

### 1. Installation

```bash
cd frontend
npm install better-auth
```

### 2. Better Auth Configuration

```typescript
// frontend/lib/auth.ts
import { createAuthClient } from "better-auth/client"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  // Better Auth will handle JWT internally
})

// Helper functions
export async function getAuthToken(): Promise<string | null> {
  const session = await authClient.getSession()
  return session?.accessToken || null
}

export async function getCurrentUser() {
  const session = await authClient.getSession()
  return session?.user || null
}
```

### 3. Sign Up Function

```typescript
// frontend/lib/auth.ts
export async function signUp(email: string, password: string, name: string) {
  try {
    const response = await authClient.signUp.email({
      email,
      password,
      name,
    })
    return { success: true, user: response.user }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
```

### 4. Sign In Function

```typescript
export async function signIn(email: string, password: string) {
  try {
    const response = await authClient.signIn.email({
      email,
      password,
    })
    return { success: true, user: response.user }
  } catch (error) {
    return { success: false, error: error.message }
  }
}
```

### 5. Sign Out Function

```typescript
export async function signOut() {
  await authClient.signOut()
  // Redirect to signin page
  window.location.href = "/auth/signin"
}
```

### 6. Auth Hook

```typescript
// frontend/hooks/useAuth.ts
'use client'

import { useEffect, useState } from 'react'
import { getCurrentUser, signIn, signUp, signOut } from '@/lib/auth'

interface User {
  id: string
  email: string
  name: string
}

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .finally(() => setLoading(false))
  }, [])

  return {
    user,
    loading,
    signIn,
    signUp,
    signOut,
  }
}
```

---

## Backend: JWT Verification

### 1. Installation

```bash
cd backend
uv pip install python-jose[cryptography] passlib[bcrypt]
```

### 2. JWT Verification Middleware

```python
# backend/app/middleware/auth.py
from fastapi import Depends, HTTPException, Header
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
if not SECRET_KEY:
    raise ValueError("BETTER_AUTH_SECRET environment variable not set")

ALGORITHM = "HS256"

async def verify_jwt(authorization: str = Header(None)) -> str:
    """
    Verify JWT token and return user_id from payload.

    Args:
        authorization: Authorization header with "Bearer <token>"

    Returns:
        str: User ID from JWT payload

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing authorization header"
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid authorization header format. Expected: Bearer <token>"
        )

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload"
            )

        return user_id

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token has expired"
        )
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
```

### 3. Usage in Routes

```python
# backend/app/routes/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from app.middleware.auth import verify_jwt
from sqlmodel import Session
from app.db import get_session

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(verify_jwt),
    session: Session = Depends(get_session)
):
    # Validate user_id matches authenticated user
    if user_id != authenticated_user_id:
        raise HTTPException(
            status_code=403,
            detail="Access denied: User ID mismatch"
        )

    # Proceed with query (user isolation enforced)
    # ...
```

---

## Shared Secret Configuration

### Environment Variables

**Backend (.env)**:
```bash
BETTER_AUTH_SECRET=your-32-character-secret-key-here-change-in-production
```

**Frontend (.env.local)**:
```bash
BETTER_AUTH_SECRET=your-32-character-secret-key-here-change-in-production
```

### Generating Secure Secret

```bash
# Generate 32-character random secret
openssl rand -base64 32

# Example output:
# k7J8mN9pQ2rS3tU4vW5xY6zA7bC8dE9f
```

**IMPORTANT**:
- Secret MUST be at least 32 characters
- Secret MUST be the same in frontend and backend
- Secret MUST NOT be committed to git (use .env files)
- Use different secrets for development and production

---

## Frontend: API Client with JWT

### API Client with Auto-Attach JWT

```typescript
// frontend/lib/api.ts
import { getAuthToken } from './auth'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class APIClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await getAuthToken()

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    // Attach JWT Bearer token
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      if (response.status === 401) {
        // Token expired or invalid - redirect to signin
        window.location.href = '/auth/signin'
        throw new Error('Authentication required')
      }

      const error = await response.json().catch(() => ({
        detail: 'Unknown error'
      }))
      throw new Error(error.detail || `HTTP ${response.status}`)
    }

    return response.json()
  }

  // Task endpoints automatically include JWT
  async getTasks(userId: string): Promise<Task[]> {
    return this.request<Task[]>(`/api/${userId}/tasks`)
  }

  async createTask(userId: string, data: TaskCreate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // ... other methods
}

export const api = new APIClient()
```

---

## User Session Persistence

### Frontend Session Check

```typescript
// frontend/app/layout.tsx
'use client'

import { useEffect, useState } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import { getCurrentUser } from '@/lib/auth'

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const router = useRouter()
  const pathname = usePathname()
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check authentication on page load
    getCurrentUser()
      .then((user) => {
        if (!user && !pathname.startsWith('/auth')) {
          // Not authenticated and not on auth page → redirect
          router.push('/auth/signin')
        }
        setLoading(false)
      })
  }, [pathname, router])

  if (loading) {
    return <div>Loading...</div>
  }

  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
```

### Protected Routes (Middleware)

```typescript
// frontend/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { getCurrentUser } from '@/lib/auth'

export async function middleware(request: NextRequest) {
  const user = await getCurrentUser()

  // Protect all routes except /auth/*
  if (!user && !request.nextUrl.pathname.startsWith('/auth')) {
    return NextResponse.redirect(new URL('/auth/signin', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     */
    '/((?!_next/static|_next/image|favicon.ico).*)',
  ],
}
```

---

## JWT Token Structure

### JWT Payload

```json
{
  "user_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
  "email": "user@example.com",
  "exp": 1734268800,  // Expiration timestamp (Unix epoch)
  "iat": 1733664000   // Issued at timestamp
}
```

### Token Expiry

- **Default Expiry**: 7 days (configurable)
- **Refresh Strategy**: User must re-login after expiry
- **Backend Validation**: Checks `exp` field in JWT payload

---

## Security Best Practices

### Password Security

- ✅ Passwords hashed with bcrypt (cost factor: 12)
- ✅ Minimum password length: 8 characters (configurable)
- ✅ Password never sent to backend in plaintext (HTTPS)
- ✅ Password hash never returned in API responses

### Token Security

- ✅ JWT signed with HS256 algorithm
- ✅ Secret key minimum 32 characters
- ✅ Token includes expiry time
- ✅ Token verified on every backend request
- ✅ Invalid/expired tokens rejected with 401

### Transport Security

- ✅ HTTPS required in production
- ✅ Cookies use HttpOnly, Secure, SameSite flags
- ✅ CORS properly configured (no wildcards)
- ✅ Authorization header used for API requests

### User Isolation

- ✅ Every API request validates user_id
- ✅ Database queries filter by authenticated user_id
- ✅ Cross-user data access prevented (403 Forbidden)
- ✅ Non-existent tasks return 404 (not 403 to prevent enumeration)

---

## Error Handling

### Authentication Errors

| HTTP Status | Scenario | Response |
|-------------|----------|----------|
| 401 Unauthorized | Missing Authorization header | `{"detail": "Missing authorization header"}` |
| 401 Unauthorized | Invalid token format | `{"detail": "Invalid authorization header format"}` |
| 401 Unauthorized | Expired token | `{"detail": "Token has expired"}` |
| 401 Unauthorized | Invalid signature | `{"detail": "Invalid token"}` |
| 403 Forbidden | User ID mismatch | `{"detail": "Access denied"}` |

### Frontend Error Handling

```typescript
// Automatic redirect on 401
if (response.status === 401) {
  window.location.href = '/auth/signin'
  throw new Error('Authentication required')
}
```

---

## Testing

### Backend Tests (pytest)

```python
# backend/tests/test_auth.py
import pytest
from jose import jwt
from app.middleware.auth import verify_jwt

def test_valid_jwt_token():
    token = jwt.encode(
        {"user_id": "test-user-id"},
        SECRET_KEY,
        algorithm="HS256"
    )
    user_id = await verify_jwt(f"Bearer {token}")
    assert user_id == "test-user-id"

def test_missing_authorization_header():
    with pytest.raises(HTTPException) as exc:
        await verify_jwt(None)
    assert exc.value.status_code == 401

def test_expired_token():
    # Create token with past expiry
    expired_token = jwt.encode(
        {"user_id": "test-user-id", "exp": 0},
        SECRET_KEY,
        algorithm="HS256"
    )
    with pytest.raises(HTTPException) as exc:
        await verify_jwt(f"Bearer {expired_token}")
    assert exc.value.status_code == 401
    assert "expired" in exc.value.detail.lower()
```

---

## Acceptance Criteria

### Frontend
- [ ] Better Auth installed and configured
- [ ] Sign up form creates user and issues JWT
- [ ] Sign in form authenticates and issues JWT
- [ ] JWT stored in HTTP-only cookie (or localStorage)
- [ ] All API requests include JWT in Authorization header
- [ ] 401 responses redirect to signin page
- [ ] User session persists after page refresh
- [ ] Sign out clears session and redirects

### Backend
- [ ] JWT verification middleware implemented
- [ ] All task endpoints require authentication
- [ ] User ID in URL validated against JWT user_id
- [ ] Invalid tokens return 401 Unauthorized
- [ ] User ID mismatch returns 403 Forbidden
- [ ] Shared secret loaded from environment variable
- [ ] Token expiry validated (exp field)
- [ ] User isolation enforced on all queries

### Security
- [ ] BETTER_AUTH_SECRET min 32 characters
- [ ] Secret not committed to git (.env in .gitignore)
- [ ] HTTPS enforced in production
- [ ] CORS configured (no wildcards)
- [ ] Passwords hashed (bcrypt)
- [ ] JWT signed with HS256

---

**Status**: ✅ Complete
**Next**: Create UI components specification
