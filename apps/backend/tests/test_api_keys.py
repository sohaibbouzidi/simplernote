import pytest


class TestApiKeys:
    def test_create_api_key(self, client, auth_header, project_id):
        resp = client.post("/api/api-keys", json={
            "name": "Test Key",
            "project_id": project_id,
            "permissions": {"read_notes": True, "write_notes": True},
        }, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Test Key"
        assert "plain_text_key" in data
        assert data["plain_text_key"].startswith("sk_")

    def test_create_api_key_no_permissions(self, client, auth_header, project_id):
        resp = client.post("/api/api-keys", json={
            "name": "No Perms",
            "project_id": project_id,
        }, headers=auth_header)
        assert resp.status_code == 201
        assert resp.json()["permissions"] == {}

    def test_create_duplicate_key(self, client, auth_header, project_id):
        client.post("/api/api-keys", json={
            "name": "First",
            "project_id": project_id,
        }, headers=auth_header)
        resp = client.post("/api/api-keys", json={
            "name": "Second",
            "project_id": project_id,
        }, headers=auth_header)
        assert resp.status_code == 409

    def test_list_keys(self, client, auth_header, project_id):
        client.post("/api/api-keys", json={
            "name": "Key 1",
            "project_id": project_id,
        }, headers=auth_header)
        resp = client.get(f"/api/api-keys/project/{project_id}", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        assert resp.json()[0]["name"] == "Key 1"

    def test_list_keys_empty(self, client, auth_header, project_id):
        resp = client.get(f"/api/api-keys/project/{project_id}", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_delete_api_key(self, client, auth_header, project_id):
        created = client.post("/api/api-keys", json={
            "name": "To Delete",
            "project_id": project_id,
        }, headers=auth_header).json()
        resp = client.delete(f"/api/api-keys/{created['id']}", headers=auth_header)
        assert resp.status_code == 204
        resp = client.get(f"/api/api-keys/project/{project_id}", headers=auth_header)
        assert resp.json() == []
