# Simplernote — AI Memory & Task Management Platform

A fullstack foundation for AI agent memory, task orchestration, and autonomous workflow management.

**Frontend:** Nuxt 3, TypeScript, Pinia, TailwindCSS  
**Backend:** FastAPI, SQLAlchemy, Pydantic, Alembic, JWT  
**Database:** PostgreSQL 16  
**Infra:** Docker Compose, Redis, MinIO (S3-compatible storage)

## Project Layout

```text
apps/
├── frontend/          # Nuxt 3 SPA
├── backend/           # FastAPI application
│   ├── app/
│   │   ├── api/       # Endpoints (auth, users, projects, notes, tasks, admin, ai-context, ai-agent)
│   │   ├── core/      # Config, rate limiting
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── services/  # Business logic (auth, email, users, api_keys)
│   │   ├── utils/     # Security, storage (S3/MinIO)
│   │   └── db/        # Session management
│   ├── alembic/       # Migrations
│   └── tests/          # Pytest suite (67+ tests)
├── docker/
└── scripts/
```

## Quick Start

```bash
cp apps/backend/.env.example apps/backend/.env
cp docker/.env.example docker/.env
docker compose up --build
```

- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- Health check: `http://localhost:8000/health`

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register (sends confirmation email) |
| POST | `/api/auth/confirm-email` | Confirm email via JWT token |
| POST | `/api/auth/login` | Login (returns access + refresh tokens) |
| POST | `/api/auth/refresh` | Refresh access token |
| GET | `/api/auth/me` | Current user profile |
| PATCH | `/api/auth/password` | Change password |
| POST | `/api/auth/forgot-password` | Request password reset email |
| POST | `/api/auth/reset-password` | Reset password via JWT token |

### AI Agent API — full CRUD (X-API-KEY header)
All endpoints scoped under `/api/ai-agent/` and authenticated via the `X-API-KEY` header.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/ai-agent/projects` | List projects |
| GET/POST/PATCH/DELETE | `/api/ai-agent/projects/{id}/notes` | Notes CRUD |
| GET/POST/PATCH/DELETE | `/api/ai-agent/projects/{id}/tasks` | Tasks CRUD |
| GET/POST/PUT/DELETE | `/api/ai-agent/projects/{id}/context` | AI context CRUD |
| POST | `/api/ai-agent/projects/{id}/context/import` | Auto-import notes+tasks into context |
| GET | `/api/ai-agent/search?query=...` | Search notes & tasks |

See `AGENTS.md` for the full endpoint reference.

## Features

- JWT auth with access/refresh tokens and API key auth
- Projects, notes (rich text, types, tags), tasks (kanban lanes, priorities, agent assignment)
- **Email system** — account confirmation, password reset via Gmail SMTP
- **Admin panel** — user management, role control, email/activity visibility
- **Profile management** — avatar upload to S3 (MinIO), `last_login_at` / `profile_updated_at` tracking
- **AI Context** — per-project knowledge document for AI agents
- **Rate limiting** — per-endpoint (5–30 req/min configurable)
- **Activity logging** — audit trail for all mutations
- Dockerized stack with PostgreSQL, Redis, MinIO

## Email Configuration (Optional)

Set these in `apps/backend/.env` to enable emails (no-op when unset):

```
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=<gmail-app-password>
EMAIL_FROM=your@gmail.com
EMAIL_FROM_NAME=Simplernote
BASE_URL=http://localhost:3000
```

Requires a Gmail App Password (https://myaccount.google.com/apppasswords).

## Tests

```bash
docker compose run --rm backend pytest
```

## License

MIT
