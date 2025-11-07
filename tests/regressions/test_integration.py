"""
Simple API integration tests to verify endpoints work correctly.

These tests require the backend service to be running at http://localhost:8000

Run with: python -m pytest tests/regressions/test_integration.py -v -m integration
"""

import pytest
import requests
import time

pytestmark = pytest.mark.integration

BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test that the API is up and running."""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200


def test_metrics_endpoint():
    """Test that metrics endpoint is accessible."""
    response = requests.get(f"{BASE_URL}/metrics")
    assert response.status_code == 200
    assert "request_count" in response.text


def test_docs_endpoint():
    """Test that OpenAPI docs are accessible."""
    response = requests.get(f"{BASE_URL}/docs")
    assert response.status_code == 200
    assert "MyTodoApp" in response.text


def test_create_and_get_project():
    """Test creating and retrieving a project."""
    # Create project
    project_data = {
        "name": "Integration Test Project",
        "description": "Test project",
        "status": "active",
    }
    create_response = requests.post(f"{BASE_URL}/projects", json=project_data)
    assert create_response.status_code == 200
    created_project = create_response.json()
    assert "id" in created_project
    assert created_project["name"] == project_data["name"]

    # Get project
    project_id = created_project["id"]
    get_response = requests.get(f"{BASE_URL}/projects/{project_id}")
    assert get_response.status_code == 200
    retrieved_project = get_response.json()
    assert retrieved_project["id"] == project_id
    assert retrieved_project["name"] == project_data["name"]

    return project_id


def test_create_and_update_todo():
    """Test creating and updating a todo."""
    # Create todo
    todo_data = {
        "title": "Integration Test Todo",
        "description": "Test todo",
        "priority": "high",
        "status": "pending",
    }
    create_response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    assert create_response.status_code == 201
    created_todo = create_response.json()
    assert "id" in created_todo
    assert created_todo["title"] == todo_data["title"]

    # Update todo
    todo_id = created_todo["id"]
    update_data = {
        "title": "Updated Todo",
        "description": "Updated description",
        "priority": "low",
        "status": "completed",
    }
    update_response = requests.put(f"{BASE_URL}/todos/{todo_id}", json=update_data)
    assert update_response.status_code == 200
    updated_todo = update_response.json()
    assert updated_todo["title"] == update_data["title"]
    assert updated_todo["status"] == "completed"
    assert updated_todo["completed_at"] is not None

    return todo_id


def test_get_all_todos():
    """Test retrieving all todos."""
    response = requests.get(f"{BASE_URL}/todos")
    assert response.status_code == 200
    todos = response.json()
    assert isinstance(todos, list)


def test_get_all_projects():
    """Test retrieving all projects."""
    response = requests.get(f"{BASE_URL}/projects")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)


def test_todo_with_project():
    """Test creating a todo associated with a project."""
    # Create project first
    project_id = test_create_and_get_project()

    # Create todo with project
    todo_data = {
        "title": "Todo in Project",
        "priority": "medium",
        "status": "pending",
        "project_id": project_id,
    }
    response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    assert response.status_code == 201
    todo = response.json()
    assert todo["project_id"] == project_id


def test_delete_todo():
    """Test deleting a todo."""
    # Create a new todo for deletion test
    todo_data = {
        "title": "To Be Deleted",
        "priority": "low",
        "status": "pending",
    }
    create_response = requests.post(f"{BASE_URL}/todos", json=todo_data)
    assert create_response.status_code == 201
    todo_id = create_response.json()["id"]

    # Delete todo
    delete_response = requests.delete(f"{BASE_URL}/todos/{todo_id}")
    assert delete_response.status_code == 200

    # Verify deleted
    get_response = requests.get(f"{BASE_URL}/todos/{todo_id}")
    assert get_response.status_code == 404


def test_update_project():
    """Test updating a project."""
    # Create project first
    project_id = test_create_and_get_project()

    # Update project
    update_data = {
        "name": "Updated Project",
        "description": "Updated description",
        "status": "completed",
    }
    update_response = requests.put(f"{BASE_URL}/projects/{project_id}", json=update_data)
    assert update_response.status_code == 200
    updated_project = update_response.json()
    assert updated_project["name"] == update_data["name"]
    assert updated_project["status"] == "completed"


def test_404_on_nonexistent_todo():
    """Test that requesting non-existent todo returns 404."""
    response = requests.get(f"{BASE_URL}/todos/999999")
    assert response.status_code == 404


def test_404_on_nonexistent_project():
    """Test that requesting non-existent project returns 404."""
    response = requests.get(f"{BASE_URL}/projects/999999")
    assert response.status_code == 404


def test_validation_error_on_invalid_todo():
    """Test that invalid todo data returns 422."""
    invalid_data = {
        # Missing required title
        "priority": "invalid_priority",
        "status": "pending",
    }
    response = requests.post(f"{BASE_URL}/todos", json=invalid_data)
    assert response.status_code == 422


if __name__ == "__main__":
    print("Running integration tests against", BASE_URL)
    print("Make sure the backend is running!")
    time.sleep(1)

    test_health_check()
    print("✓ Health check passed")

    test_metrics_endpoint()
    print("✓ Metrics endpoint passed")

    test_docs_endpoint()
    print("✓ Docs endpoint passed")

    test_get_all_projects()
    print("✓ Get all projects passed")

    test_get_all_todos()
    print("✓ Get all todos passed")

    project_id = test_create_and_get_project()
    print("✓ Create and get project passed")

    todo_id = test_create_and_update_todo()
    print("✓ Create and update todo passed")

    test_todo_with_project()
    print("✓ Todo with project passed")

    test_update_project()
    print("✓ Update project passed")

    test_delete_todo()
    print("✓ Delete todo passed")

    test_404_on_nonexistent_todo()
    print("✓ 404 on nonexistent todo passed")

    test_404_on_nonexistent_project()
    print("✓ 404 on nonexistent project passed")

    test_validation_error_on_invalid_todo()
    print("✓ Validation error on invalid todo passed")

    print("\n✅ All integration tests passed!")
