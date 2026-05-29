from fastapi import APIRouter, Depends

from app.api.endpoints import auth, projects, notes, tasks, api_keys, activity_logs, ai_context, admin
from app.api.endpoints import users
from app.api.deps import require_profile_complete

api_router = APIRouter()
# auth routes are public for login/registration/refresh/me
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Require profile completion for all app routes (except auth and users endpoints)
api_router.include_router(projects.router, prefix="/projects", tags=["projects"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api_keys"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(activity_logs.router, prefix="/activity-logs", tags=["activity_logs"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(ai_context.router, prefix="/ai-context", tags=["ai-context"], dependencies=[Depends(require_profile_complete)])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(require_profile_complete)])

# User profile routes are used to complete profile, so do not require profile completed
api_router.include_router(users.router, prefix="/users", tags=["users"])
