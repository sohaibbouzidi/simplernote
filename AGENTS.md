# Simplernote API — AI Agent Guide

You can interact with Simplernote programmatically using API keys. All endpoints return JSON.

---

## Configuration

- **Base URL**: `http://localhost:8000/api`
- **Auth**: `X-API-KEY: YOUR_API_KEY`
- **Content-Type**: `application/json`

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
