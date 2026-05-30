import pytest


class TestNotes:
    def test_create_note(self, client, auth_header, note_data):
        resp = client.post("/api/notes", json=note_data, headers=auth_header)
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == note_data["title"]
        assert data["content"] == note_data["content"]
        assert data["note_type"] == note_data["note_type"]
        assert "id" in data
        assert str(data["project_id"]) == note_data["project_id"]

    def test_create_note_default_type(self, client, auth_header, project_id):
        resp = client.post("/api/notes", json={
            "project_id": project_id,
            "title": "Default Type Note",
        }, headers=auth_header)
        assert resp.status_code == 201
        assert resp.json()["note_type"] == "documentation"

    def test_create_note_invalid_type(self, client, auth_header, project_id):
        resp = client.post("/api/notes", json={
            "project_id": project_id,
            "title": "Bad Type",
            "note_type": "invalid-type",
        }, headers=auth_header)
        assert resp.status_code == 422

    def test_list_notes(self, client, auth_header, note_data):
        client.post("/api/notes", json=note_data, headers=auth_header)
        resp = client.get("/api/notes", headers=auth_header)
        assert resp.status_code == 200
        notes = resp.json()
        assert len(notes) >= 1

    def test_list_notes_filter_by_project(self, client, auth_header, note_data, project_id):
        client.post("/api/notes", json=note_data, headers=auth_header)
        resp = client.get(f"/api/notes?project_id={project_id}", headers=auth_header)
        assert resp.status_code == 200
        for note in resp.json():
            assert str(note["project_id"]) == project_id

    def test_get_note(self, client, auth_header, note_data):
        created = client.post("/api/notes", json=note_data, headers=auth_header).json()
        resp = client.get(f"/api/notes/{created['id']}", headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["id"] == created["id"]

    def test_get_note_not_found(self, client, auth_header):
        resp = client.get("/api/notes/00000000-0000-0000-0000-000000000000", headers=auth_header)
        assert resp.status_code == 404

    def test_update_note(self, client, auth_header, note_data):
        created = client.post("/api/notes", json=note_data, headers=auth_header).json()
        resp = client.patch(f"/api/notes/{created['id']}", json={
            "title": "Updated Title",
            "content": "<p>Updated content</p>",
        }, headers=auth_header)
        assert resp.status_code == 200
        assert resp.json()["title"] == "Updated Title"

    def test_delete_note(self, client, auth_header, note_data):
        created = client.post("/api/notes", json=note_data, headers=auth_header).json()
        resp = client.delete(f"/api/notes/{created['id']}", headers=auth_header)
        assert resp.status_code == 204
        resp = client.get(f"/api/notes/{created['id']}", headers=auth_header)
        assert resp.status_code == 404
