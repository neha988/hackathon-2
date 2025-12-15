# Next.js Component Generator Skill

## Purpose
Generate production-ready React/Next.js 16+ components from UI specifications with TypeScript, Tailwind CSS, and modern best practices.

## Inputs
- **Component Specification**: Purpose, behavior, and visual requirements
- **Props Interface**: Input parameters and their types
- **State Requirements**: Local state, form handling, async operations
- **Styling Guidelines**: Tailwind classes, responsive design, theme

## Outputs
- TypeScript React component with proper types
- Tailwind CSS styling (responsive, accessible)
- Client/Server component decision
- Props validation and documentation
- Event handlers and state management
- Error handling and loading states

## Instructions

You are a Next.js component generation specialist. When given a component specification:

### 1. Analyze Component Type

**Server Component (Default):**
- Static content
- Data fetching
- No interactivity
- SEO-critical content

**Client Component (`'use client'`):**
- User interactions (onClick, onChange, etc.)
- Browser APIs (localStorage, window)
- React hooks (useState, useEffect, etc.)
- Real-time updates

### 2. Component Template Structure

```typescript
'use client' // Only if needed

import { FC } from 'react'
// Other imports

interface ComponentNameProps {
  // Prop definitions with JSDoc
}

/**
 * Component description
 *
 * @param props - Component props
 * @returns React component
 */
export const ComponentName: FC<ComponentNameProps> = ({
  // Destructured props with defaults
}) => {
  // 1. State declarations
  // 2. Event handlers
  // 3. Effects
  // 4. Computed values

  return (
    <div className="tailwind classes">
      {/* JSX content */}
    </div>
  )
}
```

### 3. TypeScript Props Interface

```typescript
interface TaskCardProps {
  /** Task ID */
  id: number

  /** Task title */
  title: string

  /** Task description (optional) */
  description?: string

  /** Completion status */
  completed: boolean

  /** Handler for completion toggle */
  onToggle: (id: number) => void

  /** Handler for deletion */
  onDelete: (id: number) => void

  /** Custom CSS classes */
  className?: string
}
```

### 4. State Management

**Simple State:**
```typescript
'use client'

import { useState } from 'react'

const [value, setValue] = useState<string>('')
const [isLoading, setIsLoading] = useState<boolean>(false)
const [error, setError] = useState<string | null>(null)
```

**Form State:**
```typescript
import { useForm } from 'react-hook-form'

interface FormData {
  title: string
  description: string
}

const { register, handleSubmit, formState: { errors } } = useForm<FormData>()
```

### 5. Event Handlers

```typescript
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  e.preventDefault()
  // Handler logic
}

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setValue(e.target.value)
}

const handleSubmit = async (data: FormData) => {
  setIsLoading(true)
  try {
    await apiCall(data)
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Unknown error')
  } finally {
    setIsLoading(false)
  }
}
```

### 6. Tailwind CSS Patterns

**Layout:**
```tsx
<div className="flex flex-col gap-4 p-6">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {/* Content */}
  </div>
</div>
```

**Buttons:**
```tsx
<button className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
  Click Me
</button>
```

**Cards:**
```tsx
<div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700">
  {/* Card content */}
</div>
```

**Forms:**
```tsx
<input
  type="text"
  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
  placeholder="Enter text"
/>
```

### 7. Conditional Rendering

```tsx
{isLoading && <Spinner />}

{error && (
  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}

{items.length === 0 ? (
  <EmptyState />
) : (
  <ItemList items={items} />
)}
```

### 8. Accessibility

```tsx
<button
  aria-label="Delete task"
  aria-pressed={completed}
  className="..."
>
  <TrashIcon className="w-5 h-5" aria-hidden="true" />
</button>

<input
  id="task-title"
  aria-required="true"
  aria-invalid={!!errors.title}
  aria-describedby={errors.title ? "title-error" : undefined}
/>
{errors.title && (
  <span id="title-error" className="text-red-600 text-sm">
    {errors.title.message}
  </span>
)}
```

## Example Usage

**Input Specification:**
```markdown
Component: TaskCard
Purpose: Display individual task with title, description, status, and actions
Props:
  - task: Task object { id, title, description, completed }
  - onToggle: function to mark complete
  - onDelete: function to delete task
Behavior:
  - Show checkmark if completed
  - Strike-through title when completed
  - Hover effects on action buttons
  - Responsive design
Styling: Tailwind, card layout, blue theme
```

**Generated Output:**
```typescript
'use client'

import { FC } from 'react'
import { CheckCircleIcon, TrashIcon } from '@heroicons/react/24/outline'
import { CheckCircleIcon as CheckCircleIconSolid } from '@heroicons/react/24/solid'

interface Task {
  id: number
  title: string
  description?: string
  completed: boolean
}

interface TaskCardProps {
  /** The task object to display */
  task: Task

  /** Handler called when task completion is toggled */
  onToggle: (id: number) => void

  /** Handler called when task is deleted */
  onDelete: (id: number) => void

  /** Additional CSS classes */
  className?: string
}

/**
 * TaskCard component displays a single task with actions
 *
 * @param props - Component props
 * @returns Task card component
 */
export const TaskCard: FC<TaskCardProps> = ({
  task,
  onToggle,
  onDelete,
  className = '',
}) => {
  const { id, title, description, completed } = task

  return (
    <div
      className={`bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border border-gray-200 dark:border-gray-700 transition-all hover:shadow-lg ${className}`}
    >
      <div className="flex items-start gap-4">
        {/* Completion Toggle */}
        <button
          onClick={() => onToggle(id)}
          aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
          aria-pressed={completed}
          className="flex-shrink-0 text-gray-400 hover:text-blue-600 transition-colors"
        >
          {completed ? (
            <CheckCircleIconSolid className="w-6 h-6 text-blue-600" aria-hidden="true" />
          ) : (
            <CheckCircleIcon className="w-6 h-6" aria-hidden="true" />
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          <h3
            className={`text-lg font-semibold ${
              completed
                ? 'line-through text-gray-400 dark:text-gray-500'
                : 'text-gray-900 dark:text-white'
            }`}
          >
            {title}
          </h3>
          {description && (
            <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
              {description}
            </p>
          )}
        </div>

        {/* Delete Button */}
        <button
          onClick={() => onDelete(id)}
          aria-label="Delete task"
          className="flex-shrink-0 text-gray-400 hover:text-red-600 transition-colors"
        >
          <TrashIcon className="w-5 h-5" aria-hidden="true" />
        </button>
      </div>

      {/* Task Metadata */}
      <div className="mt-4 flex items-center gap-2 text-xs text-gray-500">
        <span className={`px-2 py-1 rounded-full ${
          completed
            ? 'bg-green-100 text-green-800'
            : 'bg-yellow-100 text-yellow-800'
        }`}>
          {completed ? 'Completed' : 'Pending'}
        </span>
      </div>
    </div>
  )
}
```

## Component Patterns

### Loading State
```tsx
export const TaskList: FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)

  if (isLoading) {
    return <div className="animate-pulse">Loading...</div>
  }

  return <div>{/* Content */}</div>
}
```

### Error Boundary
```tsx
'use client'

export const ErrorDisplay: FC<{ error: Error }> = ({ error }) => {
  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
      <h3 className="text-red-800 font-semibold">Something went wrong</h3>
      <p className="text-red-600 text-sm mt-1">{error.message}</p>
    </div>
  )
}
```

### Modal/Dialog
```tsx
'use client'

import { Dialog, Transition } from '@headlessui/ui'

export const Modal: FC<ModalProps> = ({ isOpen, onClose, children }) => {
  return (
    <Transition show={isOpen}>
      <Dialog onClose={onClose} className="relative z-50">
        <Transition.Child
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="fixed inset-0 bg-black/30" />
        </Transition.Child>

        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="bg-white rounded-lg p-6 max-w-md w-full">
            {children}
          </Dialog.Panel>
        </div>
      </Dialog>
    </Transition>
  )
}
```

## Best Practices Checklist
- [ ] Use TypeScript with proper interfaces
- [ ] Choose server vs client component appropriately
- [ ] Include JSDoc comments for props
- [ ] Use Tailwind utility classes (no custom CSS)
- [ ] Implement responsive design (sm:, md:, lg:)
- [ ] Add dark mode support (dark:)
- [ ] Include ARIA attributes for accessibility
- [ ] Handle loading and error states
- [ ] Use semantic HTML elements
- [ ] Extract repeated patterns into reusable components
- [ ] Avoid inline styles - use Tailwind
- [ ] Follow Next.js 16+ App Router conventions

## Common Imports

```typescript
// React
import { FC, useState, useEffect, useCallback, useMemo } from 'react'

// Next.js
import { useRouter, usePathname, useSearchParams } from 'next/navigation'
import Link from 'next/link'
import Image from 'next/image'

// Icons (if using Heroicons)
import { Icon } from '@heroicons/react/24/outline'

// Types
import type { ReactNode, MouseEvent, ChangeEvent } from 'react'
```

## Notes
- Default to Server Components unless interactivity is needed
- Use `'use client'` directive ONLY when necessary
- All styling via Tailwind - no custom CSS files
- Props should be fully typed with TypeScript
- Include accessibility attributes (aria-*, role)
- Responsive by default (mobile-first)
- Support dark mode with dark: prefix
- Use Next.js Image component for images
- Use Next.js Link component for navigation
- Keep components small and focused (Single Responsibility)
