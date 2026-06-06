class TestAiContextSearch:
    def test_ai_context_search_includes_contexts(self, client, auth_header, project_id):
        client.post(
            f"/api/projects/{project_id}/contexts",
            json={"name": "needle-context", "content": "This context contains the needle keyword."},
            headers=auth_header,
        )
        client.post(
            f"/api/projects/{project_id}/notes",
            json={"title": "Needle note", "content": "This note also has the needle keyword.", "note_type": "documentation"},
            headers=auth_header,
        )
        client.post(
            f"/api/projects/{project_id}/tasks",
            json={"title": "Needle task", "description": "This task includes the needle keyword.", "status": "todo", "priority": "medium"},
            headers=auth_header,
        )

        resp = client.get(f"/api/ai-context/search?query=needle&project_id={project_id}", headers=auth_header)
        assert resp.status_code == 200

        data = resp.json()
        types = {item["type"] for item in data}
        assert {"note", "task", "context"}.issubset(types)
        assert any(item["type"] == "context" and item["title"] == "needle-context" for item in data)

    def test_ai_agent_search_includes_contexts(self, client, auth_header, project_id):
        client.post(
            f"/api/projects/{project_id}/contexts",
            json={"name": "agent-context", "content": "Agent searchable content."},
            headers=auth_header,
        )

        api_key = client.post(
            "/api/api-keys",
            json={
                "name": "Search Key",
                "project_id": project_id,
                "permissions": {
                    "read_notes": True,
                    "read_tasks": True,
                    "read_ai_context": True,
                },
            },
            headers=auth_header,
        ).json()["plain_text_key"]

        resp = client.get(
            f"/api/ai-agent/search?query=agent&project_id={project_id}",
            headers={"X-API-KEY": api_key},
        )
        assert resp.status_code == 200

        data = resp.json()
        assert any(item["type"] == "context" and item["title"] == "agent-context" for item in data)
