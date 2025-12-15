# API Client Generator Skill

## Purpose
Generate type-safe, fully-typed TypeScript API client from endpoint specifications with error handling, authentication, and request/response validation.

## Inputs
- **API Specification**: Endpoints with methods, paths, parameters, request/response schemas
- **Base URL**: API server location (development/production)
- **Authentication**: Token-based, API key, or session-based auth
- **Error Handling**: Retry logic, timeout configuration, error types

## Outputs
- TypeScript API client with full type safety
- Request/response type definitions
- Error handling utilities
- Authentication header injection
- Axios/Fetch wrapper with interceptors

## Instructions

You are an API client code generation specialist. When given API specifications:

### 1. Analyze API Specification

Parse endpoint details:
- HTTP methods (GET, POST, PUT, PATCH, DELETE)
- URL paths and path parameters
- Query parameters
- Request body schemas
- Response schemas
- Authentication requirements
- Error responses

### 2. Generate Type Definitions

```typescript
// Base types
export interface ApiResponse<T> {
  data: T
  status: number
  message?: string
}

export interface ApiError {
  status: number
  message: string
  errors?: Record<string, string[]>
}

// Entity types
export interface Task {
  id: number
  user_id: string
  title: string
  description?: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface User {
  id: string
  email: string
  name: string
  created_at: string
}

// Request types
export interface CreateTaskInput {
  title: string
  description?: string
}

export interface UpdateTaskInput {
  title?: string
  description?: string
  completed?: boolean
}

// Query parameter types
export interface TaskFilters {
  status?: 'all' | 'pending' | 'completed'
  limit?: number
  offset?: number
}
```

### 3. Create HTTP Client Base

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios'

// Configuration
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// Custom error class
export class ApiClientError extends Error {
  constructor(
    public status: number,
    public message: string,
    public errors?: Record<string, string[]>
  ) {
    super(message)
    this.name = 'ApiClientError'
  }
}

// Create axios instance
const createHttpClient = (): AxiosInstance => {
  const client = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  // Request interceptor (add auth token)
  client.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('auth_token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => Promise.reject(error)
  )

  // Response interceptor (error handling)
  client.interceptors.response.use(
    (response) => response,
    (error: AxiosError<ApiError>) => {
      if (error.response) {
        const { status, data } = error.response
        throw new ApiClientError(
          status,
          data.message || 'An error occurred',
          data.errors
        )
      }
      throw new ApiClientError(0, 'Network error')
    }
  )

  return client
}

const httpClient = createHttpClient()
```

### 4. Generate API Methods

```typescript
export const api = {
  // Tasks
  tasks: {
    /**
     * Get all tasks for a user
     */
    list: async (
      userId: string,
      filters?: TaskFilters
    ): Promise<Task[]> => {
      const { data } = await httpClient.get<Task[]>(
        `/api/${userId}/tasks`,
        { params: filters }
      )
      return data
    },

    /**
     * Get a single task by ID
     */
    get: async (userId: string, taskId: number): Promise<Task> => {
      const { data } = await httpClient.get<Task>(
        `/api/${userId}/tasks/${taskId}`
      )
      return data
    },

    /**
     * Create a new task
     */
    create: async (
      userId: string,
      input: CreateTaskInput
    ): Promise<Task> => {
      const { data } = await httpClient.post<Task>(
        `/api/${userId}/tasks`,
        input
      )
      return data
    },

    /**
     * Update an existing task
     */
    update: async (
      userId: string,
      taskId: number,
      input: UpdateTaskInput
    ): Promise<Task> => {
      const { data } = await httpClient.put<Task>(
        `/api/${userId}/tasks/${taskId}`,
        input
      )
      return data
    },

    /**
     * Delete a task
     */
    delete: async (userId: string, taskId: number): Promise<void> => {
      await httpClient.delete(`/api/${userId}/tasks/${taskId}`)
    },

    /**
     * Toggle task completion
     */
    toggleComplete: async (
      userId: string,
      taskId: number
    ): Promise<Task> => {
      const { data } = await httpClient.patch<Task>(
        `/api/${userId}/tasks/${taskId}/complete`
      )
      return data
    },
  },

  // Users
  users: {
    /**
     * Get current user profile
     */
    me: async (): Promise<User> => {
      const { data } = await httpClient.get<User>('/api/users/me')
      return data
    },

    /**
     * Update user profile
     */
    update: async (userId: string, input: UpdateUserInput): Promise<User> => {
      const { data } = await httpClient.put<User>(
        `/api/users/${userId}`,
        input
      )
      return data
    },
  },
}
```

### 5. React Hook Integration (Optional)

```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'

export const useTasksQuery = (userId: string, filters?: TaskFilters) => {
  return useQuery({
    queryKey: ['tasks', userId, filters],
    queryFn: () => api.tasks.list(userId, filters),
  })
}

export const useCreateTaskMutation = (userId: string) => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (input: CreateTaskInput) => api.tasks.create(userId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', userId] })
    },
  })
}

export const useUpdateTaskMutation = (userId: string) => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ taskId, input }: { taskId: number; input: UpdateTaskInput }) =>
      api.tasks.update(userId, taskId, input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', userId] })
    },
  })
}

export const useDeleteTaskMutation = (userId: string) => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (taskId: number) => api.tasks.delete(userId, taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks', userId] })
    },
  })
}
```

### 6. Fetch-Based Alternative (No Dependencies)

```typescript
class ApiClient {
  private baseURL: string
  private getAuthToken: () => Promise<string | null>

  constructor(baseURL: string, getAuthToken: () => Promise<string | null>) {
    this.baseURL = baseURL
    this.getAuthToken = getAuthToken
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = await this.getAuthToken()

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers,
    })

    if (!response.ok) {
      const error = await response.json().catch(() => ({
        message: response.statusText,
      }))
      throw new ApiClientError(response.status, error.message, error.errors)
    }

    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T
    }

    return response.json()
  }

  // GET request
  async get<T>(endpoint: string, params?: Record<string, any>): Promise<T> {
    const url = params
      ? `${endpoint}?${new URLSearchParams(params)}`
      : endpoint
    return this.request<T>(url, { method: 'GET' })
  }

  // POST request
  async post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  // PUT request
  async put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  // PATCH request
  async patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PATCH',
      body: JSON.stringify(data),
    })
  }

  // DELETE request
  async delete<T = void>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

// Create instance
const getToken = async () => {
  // Get token from auth provider
  const session = await authClient.getSession()
  return session?.session.token || null
}

const apiClient = new ApiClient(API_BASE_URL, getToken)

// Export typed methods
export const api = {
  tasks: {
    list: (userId: string, filters?: TaskFilters) =>
      apiClient.get<Task[]>(`/api/${userId}/tasks`, filters),

    get: (userId: string, taskId: number) =>
      apiClient.get<Task>(`/api/${userId}/tasks/${taskId}`),

    create: (userId: string, input: CreateTaskInput) =>
      apiClient.post<Task>(`/api/${userId}/tasks`, input),

    update: (userId: string, taskId: number, input: UpdateTaskInput) =>
      apiClient.put<Task>(`/api/${userId}/tasks/${taskId}`, input),

    delete: (userId: string, taskId: number) =>
      apiClient.delete(`/api/${userId}/tasks/${taskId}`),

    toggleComplete: (userId: string, taskId: number) =>
      apiClient.patch<Task>(`/api/${userId}/tasks/${taskId}/complete`),
  },
}
```

### 7. Error Handling Utilities

```typescript
export const handleApiError = (error: unknown): string => {
  if (error instanceof ApiClientError) {
    if (error.errors) {
      // Validation errors
      return Object.entries(error.errors)
        .map(([field, messages]) => `${field}: ${messages.join(', ')}`)
        .join('\n')
    }
    return error.message
  }

  if (error instanceof Error) {
    return error.message
  }

  return 'An unexpected error occurred'
}

// Usage in components
try {
  await api.tasks.create(userId, taskData)
} catch (error) {
  const message = handleApiError(error)
  toast.error(message)
}
```

### 8. OpenAPI/Swagger Integration

```typescript
// Generate types from OpenAPI spec
import type { paths } from './generated/api-schema' // From openapi-typescript

type TasksListResponse = paths['/api/{user_id}/tasks']['get']['responses']['200']['content']['application/json']
type CreateTaskRequest = paths['/api/{user_id}/tasks']['post']['requestBody']['content']['application/json']
```

## Example API Specification Input

```markdown
# Task API Endpoints

## GET /api/{user_id}/tasks
Get all tasks for user
Query params: status?, limit?, offset?
Response: Task[]

## GET /api/{user_id}/tasks/{id}
Get single task
Response: Task

## POST /api/{user_id}/tasks
Create task
Body: { title: string, description?: string }
Response: Task

## PUT /api/{user_id}/tasks/{id}
Update task
Body: { title?: string, description?: string, completed?: boolean }
Response: Task

## DELETE /api/{user_id}/tasks/{id}
Delete task
Response: 204 No Content

## PATCH /api/{user_id}/tasks/{id}/complete
Toggle completion
Response: Task
```

## Best Practices Checklist

- [ ] Full TypeScript type safety for all requests/responses
- [ ] Centralized error handling
- [ ] Authentication token injection
- [ ] Request/response interceptors
- [ ] Timeout configuration
- [ ] Retry logic for failed requests (optional)
- [ ] Request cancellation support
- [ ] Loading states integration
- [ ] Environment-based API URL
- [ ] JSDoc comments for all methods
- [ ] Separate types from implementation
- [ ] Handle empty responses (204)
- [ ] Query parameter serialization
- [ ] File upload support (if needed)

## File Structure

```
lib/
├── api/
│   ├── client.ts        # HTTP client setup
│   ├── types.ts         # All type definitions
│   ├── tasks.ts         # Task-related endpoints
│   ├── users.ts         # User-related endpoints
│   ├── errors.ts        # Error handling
│   └── index.ts         # Main export
└── hooks/
    ├── useTasks.ts      # React Query hooks for tasks
    └── useUsers.ts      # React Query hooks for users
```

## Notes
- Use Axios for advanced features (interceptors, cancellation)
- Use Fetch for minimal dependencies and simplicity
- Always type request/response for type safety
- Handle 401 errors by redirecting to login
- Cache GET requests with React Query/SWR
- Implement optimistic updates for better UX
- Use environment variables for API URLs
- Consider generating types from OpenAPI spec
- Add retry logic for transient failures
- Implement request deduplication for concurrent requests
