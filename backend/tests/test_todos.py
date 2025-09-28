from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos", json={"title": "Test Todo", "priority": "low", "status": "undone"})
    assert response.status_code == 201
    assert response.json()["title"] == "Test Todo"

def test_get_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_todo():
    # Create a todo to get
    response = client.post("/todos", json={"title": "Test Todo 2", "priority": "low", "status": "undone"})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

def test_update_todo():
    # Create a todo to update
    response = client.post("/todos", json={"title": "Test Todo 3", "priority": "low", "status": "undone"})
    todo_id = response.json()["id"]
    response = client.put(f"/todos/{todo_id}", json={"title": "Updated Todo", "status": "done"})
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"
