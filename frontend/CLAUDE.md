# Frontend Development Guidelines - Phase II

This file provides context-specific instructions for the Next.js 16 frontend application.

## Stack Overview

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth with JWT
- **State Management**: React Context / Zustand (minimal)
- **Data Fetching**: @tanstack/react-query or SWR
- **Validation**: Zod
- **Icons**: Lucide React

## Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Root layout with providers
│   ├── page.tsx                  # Home page (landing/dashboard)
│   ├── globals.css               # Global styles + Tailwind imports
│   ├── tasks/                    # Task management pages
│   │   ├── page.tsx              # Task list page
│   │   ├── new/page.tsx          # Create new task page
│   │   └── [id]/                 # Dynamic task routes
│   │       ├── page.tsx          # Task detail/edit page
│   │       └── loading.tsx       # Loading state
│   ├── auth/                     # Authentication pages
│   │   ├── signin/page.tsx       # Sign in page
│   │   └── signup/page.tsx       # Sign up page
│   └── error.tsx                 # Error boundary
├── components/                   # Reusable UI components
│   ├── TaskList.tsx              # Task list component
│   ├── TaskCard.tsx              # Individual task card
│   ├── TaskForm.tsx              # Create/edit task form
│   ├── Header.tsx                # Navigation header
│   ├── Footer.tsx                # Footer component
│   └── ui/                       # shadcn/ui components (optional)
│       ├── button.tsx
│       ├── input.tsx
│       └── card.tsx
├── lib/                          # Utilities and helpers
│   ├── api.ts                    # API client (fetch wrapper)
│   ├── auth.ts                   # Better Auth configuration
│   ├── utils.ts                  # Helper functions
│   └── validators.ts             # Zod schemas
├── types/                        # TypeScript type definitions
│   ├── task.ts                   # Task-related types
│   └── api.ts                    # API response types
├── hooks/                        # Custom React hooks
│   ├── useTasks.ts               # Task data fetching hook
│   └── useAuth.ts                # Authentication hook
├── public/                       # Static assets
│   └── images/
├── .env.local                    # Environment variables (gitignored)
├── .env.local.example            # Environment template
├── next.config.ts                # Next.js configuration
├── tailwind.config.ts            # Tailwind CSS configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Dependencies
```

## Architecture Patterns

### Server vs Client Components

**Default: Server Components**

Use server components by default for better performance. Only use `'use client'` when needed for:

- Event handlers (onClick, onChange, etc.)
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect, useContext)
- Third-party libraries that require client-side rendering

**Example:**

```tsx
// app/tasks/page.tsx (Server Component - default)
import { TaskList } from '@/components/TaskList'

export default async function TasksPage() {
  // Can fetch data directly in server component
  return (
    <div>
      <h1>My Tasks</h1>
      <TaskList />
    </div>
  )
}
```

```tsx
// components/TaskList.tsx (Client Component - needs interactivity)
'use client'

import { useState } from 'react'
import { useTasks } from '@/hooks/useTasks'

export function TaskList() {
  const [filter, setFilter] = useState('all')
  const { tasks, isLoading } = useTasks(filter)

  return (
    <div>
      <select onChange={(e) => setFilter(e.target.value)}>
        <option value="all">All</option>
        <option value="pending">Pending</option>
        <option value="completed">Completed</option>
      </select>
      {/* Task list rendering */}
    </div>
  )
}
```

## API Client Setup

### Centralized API Client

```typescript
// lib/api.ts
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

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'Unknown error' }))
      throw new Error(error.message || `HTTP ${response.status}`)
    }

    return response.json()
  }

  // Task endpoints
  async getTasks(userId: string): Promise<Task[]> {
    return this.request<Task[]>(`/api/${userId}/tasks`)
  }

  async createTask(userId: string, data: TaskCreate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async updateTask(userId: string, taskId: number, data: TaskUpdate): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async deleteTask(userId: string, taskId: number): Promise<void> {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: 'DELETE',
    })
  }

  async toggleTaskComplete(userId: string, taskId: number): Promise<Task> {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: 'PATCH',
    })
  }
}

export const api = new APIClient()
```

## Better Auth Setup

### Authentication Configuration

```typescript
// lib/auth.ts
import { createAuthClient } from 'better-auth/client'

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL || 'http://localhost:3000',
  // Better Auth will handle JWT internally
})

// Helper to get current auth token
export async function getAuthToken(): Promise<string | null> {
  const session = await authClient.getSession()
  return session?.accessToken || null
}

// Helper to get current user
export async function getCurrentUser() {
  const session = await authClient.getSession()
  return session?.user || null
}
```

### Authentication Hook

```typescript
// hooks/useAuth.ts
'use client'

import { useEffect, useState } from 'react'
import { authClient, getCurrentUser } from '@/lib/auth'

export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .finally(() => setLoading(false))
  }, [])

  const signIn = async (email: string, password: string) => {
    await authClient.signIn.email({ email, password })
    const user = await getCurrentUser()
    setUser(user)
  }

  const signUp = async (email: string, password: string, name: string) => {
    await authClient.signUp.email({ email, password, name })
    const user = await getCurrentUser()
    setUser(user)
  }

  const signOut = async () => {
    await authClient.signOut()
    setUser(null)
  }

  return { user, loading, signIn, signUp, signOut }
}
```

## Data Fetching with React Query

### Setup Provider

```tsx
// app/layout.tsx
'use client'

import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <html lang="en">
      <body>
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
      </body>
    </html>
  )
}
```

### Custom Hook for Tasks

```typescript
// hooks/useTasks.ts
'use client'

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '@/lib/api'
import { useAuth } from './useAuth'

export function useTasks(filter: 'all' | 'pending' | 'completed' = 'all') {
  const { user } = useAuth()
  const queryClient = useQueryClient()

  const { data: tasks, isLoading, error } = useQuery({
    queryKey: ['tasks', user?.id, filter],
    queryFn: () => api.getTasks(user!.id),
    enabled: !!user,
  })

  const createMutation = useMutation({
    mutationFn: (data: TaskCreate) => api.createTask(user!.id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ taskId, data }: { taskId: number; data: TaskUpdate }) =>
      api.updateTask(user!.id, taskId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (taskId: number) => api.deleteTask(user!.id, taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const toggleCompleteMutation = useMutation({
    mutationFn: (taskId: number) => api.toggleTaskComplete(user!.id, taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  return {
    tasks,
    isLoading,
    error,
    createTask: createMutation.mutate,
    updateTask: updateMutation.mutate,
    deleteTask: deleteMutation.mutate,
    toggleComplete: toggleCompleteMutation.mutate,
  }
}
```

## TypeScript Types

### Task Types

```typescript
// types/task.ts
export interface Task {
  id: number
  user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
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

## Form Validation with Zod

```typescript
// lib/validators.ts
import { z } from 'zod'

export const taskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  description: z.string().max(1000, 'Description too long').optional(),
})

export type TaskFormData = z.infer<typeof taskSchema>
```

## Styling with Tailwind CSS

### Tailwind Configuration

```typescript
// tailwind.config.ts
import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
export default config
```

### Global Styles

```css
/* app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
  }

  body {
    @apply bg-background text-foreground;
  }
}
```

## Component Best Practices

### Example: Task Card Component

```tsx
// components/TaskCard.tsx
'use client'

import { Task } from '@/types/task'
import { Trash2, Edit, Check } from 'lucide-react'

interface TaskCardProps {
  task: Task
  onToggle: (id: number) => void
  onDelete: (id: number) => void
  onEdit: (id: number) => void
}

export function TaskCard({ task, onToggle, onDelete, onEdit }: TaskCardProps) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : ''}`}>
            {task.title}
          </h3>
          {task.description && (
            <p className="text-sm text-gray-600 mt-1">{task.description}</p>
          )}
          <p className="text-xs text-gray-400 mt-2">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onToggle(task.id)}
            className="p-2 hover:bg-green-100 rounded"
            aria-label="Toggle complete"
          >
            <Check className={task.completed ? 'text-green-600' : 'text-gray-400'} size={20} />
          </button>
          <button
            onClick={() => onEdit(task.id)}
            className="p-2 hover:bg-blue-100 rounded"
            aria-label="Edit task"
          >
            <Edit className="text-blue-600" size={20} />
          </button>
          <button
            onClick={() => onDelete(task.id)}
            className="p-2 hover:bg-red-100 rounded"
            aria-label="Delete task"
          >
            <Trash2 className="text-red-600" size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}
```

## Error Handling

### Error Boundary

```tsx
// app/error.tsx
'use client'

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string }
  reset: () => void
}) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h2 className="text-2xl font-bold mb-4">Something went wrong!</h2>
      <p className="text-gray-600 mb-4">{error.message}</p>
      <button
        onClick={reset}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
      >
        Try again
      </button>
    </div>
  )
}
```

## Development Workflow

### Running Locally

```bash
# Install dependencies
npm install

# Create .env.local with API_URL and BETTER_AUTH_SECRET

# Run development server
npm run dev

# Open http://localhost:3000
```

### Build for Production

```bash
# Type check
npm run type-check

# Build
npm run build

# Start production server
npm start
```

## Code Style Guidelines

- **TypeScript**: Strict mode enabled, all types explicit
- **Component Names**: PascalCase (e.g., TaskCard)
- **File Names**: PascalCase for components, camelCase for utilities
- **Props**: Always define interface for component props
- **Hooks**: Prefix with `use` (e.g., useTasks)
- **Constants**: UPPER_SNAKE_CASE
- **CSS**: Tailwind utility classes only (no inline styles)

## Accessibility Checklist

- [ ] Use semantic HTML elements
- [ ] Add ARIA labels to buttons and inputs
- [ ] Ensure keyboard navigation works
- [ ] Test with screen readers
- [ ] Maintain proper color contrast ratios
- [ ] Add loading and error states

## References

- **Next.js Docs**: https://nextjs.org/docs
- **React Query Docs**: https://tanstack.com/query/latest
- **Better Auth Docs**: https://www.better-auth.com/docs
- **Tailwind CSS Docs**: https://tailwindcss.com/docs
- **Constitution**: `.specify/memory/constitution.md`
- **UI Specs**: `specs/phase-2/ui/`
