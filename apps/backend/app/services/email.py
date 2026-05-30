import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from app.core.config import settings


def _build_message(to: str, subject: str, html: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{settings.EMAIL_FROM_NAME} <{settings.EMAIL_FROM}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(html, "html"))
    return msg


def send_email(to: str, subject: str, html: str) -> bool:
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        return False

    msg = _build_message(to, subject, html)
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.EMAIL_FROM, [to], msg.as_string())
        return True
    except Exception:
        return False


def send_confirmation_email(to: str, token: str) -> bool:
    link = f"{settings.BASE_URL}/confirm-email?token={token}"
    html = f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#0f0f13;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:48px 16px">
<table width="480" cellpadding="0" cellspacing="0" style="background:#1a1a23;border-radius:16px;border:1px solid #2a2a35">
<tr><td style="padding:40px 32px 32px">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding-bottom:8px">
<span style="display:inline-block;width:40px;height:40px;line-height:40px;text-align:center;border-radius:12px;background:linear-gradient(135deg,#a78bfa,#e879f9);color:#fff;font-size:18px;font-weight:700">S</span>
</td></tr>
<tr><td align="center" style="padding-bottom:24px">
<h1 style="margin:0;font-size:22px;font-weight:600;color:#f1f5f9">Confirm your email</h1>
</td></tr>
<tr><td style="padding-bottom:24px">
<p style="margin:0;font-size:15px;line-height:1.6;color:#94a3b8">Thanks for signing up for Simplernote. Click the button below to confirm your email address and get started.</p>
</td></tr>
<tr><td align="center" style="padding-bottom:24px">
<a href="{link}" style="display:inline-block;padding:14px 32px;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#d946ef);color:#fff;font-size:15px;font-weight:600;text-decoration:none">Confirm email</a>
</td></tr>
<tr><td style="padding-bottom:8px">
<p style="margin:0;font-size:13px;line-height:1.5;color:#64748b">Or paste this link in your browser:</p>
<p style="margin:4px 0 0;font-size:12px;color:#475569;word-break:break-all">{link}</p>
</td></tr>
</table>
</td></tr>
</table>
</td></tr></table>
</body>
</html>"""
    return send_email(to, "Confirm your Simplernote account", html)


def send_password_reset_email(to: str, token: str) -> bool:
    link = f"{settings.BASE_URL}/reset-password?token={token}"
    html = f"""\
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#0f0f13;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif">
<table width="100%" cellpadding="0" cellspacing="0"><tr><td align="center" style="padding:48px 16px">
<table width="480" cellpadding="0" cellspacing="0" style="background:#1a1a23;border-radius:16px;border:1px solid #2a2a35">
<tr><td style="padding:40px 32px 32px">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td align="center" style="padding-bottom:8px">
<span style="display:inline-block;width:40px;height:40px;line-height:40px;text-align:center;border-radius:12px;background:linear-gradient(135deg,#a78bfa,#e879f9);color:#fff;font-size:18px;font-weight:700">S</span>
</td></tr>
<tr><td align="center" style="padding-bottom:24px">
<h1 style="margin:0;font-size:22px;font-weight:600;color:#f1f5f9">Reset your password</h1>
</td></tr>
<tr><td style="padding-bottom:24px">
<p style="margin:0;font-size:15px;line-height:1.6;color:#94a3b8">We received a request to reset the password for your Simplernote account. Click the button below to choose a new password.</p>
</td></tr>
<tr><td align="center" style="padding-bottom:24px">
<a href="{link}" style="display:inline-block;padding:14px 32px;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#d946ef);color:#fff;font-size:15px;font-weight:600;text-decoration:none">Reset password</a>
</td></tr>
<tr><td style="padding-bottom:8px">
<p style="margin:0;font-size:13px;line-height:1.5;color:#64748b">Or paste this link in your browser:</p>
<p style="margin:4px 0 0;font-size:12px;color:#475569;word-break:break-all">{link}</p>
</td></tr>
<tr><td style="padding-top:16px">
<p style="margin:0;font-size:13px;line-height:1.5;color:#64748b">If you didn't request this, you can safely ignore this email.</p>
</td></tr>
</table>
</td></tr>
</table>
</td></tr></table>
</body>
</html>"""
    return send_email(to, "Reset your Simplernote password", html)
