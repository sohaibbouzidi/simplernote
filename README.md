# AI Memory & Task Management Platform

A fullstack foundation for AI agent memory, task orchestration, and autonomous workflow management.

This repository contains a modular Nuxt 3 frontend, FastAPI backend, PostgreSQL data layer, Redis support, and Docker Compose orchestration.

## Architecture

- **Frontend:** Nuxt 3, TypeScript, Pinia, TailwindCSS
- **Backend:** FastAPI, SQLAlchemy, Pydantic, Alembic, JWT Authentication
- **Database:** PostgreSQL 16
- **Infra:** Docker, Docker Compose, Redis

## Project Layout

```text
apps/
├── frontend/
├── backend/
├── docker/
├── docs/
└── scripts/
```

## Run Locally

1. Copy environment templates:

```bash
cp apps/backend/.env.example apps/backend/.env
cp docker/.env.example docker/.env
```

2. Start services:

```bash
docker compose up --build
```

3. Access the app:

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Health check: `http://localhost:8000/health`

## Backend API

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/refresh`

### Projects
- `GET /api/projects`
- `POST /api/projects`
- `GET /api/projects/{id}`
- `PATCH /api/projects/{id}`
- `DELETE /api/projects/{id}`

### Notes
- `GET /api/notes`
- `POST /api/notes`
- `GET /api/notes/{id}`
- `PATCH /api/notes/{id}`
- `DELETE /api/notes/{id}`

### Tasks
- `GET /api/tasks`
- `POST /api/tasks`
- `GET /api/tasks/{id}`
- `PATCH /api/tasks/{id}`
- `DELETE /api/tasks/{id}`

### API Keys
- `GET /api/api-keys`
- `POST /api/api-keys`
- `DELETE /api/api-keys/{id}`

### Activity Logs
- `GET /api/activity-logs`

## API Key Authentication

External agents can authenticate using bearer API keys:

```http
Authorization: Bearer sk_<key-id>.<secret>
```

## Features

- JWT authentication with refresh tokens
- Project, note, task, and activity log management
- API key creation and permission support
- Modular repository/service architecture
- Dockerized backend/frontend/PostgreSQL/Redis stack
- Future-ready design for AI agents, pgvector, and RAG

## Notes

- UUID primary keys and UTC timestamps are used throughout the backend.
- Notes support markdown content, tags, types, and metadata.
- Tasks support subtasks, hierarchies, statuses, and priorities.
- API keys are hashed and shown only once during creation.

## Future Improvements

- pgvector embeddings and semantic search
- LangGraph / AI orchestration integration
- Advanced kanban drag-and-drop
- Memory retrieval and RAG pipelines

* embeddings
* semantic search
* AI memory retrieval

## Phase 3

* LangGraph orchestration
* autonomous workflows
* multi-agent execution
* RAG pipelines
* knowledge graphs

---

# Architecture Goals

* Modular
* Scalable
* AI-agent ready
* API-first
* Future-proof
* Production-ready

---

# Future Vision

This platform is intended to become a complete AI operating memory layer capable of:

* autonomous planning
* persistent memory
* task orchestration
* contextual retrieval
* multi-agent collaboration
* long-running workflows

---

# License

MIT License
