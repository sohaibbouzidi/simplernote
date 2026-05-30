import io
import base64
import pyotp
import qrcode
import qrcode.image.svg

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.rate_limit import rate_limit
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import TOTPSetupResponse, TOTPVerifySchema, TOTPDisableSchema
from app.services.auth import AuthService
from app.services.activity_logs import ActivityLogService
from app.utils.security import verify_password

router = APIRouter()


def _generate_qr_svg(uri: str) -> str:
    buf = io.BytesIO()
    img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgImage)
    img.save(buf)
    return "data:image/svg+xml;base64," + base64.b64encode(buf.getvalue()).decode()


@router.post("/setup", response_model=TOTPSetupResponse)
def setup_totp(
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    if current_user.totp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is already enabled")
    secret = pyotp.random_base32()
    provisioning_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=current_user.email,
        issuer_name="Simplernote",
    )
    current_user.totp_secret = secret
    db.commit()
    qr_svg = _generate_qr_svg(provisioning_uri)
    return TOTPSetupResponse(secret=secret, provisioning_uri=provisioning_uri, qr_svg=qr_svg)


@router.post("/verify", response_model=dict)
def verify_totp(
    data: TOTPVerifySchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    if not current_user.totp_secret:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA not set up yet")
    if current_user.totp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is already enabled")
    totp = pyotp.TOTP(current_user.totp_secret)
    if not totp.verify(data.code, valid_window=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid code")
    current_user.totp_enabled = True
    db.commit()
    ActivityLogService.record(db, user_id=str(current_user.id), action="enable", entity_type="totp", entity_id=str(current_user.id))
    return {"message": "2FA enabled successfully"}


@router.post("/disable", response_model=dict)
def disable_totp(
    data: TOTPDisableSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(AuthService.get_current_user),
):
    if not current_user.totp_enabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="2FA is not enabled")
    if not verify_password(data.password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    current_user.totp_secret = None
    current_user.totp_enabled = False
    db.commit()
    ActivityLogService.record(db, user_id=str(current_user.id), action="disable", entity_type="totp", entity_id=str(current_user.id))
    return {"message": "2FA disabled successfully"}
