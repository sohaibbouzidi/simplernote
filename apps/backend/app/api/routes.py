from fastapi import APIRouter, Depends

from app.api.endpoints import auth, projects, notes, tasks, api_keys, activity_logs, ai_context, admin
from app.api.endpoints import totp
from app.api.endpoints import users
from app.api.endpoints import ai_agent
from app.api.endpoints import export as export_endpoints
from app.api.deps import require_profile_complete

api_router = APIRouter()
# auth routes are public for login/registration/refresh/me
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(totp.router, prefix="/auth/totp", tags=["totp"])

# Require profile completion for all app routes (except auth and users endpoints)
api_router.include_router(projects.router, prefix="/projects", tags=["projects"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(notes.router, prefix="/projects/{project_id}/notes", tags=["notes"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(tasks.router, prefix="/projects/{project_id}/tasks", tags=["tasks"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(ai_context.router, prefix="/projects/{project_id}/ai-context", tags=["ai-context"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(ai_context.search_router, prefix="/ai-context", tags=["ai-context"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api_keys"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(activity_logs.router, prefix="/activity-logs", tags=["activity_logs"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(require_profile_complete)])

# User profile routes are used to complete profile, so do not require profile completed
api_router.include_router(users.router, prefix="/users", tags=["users"])

api_router.include_router(export_endpoints.router, prefix="/export", tags=["export"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(ai_agent.router, prefix="/ai-agent", tags=["ai-agent"])
