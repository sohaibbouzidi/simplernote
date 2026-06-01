from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from app.core.config import settings


def get_tz() -> ZoneInfo:
    return ZoneInfo(settings.TIMEZONE)


def now() -> datetime:
    return datetime.now(get_tz())


def localize(dt: datetime) -> datetime:
    return dt.astimezone(get_tz())
