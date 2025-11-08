from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_project():
    response = client.post("/projects", json={"name": "Test Project", "status": "undone"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Project"


def test_get_projects():
    response = client.get("/projects")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_project():
    # Create a project to get
    response = client.post("/projects", json={"name": "Test Project 2", "status": "undone"})
    project_id = response.json()["id"]
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id


def test_update_project():
    # Create a project to update
    response = client.post("/projects", json={"name": "Test Project 3", "status": "undone"})
    project_id = response.json()["id"]
    response = client.put(f"/projects/{project_id}", json={"name": "Updated Project", "status": "done"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project"
