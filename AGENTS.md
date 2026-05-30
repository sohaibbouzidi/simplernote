# Simplernote API — AI Agent Guide

You can interact with Simplernote programmatically using API keys. All endpoints return JSON.

---

## Configuration

- **Base URL**: `http://localhost:8000/api`
- **Auth**: `Authorization: Bearer YOUR_API_KEY`
- **Content-Type**: `application/json`

---

## Endpoints

### AI Context — search and import knowledge
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/ai-context/search?query=...` | Search notes and tasks |
| POST | `/ai-context/import` | Batch import notes and tasks |

### Notes — structured notes with types, tags, metadata
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/notes` | List all notes |
| POST | `/notes` | Create a note |
| GET | `/notes/:id` | Get a note |
| PATCH | `/notes/:id` | Update a note |
| DELETE | `/notes/:id` | Delete a note |

### Tasks — status lanes, priorities, agent assignment
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/tasks` | List all tasks |
| POST | `/tasks` | Create a task |
| GET | `/tasks/:id` | Get a task |
| PATCH | `/tasks/:id` | Update a task |
| DELETE | `/tasks/:id` | Delete a task |

### Projects — workspaces grouping notes and tasks
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/projects` | List all projects |
| POST | `/projects` | Create a project |
| GET | `/projects/:id` | Get a project |
| PATCH | `/projects/:id` | Update a project |
| DELETE | `/projects/:id` | Delete a project |

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

### Auth — user authentication
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/auth/register` | Register a new user (sends confirmation email) |
| POST | `/auth/login` | Login |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/confirm-email` | Confirm email address with token |
| POST | `/auth/forgot-password` | Request password reset email |
| POST | `/auth/reset-password` | Reset password with token |
| GET | `/auth/me` | Get current user profile |
| PATCH | `/auth/password` | Change password (requires auth)

---

## Examples

```bash
# Search context
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "http://localhost:8000/api/ai-context/search?query=deployment+steps"

# List projects
curl -H "Authorization: Bearer YOUR_API_KEY" \
  "http://localhost:8000/api/projects"

# Create a task
curl -X POST "http://localhost:8000/api/tasks" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project_id": "...", "title": "Review PR", "status": "todo", "priority": "high"}'
```
