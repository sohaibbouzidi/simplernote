from fastapi import APIRouter

from app.api.endpoints import auth, projects, notes, tasks, api_keys, activity_logs

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(api_keys.router, prefix="/api-keys", tags=["api_keys"])
api_router.include_router(activity_logs.router, prefix="/activity-logs", tags=["activity_logs"])
