import pytest


class TestAuth:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "newuser@example.com",
            "password": "ValidPass1!",
            "first_name": "Jane",
            "last_name": "Doe",
            "country": "CA",
            "city": "Toronto",
        })
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "newuser@example.com"
        assert data["first_name"] == "Jane"
        assert data["email_confirmed"] is False
        assert "id" in data

    def test_register_duplicate_email(self, client, user_data):
        client.post("/api/auth/register", json=user_data)
        resp = client.post("/api/auth/register", json=user_data)
        assert resp.status_code == 400
        assert "already" in resp.json()["detail"].lower()

    def test_register_weak_password(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "weak@example.com",
            "password": "short",
            "first_name": "Weak",
            "last_name": "Pass",
            "country": "US",
            "city": "NYC",
        })
        assert resp.status_code == 400
        detail = resp.json()["detail"].lower()
        assert "password" in detail

    def test_register_missing_required_fields(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "missing@example.com",
            "password": "ValidPass1!",
        })
        assert resp.status_code == 422

    def test_login_success(self, client, user_data):
        client.post("/api/auth/register", json=user_data)
        resp = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"],
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_updates_last_login_at(self, client, user_data):
        client.post("/api/auth/register", json=user_data)
        token = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"],
        }).json()["access_token"]
        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).json()
        assert me["last_login_at"] is not None

    def test_login_wrong_password(self, client, user_data):
        client.post("/api/auth/register", json=user_data)
        resp = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": "WrongPass1!",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/api/auth/login", json={
            "email": "nobody@example.com",
            "password": "AnyPass1!",
        })
        assert resp.status_code == 401

    def test_change_password_success(self, client, user_data, auth_header):
        client.post("/api/auth/register", json=user_data)
        resp = client.patch("/api/auth/password", json={
            "old_password": user_data["password"],
            "new_password": "NewValid1!",
        }, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["message"] == "Password updated successfully"

    def test_change_password_wrong_old(self, client, user_data, auth_header):
        client.post("/api/auth/register", json=user_data)
        resp = client.patch("/api/auth/password", json={
            "old_password": "WrongOld1!",
            "new_password": "NewValid1!",
        }, headers=auth_header)
        assert resp.status_code == 400

    def test_change_password_weak_new(self, client, user_data, auth_header):
        client.post("/api/auth/register", json=user_data)
        resp = client.patch("/api/auth/password", json={
            "old_password": user_data["password"],
            "new_password": "weak",
        }, headers=auth_header)
        assert resp.status_code == 400

    def test_me_endpoint(self, client, user_data, auth_header):
        client.post("/api/auth/register", json=user_data)
        resp = client.get("/api/auth/me", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["email"] == user_data["email"]
        assert "email_confirmed" in resp.json()

    def test_me_without_token(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_refresh_token(self, client, user_data):
        client.post("/api/auth/register", json=user_data)
        login_resp = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"],
        })
        refresh = login_resp.json()["refresh_token"]
        resp = client.post("/api/auth/refresh", json={"refresh_token": refresh})
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_confirm_email(self, client, user_data):
        register_resp = client.post("/api/auth/register", json=user_data)
        assert register_resp.status_code == 201
        assert register_resp.json()["email_confirmed"] is False
        me_resp = client.post("/api/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"],
        })
        token = me_resp.json()["access_token"]
        me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me.json()["email_confirmed"] is False
        # Without SMTP configured, the email send is a no-op
        # We test the endpoint directly via /me checking email_confirmed is False
        resp = client.post("/api/auth/confirm-email", json={"token": "invalid-token"})
        assert resp.status_code == 400

    def test_forgot_password(self, client, user_data):
        client.post("/api/auth/register", json=user_data)
        resp = client.post("/api/auth/forgot-password", json={"email": user_data["email"]})
        assert resp.status_code == 200
        assert "sent" in resp.json()["message"].lower()

    def test_forgot_password_nonexistent(self, client):
        resp = client.post("/api/auth/forgot-password", json={"email": "noone@example.com"})
        assert resp.status_code == 200
        assert "sent" in resp.json()["message"].lower()

    def test_reset_password_invalid_token(self, client):
        resp = client.post("/api/auth/reset-password", json={
            "token": "invalid-token",
            "new_password": "NewValid1!",
        })
        assert resp.status_code == 400

    def test_resend_confirmation_smtp_unset(self, client, user_data):
        from app.core.config import settings
        original = settings.SMTP_HOST
        settings.SMTP_HOST = None
        try:
            client.post("/api/auth/register", json=user_data)
            resp = client.post("/api/auth/resend-confirmation", json={"email": user_data["email"]})
            assert resp.status_code == 400
            assert "not configured" in resp.json()["detail"].lower()
        finally:
            settings.SMTP_HOST = original

    def test_resend_confirmation_unknown_email(self, client):
        resp = client.post("/api/auth/resend-confirmation", json={"email": "unknown@example.com"})
        assert resp.status_code == 200
        assert "sent" in resp.json()["message"].lower()

    def test_login_blocked_when_enforcing(self, client, user_data):
        from app.core.config import settings
        settings.ENFORCE_EMAIL_CONFIRMATION = True
        try:
            client.post("/api/auth/register", json=user_data)
            resp = client.post("/api/auth/login", json={
                "email": user_data["email"],
                "password": user_data["password"],
            })
            assert resp.status_code == 403
            assert "confirm" in resp.json()["detail"].lower()
        finally:
            settings.ENFORCE_EMAIL_CONFIRMATION = False

    def test_login_allowed_when_enforcing_and_confirmed(self, client, user_data, db):
        from app.core.config import settings
        from app.models.user import User
        test_email = "confirmed@example.com"
        client.post("/api/auth/register", json={**user_data, "email": test_email})
        user = db.query(User).filter(User.email == test_email).first()
        user.email_confirmed = True
        db.commit()
        settings.ENFORCE_EMAIL_CONFIRMATION = True
        try:
            resp = client.post("/api/auth/login", json={
                "email": test_email,
                "password": user_data["password"],
            })
            assert resp.status_code == 200
            assert "access_token" in resp.json()
        finally:
            settings.ENFORCE_EMAIL_CONFIRMATION = False
