import pytest


class TestAiContext:
    def test_create(self, client, auth_header, project_id):
        resp = client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Project context for AI agents",
        }, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["content"] == "Project context for AI agents"
        assert str(data["project_id"]) == project_id

    def test_create_duplicate(self, client, auth_header, project_id):
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "First context",
        }, headers=auth_header)
        resp = client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Duplicate context",
        }, headers=auth_header)
        assert resp.status_code == 409

    def test_get_by_project(self, client, auth_header, project_id):
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Context content",
        }, headers=auth_header)
        resp = client.get(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["content"] == "Context content"

    def test_get_by_project_not_found(self, client, auth_header, project_id):
        resp = client.get(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 404

    def test_update(self, client, auth_header, project_id):
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Original",
        }, headers=auth_header)
        resp = client.patch(f"/api/projects/{project_id}/ai-context", json={
            "content": "Updated content",
        }, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["content"] == "Updated content"

    def test_delete(self, client, auth_header, project_id):
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "To delete",
        }, headers=auth_header)
        resp = client.delete(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 204
        resp = client.get(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 404
