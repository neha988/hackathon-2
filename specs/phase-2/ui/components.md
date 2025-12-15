# UI Components Specification

**Version**: 1.0.0
**Date**: 2025-12-15
**Framework**: Next.js 16 + React 19 + TypeScript + Tailwind CSS

---

## Overview

This specification defines all UI components for the Todo application frontend, including component structure, props interfaces, styling, and behavior.

**Design Principles**:
- Component-based architecture (reusable, composable)
- Server Components by default (use 'use client' only when needed)
- TypeScript strict mode (all props typed)
- Tailwind CSS for styling (no inline styles)
- Accessible (ARIA labels, keyboard navigation)
- Responsive (mobile-first approach)

---

## Component Architecture

```
frontend/
├── app/                          # Pages (Next.js App Router)
│   ├── layout.tsx                # Root layout (providers)
│   ├── page.tsx                  # Home/landing page
│   ├── tasks/                    # Task pages
│   │   ├── page.tsx              # Task list page (TaskList component)
│   │   ├── new/page.tsx          # Create task page (TaskForm component)
│   │   └── [id]/page.tsx         # Edit task page (TaskForm component)
│   └── auth/                     # Auth pages
│       ├── signin/page.tsx       # Sign in (AuthForm component)
│       └── signup/page.tsx       # Sign up (AuthForm component)
├── components/                   # Reusable components
│   ├── TaskList.tsx              # List of tasks (client component)
│   ├── TaskCard.tsx              # Individual task card
│   ├── TaskForm.tsx              # Create/edit task form
│   ├── AuthForm.tsx              # Sign in/sign up form
│   ├── Header.tsx                # Navigation header
│   ├── Footer.tsx                # Footer
│   └── ui/                       # Base UI components
│       ├── Button.tsx
│       ├── Input.tsx
│       └── Card.tsx
└── hooks/                        # Custom hooks
    ├── useTasks.ts               # Task data fetching
    └── useAuth.ts                # Authentication
```

---

## Component Inventory

| Component | Type | Purpose | Interactive |
|-----------|------|---------|-------------|
| **TaskList** | Client | Display list of tasks with filters | Yes |
| **TaskCard** | Client | Individual task card with actions | Yes |
| **TaskForm** | Client | Create/edit task form | Yes |
| **AuthForm** | Client | Sign in/sign up form | Yes |
| **Header** | Server | Navigation with user menu | Partial |
| **Footer** | Server | Footer with links | No |
| **Button** | Server | Reusable button component | No |
| **Input** | Server | Reusable input component | No |
| **Card** | Server | Card container | No |

---

## Component Specifications

### 1. TaskList Component

**Purpose**: Display list of tasks with filtering and sorting

**File**: `frontend/components/TaskList.tsx`

**Props**:
```typescript
interface TaskListProps {
  userId: string  // Current user ID
}
```

**State**:
- `filter`: "all" | "pending" | "completed"
- `sort`: "created" | "updated" | "title"
- `order`: "asc" | "desc"

**Implementation**:
```tsx
'use client'

import { useState } from 'react'
import { useTasks } from '@/hooks/useTasks'
import { TaskCard } from './TaskCard'

interface TaskListProps {
  userId: string
}

export function TaskList({ userId }: TaskListProps) {
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all')
  const [sort, setSort] = useState<'created' | 'updated' | 'title'>('created')

  const {
    tasks,
    isLoading,
    error,
    deleteTask,
    toggleComplete,
  } = useTasks(userId, filter, sort)

  if (isLoading) {
    return <div className="text-center py-8">Loading tasks...</div>
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        Error loading tasks: {error.message}
      </div>
    )
  }

  if (!tasks || tasks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        {filter === 'all'
          ? 'No tasks yet. Create your first task!'
          : `No ${filter} tasks.`}
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {/* Filters */}
      <div className="flex gap-4 mb-6">
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value as any)}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="all">All Tasks</option>
          <option value="pending">Pending</option>
          <option value="completed">Completed</option>
        </select>

        <select
          value={sort}
          onChange={(e) => setSort(e.target.value as any)}
          className="px-4 py-2 border rounded-lg"
        >
          <option value="created">Sort by Created</option>
          <option value="updated">Sort by Updated</option>
          <option value="title">Sort by Title</option>
        </select>
      </div>

      {/* Task List */}
      <div className="space-y-3">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onToggle={() => toggleComplete(task.id)}
            onDelete={() => deleteTask(task.id)}
          />
        ))}
      </div>
    </div>
  )
}
```

**Styling**: Tailwind CSS utility classes
**Accessibility**: Select elements have labels (implicit)

---

### 2. TaskCard Component

**Purpose**: Display individual task with action buttons

**File**: `frontend/components/TaskCard.tsx`

**Props**:
```typescript
import { Task } from '@/types/task'

interface TaskCardProps {
  task: Task
  onToggle: () => void
  onDelete: () => void
}
```

**Implementation**:
```tsx
'use client'

import { Task } from '@/types/task'
import { Trash2, Edit, Check } from 'lucide-react'
import Link from 'next/link'

interface TaskCardProps {
  task: Task
  onToggle: () => void
  onDelete: () => void
}

export function TaskCard({ task, onToggle, onDelete }: TaskCardProps) {
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-white">
      <div className="flex items-start justify-between gap-4">
        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-medium truncate ${
              task.completed
                ? 'line-through text-gray-500'
                : 'text-gray-900'
            }`}
          >
            {task.title}
          </h3>

          {task.description && (
            <p className="text-sm text-gray-600 mt-1 line-clamp-2">
              {task.description}
            </p>
          )}

          <div className="flex items-center gap-4 mt-2 text-xs text-gray-400">
            <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
            {task.updated_at !== task.created_at && (
              <span>Updated: {new Date(task.updated_at).toLocaleDateString()}</span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-2 flex-shrink-0">
          <button
            onClick={onToggle}
            className={`p-2 rounded hover:bg-green-100 transition-colors ${
              task.completed ? 'text-green-600' : 'text-gray-400'
            }`}
            aria-label={task.completed ? 'Mark as incomplete' : 'Mark as complete'}
          >
            <Check size={20} />
          </button>

          <Link
            href={`/tasks/${task.id}`}
            className="p-2 rounded hover:bg-blue-100 transition-colors text-blue-600"
            aria-label="Edit task"
          >
            <Edit size={20} />
          </Link>

          <button
            onClick={onDelete}
            className="p-2 rounded hover:bg-red-100 transition-colors text-red-600"
            aria-label="Delete task"
          >
            <Trash2 size={20} />
          </button>
        </div>
      </div>
    </div>
  )
}
```

**Styling**:
- Card with border and shadow on hover
- Completed tasks: line-through, gray text
- Icon buttons with colored backgrounds on hover
- Responsive layout (stacks on mobile)

**Accessibility**:
- All buttons have `aria-label`
- Keyboard navigable (Tab key)
- Visual feedback on hover/focus

---

### 3. TaskForm Component

**Purpose**: Create or edit task

**File**: `frontend/components/TaskForm.tsx`

**Props**:
```typescript
interface TaskFormProps {
  userId: string
  taskId?: number  // undefined for create, number for edit
  initialData?: {
    title: string
    description: string | null
  }
  onSuccess?: () => void
}
```

**Implementation**:
```tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useTasks } from '@/hooks/useTasks'
import { Button } from './ui/Button'
import { Input } from './ui/Input'

interface TaskFormProps {
  userId: string
  taskId?: number
  initialData?: {
    title: string
    description: string | null
  }
  onSuccess?: () => void
}

export function TaskForm({
  userId,
  taskId,
  initialData,
  onSuccess,
}: TaskFormProps) {
  const router = useRouter()
  const { createTask, updateTask } = useTasks(userId)

  const [title, setTitle] = useState(initialData?.title || '')
  const [description, setDescription] = useState(initialData?.description || '')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    if (!title.trim()) {
      setError('Title is required')
      return
    }

    if (title.length > 200) {
      setError('Title must be 200 characters or less')
      return
    }

    if (description.length > 1000) {
      setError('Description must be 1000 characters or less')
      return
    }

    setLoading(true)

    try {
      if (taskId) {
        // Update existing task
        await updateTask(taskId, {
          title: title.trim(),
          description: description.trim() || null,
        })
      } else {
        // Create new task
        await createTask({
          title: title.trim(),
          description: description.trim() || null,
        })
      }

      onSuccess?.()
      router.push('/tasks')
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-2xl">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <Input
          id="title"
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title"
          maxLength={200}
          required
          disabled={loading}
        />
        <p className="text-xs text-gray-500 mt-1">{title.length}/200 characters</p>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description"
          maxLength={1000}
          rows={4}
          disabled={loading}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <p className="text-xs text-gray-500 mt-1">{description.length}/1000 characters</p>
      </div>

      <div className="flex gap-3">
        <Button type="submit" disabled={loading}>
          {loading ? 'Saving...' : taskId ? 'Update Task' : 'Create Task'}
        </Button>
        <Button
          type="button"
          variant="secondary"
          onClick={() => router.back()}
          disabled={loading}
        >
          Cancel
        </Button>
      </div>
    </form>
  )
}
```

**Validation**:
- Title required, 1-200 characters
- Description optional, max 1000 characters
- Character count displayed
- Client-side validation before submission

---

### 4. AuthForm Component

**Purpose**: Sign in or sign up form

**File**: `frontend/components/AuthForm.tsx`

**Props**:
```typescript
interface AuthFormProps {
  mode: 'signin' | 'signup'
}
```

**Implementation**:
```tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '@/hooks/useAuth'
import { Button } from './ui/Button'
import { Input } from './ui/Input'
import Link from 'next/link'

interface AuthFormProps {
  mode: 'signin' | 'signup'
}

export function AuthForm({ mode }: AuthFormProps) {
  const router = useRouter()
  const { signIn, signUp } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (mode === 'signin') {
        const result = await signIn(email, password)
        if (!result.success) {
          setError(result.error || 'Sign in failed')
          return
        }
      } else {
        const result = await signUp(email, password, name)
        if (!result.success) {
          setError(result.error || 'Sign up failed')
          return
        }
      }

      router.push('/tasks')
    } catch (err: any) {
      setError(err.message || 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-8">
      <h2 className="text-2xl font-bold text-center mb-6">
        {mode === 'signin' ? 'Sign In' : 'Sign Up'}
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {mode === 'signup' && (
          <div>
            <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-1">
              Name
            </label>
            <Input
              id="name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              disabled={loading}
            />
          </div>
        )}

        <div>
          <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <Input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>

        <div>
          <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
            Password
          </label>
          <Input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            disabled={loading}
          />
        </div>

        <Button type="submit" className="w-full" disabled={loading}>
          {loading ? 'Please wait...' : mode === 'signin' ? 'Sign In' : 'Sign Up'}
        </Button>
      </form>

      <p className="text-center mt-4 text-sm text-gray-600">
        {mode === 'signin' ? (
          <>
            Don't have an account?{' '}
            <Link href="/auth/signup" className="text-blue-600 hover:underline">
              Sign Up
            </Link>
          </>
        ) : (
          <>
            Already have an account?{' '}
            <Link href="/auth/signin" className="text-blue-600 hover:underline">
              Sign In
            </Link>
          </>
        )}
      </p>
    </div>
  )
}
```

---

### 5. Header Component

**Purpose**: Navigation bar with user menu

**File**: `frontend/components/Header.tsx`

**Implementation**:
```tsx
import Link from 'next/link'
import { useAuth } from '@/hooks/useAuth'

export function Header() {
  const { user, signOut } = useAuth()

  return (
    <header className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between">
        <Link href="/" className="text-2xl font-bold text-blue-600">
          Todo App
        </Link>

        <nav>
          {user ? (
            <div className="flex items-center gap-4">
              <Link href="/tasks" className="text-gray-700 hover:text-blue-600">
                My Tasks
              </Link>
              <Link href="/tasks/new" className="text-gray-700 hover:text-blue-600">
                New Task
              </Link>
              <span className="text-gray-600">{user.email}</span>
              <button
                onClick={signOut}
                className="text-gray-700 hover:text-red-600"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <div className="flex gap-4">
              <Link href="/auth/signin" className="text-gray-700 hover:text-blue-600">
                Sign In
              </Link>
              <Link href="/auth/signup" className="text-gray-700 hover:text-blue-600">
                Sign Up
              </Link>
            </div>
          )}
        </nav>
      </div>
    </header>
  )
}
```

---

### 6. Base UI Components

#### Button Component

**File**: `frontend/components/ui/Button.tsx`

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
  children: React.ReactNode
}

export function Button({
  variant = 'primary',
  children,
  className = '',
  ...props
}: ButtonProps) {
  const baseStyles = 'px-4 py-2 rounded-lg font-medium transition-colors disabled:opacity-50'
  const variantStyles = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700',
  }

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${className}`}
      {...props}
    >
      {children}
    </button>
  )
}
```

#### Input Component

**File**: `frontend/components/ui/Input.tsx`

```tsx
interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {}

export function Input({ className = '', ...props }: InputProps) {
  return (
    <input
      className={`w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 ${className}`}
      {...props}
    />
  )
}
```

---

## Pages (App Router)

### Task List Page

**File**: `frontend/app/tasks/page.tsx`

```tsx
import { TaskList } from '@/components/TaskList'
import { getCurrentUser } from '@/lib/auth'
import { redirect } from 'next/navigation'
import Link from 'next/link'

export default async function TasksPage() {
  const user = await getCurrentUser()

  if (!user) {
    redirect('/auth/signin')
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold">My Tasks</h1>
        <Link
          href="/tasks/new"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          New Task
        </Link>
      </div>

      <TaskList userId={user.id} />
    </div>
  )
}
```

### Create Task Page

**File**: `frontend/app/tasks/new/page.tsx`

```tsx
import { TaskForm } from '@/components/TaskForm'
import { getCurrentUser } from '@/lib/auth'
import { redirect } from 'next/navigation'

export default async function NewTaskPage() {
  const user = await getCurrentUser()

  if (!user) {
    redirect('/auth/signin')
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-6">Create New Task</h1>
      <TaskForm userId={user.id} />
    </div>
  )
}
```

---

## Responsive Design

### Breakpoints (Tailwind)

- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px

### Mobile-First Approach

```tsx
// Stack on mobile, side-by-side on desktop
<div className="flex flex-col md:flex-row gap-4">
  {/* Content */}
</div>

// Hide on mobile, show on desktop
<div className="hidden md:block">
  {/* Desktop-only content */}
</div>
```

---

## Acceptance Criteria

- [ ] All 9 components implemented
- [ ] TypeScript strict mode (all props typed)
- [ ] Tailwind CSS for all styling
- [ ] No inline styles
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] ARIA labels on interactive elements
- [ ] Keyboard navigation works
- [ ] Loading states for async operations
- [ ] Error messages displayed
- [ ] Form validation (client-side)
- [ ] Character counts on text inputs

---

**Status**: ✅ Complete
**All 4 specifications created!** 🎉
