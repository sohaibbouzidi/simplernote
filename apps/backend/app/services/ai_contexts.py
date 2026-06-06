from datetime import datetime
from typing import List
from app.utils.timezone import now
from sqlalchemy.orm import Session
from app.models.ai_context import AiContext
from app.schemas.ai_context import AiContextCreateSchema, AiContextUpdateSchema


class AiContextService:

    @staticmethod
    def list_by_project(db: Session, project_id: str, user_id: str = None) -> List[AiContext]:
        """Get all non-deleted contexts for a project."""
        query = db.query(AiContext).filter(
            AiContext.project_id == project_id,
            AiContext.deleted_at.is_(None),
        )
        if user_id:
            query = query.filter(AiContext.created_by == user_id)
        return query.all()

    @staticmethod
    def get_by_project_and_name(db: Session, project_id: str, name: str, user_id: str = None) -> AiContext | None:
        """Get a specific context by project_id and name."""
        query = db.query(AiContext).filter(
            AiContext.project_id == project_id,
            AiContext.name == name,
            AiContext.deleted_at.is_(None),
        )
        if user_id:
            query = query.filter(AiContext.created_by == user_id)
        return query.first()

    @staticmethod
    def get_by_id(db: Session, context_id: str, user_id: str = None) -> AiContext | None:
        """Get a specific context by ID."""
        query = db.query(AiContext).filter(
            AiContext.id == context_id,
            AiContext.deleted_at.is_(None),
        )
        if user_id:
            query = query.filter(AiContext.created_by == user_id)
        return query.first()

    @staticmethod
    def get_by_project(db: Session, project_id: str, user_id: str = None) -> AiContext | None:
        """DEPRECATED: Get the default context for a project (backwards compatibility)."""
        return AiContextService.get_by_project_and_name(db, project_id, "default", user_id)

    @staticmethod
    def create(db: Session, user_id: str, project_id: str, data: AiContextCreateSchema) -> AiContext:
        ctx = AiContext(
            project_id=project_id,
            name=data.name,
            content=data.content,
            created_by=user_id,
        )
        db.add(ctx)
        db.commit()
        db.refresh(ctx)
        return ctx

    @staticmethod
    def update(db: Session, ctx: AiContext, data: AiContextUpdateSchema) -> AiContext:
        if data.name is not None:
            ctx.name = data.name
        if data.content is not None:
            ctx.content = data.content
        db.commit()
        db.refresh(ctx)
        return ctx

    @staticmethod
    def delete(db: Session, ctx: AiContext) -> None:
        ctx.deleted_at = now()
        db.commit()

    @staticmethod
    def restore(db: Session, ctx: AiContext) -> AiContext:
        ctx.deleted_at = None
        db.commit()
        db.refresh(ctx)
        return ctx
