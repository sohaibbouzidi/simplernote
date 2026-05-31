from typing import Any
from fastapi import APIRouter, Depends, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.services.auth import AuthService
from app.services.notes import NoteService
from app.services.tasks import TaskService

router = APIRouter()


def _get(obj: Any, attr: str, default=None):
    if isinstance(obj, dict):
        return obj.get(attr, default)
    return getattr(obj, attr, default)


@router.get("/")
def export_data(
    format: str = Query("json", regex="^(json|markdown)$"),
    project_id: str = Query(..., description="Project ID is required"),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    user_id = str(current_user.id)
    notes = NoteService.list_notes(db, user_id, project_id)
    tasks = TaskService.list_tasks(db, user_id, project_id)

    if format == "markdown":
        lines = [f"# Simplernote Export — {current_user.email} (project: {project_id})"]
        lines.append("")
        lines.append(f"Generated: {__import__('datetime').datetime.utcnow().isoformat()}Z")
        lines.append("")

        if notes:
            lines.append("## Notes")
            lines.append("")
            for n in notes:
                lines.append(f"### {_get(n, 'title')}")
                note_type = _get(n, 'note_type')
                if note_type:
                    lines.append(f"**Type:** {note_type}")
                tags = _get(n, 'tags', [])
                if tags:
                    lines.append(f"**Tags:** {', '.join(tags)}")
                lines.append("")
                content = _get(n, 'content') or _get(n, 'summary') or "No content"
                lines.append(content)
                lines.append("")
                lines.append("---")
                lines.append("")

        if tasks:
            lines.append("## Tasks")
            lines.append("")
            for t in tasks:
                status_icon = {"done": "✅", "in-progress": "🔄", "todo": "📝", "backlog": "📋", "review": "👀", "blocked": "🚫", "cancelled": "❌", "deferred": "⏳"}
                icon = status_icon.get(_get(t, 'status'), "📝")
                lines.append(f"### {icon} {_get(t, 'title')}")
                lines.append(f"**Status:** {_get(t, 'status')}  |  **Priority:** {_get(t, 'priority')}")
                description = _get(t, 'description')
                if description:
                    lines.append("")
                    lines.append(description)
                lines.append("")
                lines.append("---")
                lines.append("")

        return PlainTextResponse("\n".join(lines), media_type="text/markdown")

    data = {
        "exported_at": __import__("datetime").datetime.utcnow().isoformat() + "Z",
        "user": current_user.email,
        "notes": [
            {
                "id": str(_get(n, 'id')),
                "title": _get(n, 'title'),
                "content": _get(n, 'content'),
                "summary": _get(n, 'summary'),
                "note_type": _get(n, 'note_type'),
                "tags": _get(n, 'tags', []) or [],
                "project_id": str(_get(n, 'project_id')) if _get(n, 'project_id') else None,
                "created_at": _get(n, 'created_at').isoformat() if _get(n, 'created_at') else None,
                "updated_at": _get(n, 'updated_at').isoformat() if _get(n, 'updated_at') else None,
            }
            for n in notes
        ],
        "tasks": [
            {
                "id": str(_get(t, 'id')),
                "title": _get(t, 'title'),
                "description": _get(t, 'description'),
                "status": _get(t, 'status'),
                "priority": _get(t, 'priority'),
                "assigned_agent": _get(t, 'assigned_agent'),
                "project_id": str(_get(t, 'project_id')) if _get(t, 'project_id') else None,
                "created_at": _get(t, 'created_at').isoformat() if _get(t, 'created_at') else None,
            }
            for t in tasks
        ],
    }
    return data
