# Simplernote API — AI Agent Guide

You can interact with Simplernote programmatically using API keys. All endpoints return JSON.

---

## Configuration

- **Base URL**: `http://localhost:8000/api`
- **Auth**: `X-API-KEY: YOUR_API_KEY`
- **Content-Type**: `application/json`

---

## Project Knowledge

### Auth Architecture
- **JWT-only** for `/api/` routes: `PermissionChecker`, `require_profile_complete`, `AuthService.get_current_user` all reject API keys (`sk_…`)
- **X-API-KEY only** for `/api/ai-agent/` routes via `get_ai_agent_key` dependency
- No overlap between the two auth paths
- Login now always requires email confirmation (removed `ENFORCE_EMAIL_CONFIRMATION` flag)
- Disabled users (`is_active = False`) are rejected at login with 403 "Account is disabled"
- Rate limit: 10 login attempts per 60 seconds

### Admin Endpoints
- All admin routes check `role == "admin"` via `require_role("admin")`
- Self-modification is blocked: cannot change own role, toggle own active status, or delete own account
- Hard delete (`/admin/users/{id}/hard`) cascades in FK-safe order: activity_logs → api_keys → ai_contexts → tasks → notes → projects → user

### Soft-Delete
- Projects, notes, tasks, and AI contexts all use soft-delete (`deleted_at` column)
- Deleting a project cascades to all its notes, tasks, and contexts (soft-delete)
- Restoring a project restores all cascaded items
- Notes and tasks can be individually restored via dedicated restore endpoints

### Data Isolation
- Users see only their own data (filtered by `created_by`)
- AI agents access only the project their API key was created for (`_check_project_access`)
- Notes/tasks/contexts are scoped to projects

### Timezone Support
- Configurable via `TIMEZONE` env var (default `"UTC"`)
- Utility at `app/utils/timezone.py`: `get_tz()`, `now()`, `localize()` using `zoneinfo.ZoneInfo`
- All model `default` and service calls use `now()` instead of `datetime.utcnow()`
- PostgreSQL `timestamptz` normalizes to UTC internally

### Frontend Conventions
- Admin page: hash-driven tabs not used here, but project detail page uses `#notes`, `#tasks`, `#ai-context`, `#settings` for tab state
- Tab data loads lazily on each tab switch
- Admin actions column right-aligned via `justify-end`
- "Delete Permanently" requires email confirmation input
- Create User modal on admin page

### Testing
- In-memory SQLite database (`sqlite:///file::memory:?cache=shared&mode=memory&uri=true`)
- All tables recreated before and dropped after each test via `setup_database` fixture
- Data-creating fixtures (`registered_user`, `user_project`, `admin_setup`) are self-cleaning (yield + delete)
- SMTP disabled in tests (`settings.SMTP_HOST = "localhost"`)
- 69 tests across auth, admin, projects, notes, tasks, API keys, and AI context

### Infrastructure
- Docker Compose with nginx, backend (FastAPI), frontend (Nuxt 3), PostgreSQL, Redis, MinIO
- nginx upstream hostnames resolve at startup; restart nginx after container rebuilds to avoid 502
- Frontend container has no volume mounts — rebuild on change

---

## Endpoints

### AI Agent API — full CRUD, X-API-KEY header
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ai-agent/projects` | List accessible projects |
| GET | `/ai-agent/projects/{project_id}/notes` | List notes in a project |
| GET | `/ai-agent/projects/{project_id}/notes?note_type=...` | Filter notes by type |
| GET | `/ai-agent/projects/{project_id}/notes?search=...` | Search notes by title/content |
| POST | `/ai-agent/projects/{project_id}/notes` | Create a note |
| PATCH | `/ai-agent/projects/{project_id}/notes/{note_id}` | Update a note |
| DELETE | `/ai-agent/projects/{project_id}/notes/{note_id}` | Delete a note |
| PATCH | `/ai-agent/projects/{project_id}/notes/{note_id}/restore` | Restore a deleted note |
| GET | `/ai-agent/projects/{project_id}/tasks` | List tasks in a project |
| GET | `/ai-agent/projects/{project_id}/tasks?status=...` | Filter tasks by status |
| POST | `/ai-agent/projects/{project_id}/tasks` | Create a task |
| PATCH | `/ai-agent/projects/{project_id}/tasks/{task_id}` | Update a task |
| DELETE | `/ai-agent/projects/{project_id}/tasks/{task_id}` | Delete a task |
| PATCH | `/ai-agent/projects/{project_id}/tasks/{task_id}/restore` | Restore a deleted task |
| GET | `/ai-agent/projects/{project_id}/context` | Get AI context for a project |
| POST | `/ai-agent/projects/{project_id}/context` | Create AI context |
| PUT | `/ai-agent/projects/{project_id}/context` | Update AI context |
| DELETE | `/ai-agent/projects/{project_id}/context` | Delete AI context |
| POST | `/ai-agent/projects/{project_id}/context/import` | Auto-import notes+tasks into context |
| GET | `/ai-agent/search?query=...` | Search across notes and tasks |

All entities (projects, notes, tasks, contexts) use **soft-delete**: deleted items are hidden from listings but can be restored. Deleting a project also soft-deletes all its notes, tasks, and context; restoring the project restores them too.

### API Keys — manage agent credentials
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api-keys` | List API keys |
| POST | `/api-keys` | Create an API key |
| DELETE | `/api-keys/:id` | Revoke an API key |

### Activity Logs — audit trail
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/activity-logs` | List activity logs |

### Admin — user management
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/admin/users` | List all users |
| POST | `/admin/users` | Create a user (email, password, role, email_confirmed) |
| PATCH | `/admin/users/{user_id}/role` | Change user role |
| PATCH | `/admin/users/{user_id}/verify-email` | Manually verify a user's email |
| PATCH | `/admin/users/{user_id}/toggle-active` | Enable/disable a user |
| DELETE | `/admin/users/{user_id}` | Soft-delete (set inactive) |
| DELETE | `/admin/users/{user_id}/hard` | Permanently delete user + all data |

---

## Examples

```bash
# List projects (AI agent API - X-API-KEY header)
curl -H "X-API-KEY: YOUR_API_KEY" \
  "http://localhost:8000/api/ai-agent/projects"

# List notes in a project (AI agent API)
curl -H "X-API-KEY: YOUR_API_KEY" \
  "http://localhost:8000/api/ai-agent/projects/{project_id}/notes"

# Search across notes and tasks (AI agent API)
curl -H "X-API-KEY: YOUR_API_KEY" \
  "http://localhost:8000/api/ai-agent/search?query=deployment"

# Create a task (AI agent API)
curl -X POST "http://localhost:8000/api/ai-agent/projects/{project_id}/tasks" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Review PR", "status": "todo", "priority": "high"}'

# Update AI context (AI agent API)
curl -X PUT "http://localhost:8000/api/ai-agent/projects/{project_id}/context" \
  -H "X-API-KEY: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "# Current Focus\n\nWorking on deployment automation."}'
```
