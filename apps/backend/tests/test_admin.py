import pytest


class TestAdmin:
    def test_list_users_as_admin(self, client, admin_setup):
        token, headers = admin_setup
        resp = client.get("/api/admin/users", headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        user = data[0]
        assert "created_at" in user
        assert "last_login_at" in user
        assert "email_confirmed" in user

    def test_list_users_denied_for_user(self, client, auth_header):
        resp = client.get("/api/admin/users", headers=auth_header)
        assert resp.status_code == 403

    def test_promote_user(self, client, user_data, user_token, admin_setup):
        _, admin_headers = admin_setup
        uid = client.get("/api/auth/me", headers={"Authorization": f"Bearer {user_token}"}).json()["id"]
        resp = client.patch(f"/api/admin/users/{uid}/role", json={"role": "admin"}, headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["role"] == "admin"

    def test_demote_user(self, client, user_data, user_token, admin_setup):
        _, admin_headers = admin_setup
        uid = client.get("/api/auth/me", headers={"Authorization": f"Bearer {user_token}"}).json()["id"]
        client.patch(f"/api/admin/users/{uid}/role", json={"role": "admin"}, headers=admin_headers)
        resp = client.patch(f"/api/admin/users/{uid}/role", json={"role": "user"}, headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["role"] == "user"

    def test_cannot_self_demote(self, client, admin_setup):
        token, admin_headers = admin_setup
        admin_id = client.get("/api/auth/me", headers=admin_headers).json()["id"]
        resp = client.patch(f"/api/admin/users/{admin_id}/role",
                            json={"role": "user"}, headers=admin_headers)
        assert resp.status_code == 400

    def test_delete_user(self, client, user_data, admin_setup):
        token, admin_headers = admin_setup
        resp = client.post("/api/auth/register", json={
            "email": "delete_me@example.com",
            "password": "DeleteMe1!",
            "first_name": "Delete",
            "last_name": "Me",
            "country": "US",
            "city": "NYC",
        })
        uid = resp.json()["id"]
        resp = client.delete(f"/api/admin/users/{uid}", headers=admin_headers)
        assert resp.status_code == 204
