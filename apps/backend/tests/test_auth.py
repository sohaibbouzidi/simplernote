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
