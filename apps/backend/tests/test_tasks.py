import pytest


class TestTasks:
    def test_create_task(self, client, auth_header, task_data):
        resp = client.post("/api/tasks", json=task_data, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == task_data["title"]
        assert data["status"] == task_data["status"]
        assert data["priority"] == task_data["priority"]
        assert "id" in data

    def test_create_task_defaults(self, client, auth_header, project_id):
        resp = client.post("/api/tasks", json={
            "project_id": project_id,
            "title": "Default Task",
        }, headers=auth_header)
        assert resp.status_code == 201
        assert resp.json()["status"] == "todo"
        assert resp.json()["priority"] == "medium"

    def test_create_task_invalid_status(self, client, auth_header, project_id):
        resp = client.post("/api/tasks", json={
            "project_id": project_id,
            "title": "Bad Status",
            "status": "invalid-status",
        }, headers=auth_header)
        assert resp.status_code == 422

    def test_create_task_invalid_priority(self, client, auth_header, project_id):
        resp = client.post("/api/tasks", json={
            "project_id": project_id,
            "title": "Bad Priority",
            "priority": "urgent",
        }, headers=auth_header)
        assert resp.status_code == 422

    def test_unauthorized(self, client, task_data):
        resp = client.post("/api/tasks", json=task_data)
        assert resp.status_code == 401

    def test_list_tasks(self, client, auth_header, task_data):
        client.post("/api/tasks", json=task_data, headers=auth_header)
        resp = client.get("/api/tasks", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_list_tasks_filter_project(self, client, auth_header, task_data, project_id):
        client.post("/api/tasks", json=task_data, headers=auth_header)
        resp = client.get(f"/api/tasks?project_id={project_id}", headers=auth_header)
        assert resp.status_code == 200
        for t in resp.json():
            assert str(t["project_id"]) == project_id

    def test_list_tasks_filter_status(self, client, auth_header, task_data, project_id):
        client.post("/api/tasks", json=task_data, headers=auth_header)
        resp = client.get(f"/api/tasks?project_id={project_id}&status=todo", headers=auth_header)
        assert resp.status_code == 200
        assert len(resp.json()) >= 1

    def test_get_task(self, client, auth_header, task_data):
        created = client.post("/api/tasks", json=task_data, headers=auth_header).json()
        resp = client.get(f"/api/tasks/{created['id']}", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_task_not_found(self, client, auth_header):
        resp = client.get("/api/tasks/00000000-0000-0000-0000-000000000000", headers=auth_header)
        assert resp.status_code == 404

    def test_update_task(self, client, auth_header, task_data):
        created = client.post("/api/tasks", json=task_data, headers=auth_header).json()
        resp = client.patch(f"/api/tasks/{created['id']}", json={
            "title": "Updated Task",
            "status": "in-progress",
        }, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated Task"
        assert resp.json()["status"] == "in-progress"

    def test_delete_task(self, client, auth_header, task_data):
        created = client.post("/api/tasks", json=task_data, headers=auth_header).json()
        resp = client.delete(f"/api/tasks/{created['id']}", headers=auth_header)
        assert resp.status_code == 204
        resp = client.get(f"/api/tasks/{created['id']}", headers=auth_header)
        assert resp.status_code == 404
