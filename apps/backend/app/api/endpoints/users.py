import io
import os
import mimetypes
import uuid

from datetime import datetime
from app.utils.timezone import now
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, BackgroundTasks
from sqlalchemy.orm import Session

from app.db.session import get_db, SessionLocal
from app.models.user import User
from app.schemas.auth import UserSchema, UserUpdateSchema
from app.services.users import UserService
from app.services.auth import AuthService
from app.utils.storage import upload_fileobj, ensure_bucket_exists, delete_object, generate_presigned_url
from app.core.config import settings

router = APIRouter()


@router.patch("/me", response_model=UserSchema)
def update_me(
    user_in: UserUpdateSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    user = UserService.update_user(db, current_user, user_in)
    return user


@router.post("/me/picture", response_model=UserSchema)
def upload_picture(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    # validate content type
    allowed = settings.ALLOWED_IMAGE_CONTENT_TYPES
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid image type. Allowed: {', '.join(allowed)}",
        )

    # validate size (use file.file seek/tell)
    try:
        file.file.seek(0, os.SEEK_END)
        size = file.file.tell()
        file.file.seek(0)
    except Exception:
        # fallback: read bytes
        data_tmp = file.file.read()
        size = len(data_tmp)
        file.file = io.BytesIO(data_tmp)

    if size > settings.MAX_PROFILE_PIC_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Image too large. Max size is {settings.MAX_PROFILE_PIC_SIZE_BYTES} bytes",
        )

    # determine extension
    ext = os.path.splitext(file.filename)[1] if file.filename else ""
    if not ext:
        ext = mimetypes.guess_extension(file.content_type) or ""

    # generate unique key
    unique = uuid.uuid4().hex
    key = f"users/{current_user.id}/profile_{unique}{ext}"

    # ensure bucket exists now (so background upload has it)
    ensure_bucket_exists(settings.S3_BUCKET_NAME)

    # read bytes into memory for background upload
    try:
        file.file.seek(0)
        data = file.file.read()
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to read uploaded file")

    # remember previous picture key (if it's a URL, extract the key; otherwise assume it's already a key)
    prev_picture_url = current_user.picture
    prev_key = None
    if prev_picture_url:
        if settings.S3_BUCKET_NAME and f"/{settings.S3_BUCKET_NAME}/" in prev_picture_url:
            prev_key = prev_picture_url.split(f"/{settings.S3_BUCKET_NAME}/", 1)[1]
        else:
            prev_key = prev_picture_url

    # optimistically set new picture to the S3 key in DB and schedule background upload
    current_user.picture = key
    current_user.profile_updated_at = now()
    db.commit()
    db.refresh(current_user)

    def _bg_upload_and_handle(user_id: str, data_bytes: bytes, key: str, content_type: str, prev_picture_url: str | None, prev_key: str | None):
        try:
            upload_fileobj(io.BytesIO(data_bytes), key, content_type=content_type)
            # delete previous object if present
            if prev_key:
                try:
                    delete_object(prev_key)
                except Exception:
                    pass
        except Exception:
            # upload failed: revert DB picture to previous value
            session = SessionLocal()
            try:
                user = session.get(User, user_id)
                if user:
                    user.picture = prev_picture_url if prev_picture_url else None
                    session.add(user)
                    session.commit()
            finally:
                session.close()

    background_tasks.add_task(
        _bg_upload_and_handle,
        str(current_user.id),
        data,
        key,
        file.content_type,
        prev_picture_url,
        prev_key,
    )

    return current_user



@router.get("/me/picture-url")
def get_my_picture_url(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    if not current_user.picture:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No profile picture set")
    try:
        url = generate_presigned_url(current_user.picture)
    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to generate presigned URL")
    return {"url": url}
