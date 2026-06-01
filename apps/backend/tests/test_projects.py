import pytest


class TestProjects:
    def test_create_project(self, client, auth_header, project_data):
        resp = client.post("/api/projects", json=project_data, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == project_data["name"]
        assert data["description"] == project_data["description"]
        assert "id" in data
        assert "created_by" in data

    def test_create_project_minimal(self, client, auth_header):
        resp = client.post("/api/projects", json={"name": "Minimal"}, headers=auth_header)
        assert resp.status_code == 201
        assert resp.json()["name"] == "Minimal"

    def test_create_project_unauthorized(self, client, project_data):
        resp = client.post("/api/projects", json=project_data)
        assert resp.status_code == 401

    def test_list_projects(self, client, auth_header, project_data):
        client.post("/api/projects", json=project_data, headers=auth_header)
        client.post("/api/projects", json={"name": "Project 2"}, headers=auth_header)
        resp = client.get("/api/projects", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_list_projects_empty(self, client, auth_header):
        resp = client.get("/api/projects", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_get_project(self, client, auth_header, user_project):
        pid = user_project["id"]
        resp = client.get(f"/api/projects/{pid}", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["id"] == pid

    def test_get_project_not_found(self, client, auth_header):
        resp = client.get("/api/projects/00000000-0000-0000-0000-000000000000", headers=auth_header)
        assert resp.status_code == 404

    def test_update_project(self, client, auth_header, user_project):
        pid = user_project["id"]
        resp = client.patch(f"/api/projects/{pid}", json={"name": "Updated"}, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Updated"

    def test_delete_project(self, client, auth_header, user_project):
        pid = user_project["id"]
        resp = client.delete(f"/api/projects/{pid}", headers=auth_header)
        assert resp.status_code == 204
        resp = client.get(f"/api/projects/{pid}", headers=auth_header)
        assert resp.status_code == 404

    def test_cannot_access_other_users_project(self, client, user_data, auth_header, db):
        from app.models.user import User
        client.post("/api/auth/register", json={
            "email": "other@example.com",
            "password": "OtherPass1!",
            "first_name": "Other",
            "last_name": "User",
            "country": "UK",
            "city": "London",
        })
        other_user = db.query(User).filter(User.email == "other@example.com").first()
        other_user.email_confirmed = True
        db.commit()
        login = client.post("/api/auth/login", json={"email": "other@example.com", "password": "OtherPass1!"})
        other_token = login.json()["access_token"]

        project = client.post("/api/projects", json={"name": "My Project"}, headers=auth_header).json()
        resp = client.get(f"/api/projects/{project['id']}", headers={"Authorization": f"Bearer {other_token}"})
        assert resp.status_code == 404
