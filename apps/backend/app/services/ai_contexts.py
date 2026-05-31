from datetime import datetime
from sqlalchemy.orm import Session
from app.models.ai_context import AiContext
from app.schemas.ai_context import AiContextCreateSchema, AiContextUpdateSchema


class AiContextService:

    @staticmethod
    def get_by_project(db: Session, project_id: str, user_id: str = None) -> AiContext | None:
        query = db.query(AiContext).filter(
            AiContext.project_id == project_id,
            AiContext.deleted_at.is_(None),
        )
        if user_id:
            query = query.filter(AiContext.created_by == user_id)
        return query.first()

    @staticmethod
    def create(db: Session, user_id: str, project_id: str, data: AiContextCreateSchema) -> AiContext:
        ctx = AiContext(
            project_id=project_id,
            content=data.content,
            created_by=user_id,
        )
        db.add(ctx)
        db.commit()
        db.refresh(ctx)
        return ctx

    @staticmethod
    def update(db: Session, ctx: AiContext, data: AiContextUpdateSchema) -> AiContext:
        if data.content is not None:
            ctx.content = data.content
        db.commit()
        db.refresh(ctx)
        return ctx

    @staticmethod
    def delete(db: Session, ctx: AiContext) -> None:
        ctx.deleted_at = datetime.utcnow()
        db.commit()
