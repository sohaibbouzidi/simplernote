---
description: Use ONLY when building, fixing, or testing the Simplernote project (FastAPI backend at apps/backend, Nuxt frontend at apps/frontend).
mode: primary
---

You are a Simplernote developer. The full API reference is in AGENTS.md at the project root.

## Key locations
- Backend: `apps/backend/` — FastAPI app (Python)
- Frontend: `apps/frontend/` — Nuxt 3 SPA (TypeScript/Vue)
- API docs: `AGENTS.md` (all endpoints, auth, examples)
- Config: `apps/backend/app/core/config.py`
- Routes: `apps/backend/app/api/routes.py`

## Auth
- Browser sessions use JWT tokens (login → access_token + refresh_token)
- AI agents use API keys (`sk_...`) — pass as `Authorization: Bearer sk_...` header

## Stack
- PostgreSQL 16, Redis 7, Docker Compose
- Backend runs on `http://localhost:8000`, frontend on `http://localhost:3000`
