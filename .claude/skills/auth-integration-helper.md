# Auth Integration Helper Skill

## Purpose
Set up complete authentication flow using Better Auth (frontend) + JWT verification (backend) for secure full-stack applications.

## Inputs
- **Authentication Requirements**: Login/signup flows, social auth, email verification
- **User Model**: Fields to store (email, name, profile, etc.)
- **JWT Configuration**: Secret, expiration, claims
- **Protected Routes**: Which endpoints/pages require authentication

## Outputs
- Better Auth configuration (frontend)
- JWT middleware for FastAPI (backend)
- Login/signup UI components
- Session management
- Protected route implementation
- Environment variables setup

## Instructions

You are an authentication integration specialist. When setting up auth:

### 1. Architecture Overview

```
┌─────────────────┐         ┌─────────────────┐
│   Frontend      │         │    Backend      │
│   (Next.js)     │         │   (FastAPI)     │
│                 │         │                 │
│  Better Auth    │◄───────►│  JWT Verify     │
│  - Signup       │  HTTP   │  - Protected    │
│  - Login        │  + JWT  │    Routes       │
│  - Session      │  Token  │  - User Info    │
└─────────────────┘         └─────────────────┘
```

**Flow:**
1. User signs up/logs in → Better Auth (frontend)
2. Better Auth creates session + issues JWT token
3. Frontend includes JWT in `Authorization: Bearer <token>` header
4. Backend verifies JWT signature → extracts user info
5. Backend checks user_id in URL matches JWT user_id
6. Return user-specific data

### 2. Better Auth Setup (Frontend)

**Installation:**
```bash
npm install better-auth
```

**Configuration File: `lib/auth.ts`**
```typescript
import { betterAuth } from "better-auth"
import { nextCookies } from "better-auth/next-js"

export const auth = betterAuth({
  // Database (stores users and sessions)
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL!,
  },

  // Email/password authentication
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },

  // JWT configuration
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 60 * 24 * 7, // 7 days
    },
  },

  // Secret for signing tokens
  secret: process.env.BETTER_AUTH_SECRET!,

  // Plugins
  plugins: [nextCookies()],
})

export type Session = typeof auth.$Infer.Session
```

**Environment Variables: `.env.local`**
```env
# Shared secret (MUST be same in frontend and backend)
BETTER_AUTH_SECRET=your-secret-key-min-32-chars

# Database URL (Neon PostgreSQL)
DATABASE_URL=postgresql://user:password@host/db

# Application URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**API Route: `app/api/auth/[...all]/route.ts`**
```typescript
import { auth } from "@/lib/auth"

export const { GET, POST } = auth.handler
```

### 3. Better Auth Client (Frontend)

**Client Setup: `lib/auth-client.ts`**
```typescript
import { createAuthClient } from "better-auth/client"

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL!,
})

export const {
  signIn,
  signUp,
  signOut,
  useSession,
} = authClient
```

### 4. Auth UI Components (Frontend)

**Signup Component:**
```typescript
'use client'

import { FC, useState } from 'react'
import { useRouter } from 'next/navigation'
import { signUp } from '@/lib/auth-client'

export const SignupForm: FC = () => {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await signUp.email({
        email,
        password,
        name,
      })
      router.push('/dashboard')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Signup failed')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <div>
        <label htmlFor="name" className="block text-sm font-medium">
          Name
        </label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          minLength={8}
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Signing up...' : 'Sign Up'}
      </button>
    </form>
  )
}
```

**Login Component:**
```typescript
'use client'

import { FC, useState } from 'react'
import { useRouter } from 'next/navigation'
import { signIn } from '@/lib/auth-client'

export const LoginForm: FC = () => {
  const router = useRouter()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setIsLoading(true)

    try {
      await signIn.email({
        email,
        password,
      })
      router.push('/dashboard')
    } catch (err) {
      setError('Invalid email or password')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          className="mt-1 w-full px-3 py-2 border rounded-md"
        />
      </div>

      {error && (
        <div className="text-red-600 text-sm">{error}</div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full py-2 px-4 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isLoading ? 'Signing in...' : 'Sign In'}
      </button>
    </form>
  )
}
```

**Session Hook (Protected Pages):**
```typescript
'use client'

import { useSession } from '@/lib/auth-client'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function useRequireAuth() {
  const { data: session, isPending } = useSession()
  const router = useRouter()

  useEffect(() => {
    if (!isPending && !session) {
      router.push('/login')
    }
  }, [session, isPending, router])

  return { session, isPending }
}

// Usage in protected page
export default function DashboardPage() {
  const { session, isPending } = useRequireAuth()

  if (isPending) return <div>Loading...</div>
  if (!session) return null

  return <div>Welcome, {session.user.name}!</div>
}
```

### 5. JWT Middleware (Backend - FastAPI)

**Installation:**
```bash
pip install pyjwt python-jose[cryptography]
```

**JWT Utilities: `backend/auth.py`**
```python
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import os

# Security scheme
security = HTTPBearer()

# Secret key (MUST match frontend BETTER_AUTH_SECRET)
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET")
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Verify JWT token and return decoded payload

    Args:
        credentials: Bearer token from Authorization header

    Returns:
        dict: Decoded token payload with user info

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token_payload: dict = Security(verify_token)) -> dict:
    """
    Extract current user from verified token

    Args:
        token_payload: Decoded JWT payload

    Returns:
        dict: User information (id, email, etc.)

    Raises:
        HTTPException: If user info missing from token
    """
    user_id = token_payload.get("sub")  # Better Auth stores user ID in 'sub'
    email = token_payload.get("email")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    return {
        "id": user_id,
        "email": email,
    }
```

**Protected Endpoint Example:**
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from .auth import get_current_user
from .database import get_db
from .models import Task

router = APIRouter(prefix="/api", tags=["tasks"])

@router.get("/{user_id}/tasks")
async def get_user_tasks(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all tasks for a user (protected route)

    Security:
    - Requires valid JWT token
    - User can only access their own tasks
    """
    # Verify user is accessing their own data
    if current_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this user's tasks"
        )

    # Query tasks
    statement = select(Task).where(Task.user_id == user_id)
    tasks = db.exec(statement).all()

    return tasks
```

### 6. API Client with Auth (Frontend)

**API Client: `lib/api-client.ts`**
```typescript
import { authClient } from './auth-client'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function getAuthToken(): Promise<string | null> {
  const session = await authClient.getSession()
  return session?.session.token || null
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken()

  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  }

  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Token expired or invalid
      window.location.href = '/login'
    }
    throw new Error(`API error: ${response.statusText}`)
  }

  return response.json()
}

// Usage examples
export const api = {
  getTasks: (userId: string) =>
    apiRequest<Task[]>(`/api/${userId}/tasks`),

  createTask: (userId: string, data: CreateTaskInput) =>
    apiRequest<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  deleteTask: (userId: string, taskId: number) =>
    apiRequest(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    }),
}
```

### 7. Environment Variables Checklist

**Frontend (.env.local):**
```env
BETTER_AUTH_SECRET=same-secret-as-backend
DATABASE_URL=postgresql://...
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Backend (.env):**
```env
BETTER_AUTH_SECRET=same-secret-as-frontend
DATABASE_URL=postgresql://...
```

### 8. Security Best Practices

- [ ] Use HTTPS in production
- [ ] Store JWT secret in environment variables (never in code)
- [ ] Use strong secrets (minimum 32 characters)
- [ ] Implement token expiration (7 days recommended)
- [ ] Verify user_id in URL matches JWT user_id
- [ ] Hash passwords (Better Auth does this automatically)
- [ ] Use httpOnly cookies for session storage
- [ ] Implement rate limiting on auth endpoints
- [ ] Validate email addresses
- [ ] Implement password strength requirements

## Testing Auth Flow

```typescript
// Test signup
await signUp.email({
  email: 'test@example.com',
  password: 'SecurePass123',
  name: 'Test User',
})

// Test login
await signIn.email({
  email: 'test@example.com',
  password: 'SecurePass123',
})

// Test protected request
const tasks = await api.getTasks('user-id-123')
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| "Invalid token" error | Verify BETTER_AUTH_SECRET matches in both apps |
| CORS errors | Configure CORS in FastAPI to allow frontend origin |
| Token not included | Check API client adds Authorization header |
| User can see other's data | Verify user_id check in backend endpoints |

## Notes
- Better Auth automatically handles password hashing
- JWT tokens are signed, not encrypted (don't put secrets in claims)
- Token expiration prevents indefinite access
- Use HTTPS in production to prevent token interception
- Consider refresh tokens for longer sessions
- Implement logout by clearing session on frontend
