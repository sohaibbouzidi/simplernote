import pytest


class TestAiContext:
    def test_create(self, client, auth_header, project_id):
        resp = client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "architecture",
            "content": "Project context for AI agents",
        }, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["content"] == "Project context for AI agents"
        assert data["name"] == "architecture"
        assert str(data["project_id"]) == project_id

    def test_create_duplicate(self, client, auth_header, project_id):
        client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "default",
            "content": "First context",
        }, headers=auth_header)
        resp = client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "default",
            "content": "Duplicate context",
        }, headers=auth_header)
        assert resp.status_code == 409

    def test_get_by_project(self, client, auth_header, project_id):
        ctx_resp = client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "test-context",
            "content": "Context content",
        }, headers=auth_header)
        ctx_id = ctx_resp.json()["id"]
        
        resp = client.get(f"/api/projects/{project_id}/contexts/{ctx_id}", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["content"] == "Context content"
        assert resp.json()["name"] == "test-context"

    def test_get_by_project_not_found(self, client, auth_header, project_id):
        resp = client.get(f"/api/projects/{project_id}/contexts", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_list_contexts(self, client, auth_header, project_id):
        # Create multiple contexts
        client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "context1",
            "content": "Content 1",
        }, headers=auth_header)
        client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "context2",
            "content": "Content 2",
        }, headers=auth_header)
        
        resp = client.get(f"/api/projects/{project_id}/contexts", headers=auth_header)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        names = {ctx["name"] for ctx in data}
        assert names == {"context1", "context2"}

    def test_update(self, client, auth_header, project_id):
        ctx_resp = client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "original",
            "content": "Original",
        }, headers=auth_header)
        ctx_id = ctx_resp.json()["id"]
        
        resp = client.patch(f"/api/projects/{project_id}/contexts/{ctx_id}", json={
            "content": "Updated content",
        }, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["content"] == "Updated content"
        assert resp.json()["name"] == "original"

    def test_delete(self, client, auth_header, project_id):
        ctx_resp = client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "to-delete",
            "content": "To delete",
        }, headers=auth_header)
        ctx_id = ctx_resp.json()["id"]
        
        resp = client.delete(f"/api/projects/{project_id}/contexts/{ctx_id}", headers=auth_header)
        assert resp.status_code == 204
        
        resp = client.get(f"/api/projects/{project_id}/contexts/{ctx_id}", headers=auth_header)
        assert resp.status_code == 404

    def test_restore(self, client, auth_header, project_id):
        ctx_resp = client.post(f"/api/projects/{project_id}/contexts", json={
            "name": "to-restore",
            "content": "To restore",
        }, headers=auth_header)
        ctx_id = ctx_resp.json()["id"]
        
        # Delete
        client.delete(f"/api/projects/{project_id}/contexts/{ctx_id}", headers=auth_header)
        
        # Restore
        resp = client.post(f"/api/projects/{project_id}/contexts/{ctx_id}/restore", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["name"] == "to-restore"

    # Backwards compatibility tests
    def test_deprecated_create(self, client, auth_header, project_id):
        """Test old endpoint still works for backwards compatibility."""
        resp = client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Legacy context",
        }, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["content"] == "Legacy context"
        assert data["name"] == "default"

    def test_deprecated_get(self, client, auth_header, project_id):
        """Test old GET endpoint."""
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Legacy content",
        }, headers=auth_header)
        resp = client.get(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["content"] == "Legacy content"
        assert resp.json()["name"] == "default"

    def test_deprecated_update(self, client, auth_header, project_id):
        """Test old PATCH endpoint."""
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "Original",
        }, headers=auth_header)
        resp = client.patch(f"/api/projects/{project_id}/ai-context", json={
            "content": "Updated",
        }, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["content"] == "Updated"

    def test_deprecated_delete(self, client, auth_header, project_id):
        """Test old DELETE endpoint."""
        client.post(f"/api/projects/{project_id}/ai-context", json={
            "content": "To delete",
        }, headers=auth_header)
        resp = client.delete(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 204
        
        resp = client.get(f"/api/projects/{project_id}/ai-context", headers=auth_header)
        assert resp.status_code == 404

