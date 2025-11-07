"""
Comprehensive API regression tests for Projects endpoints.

This module tests all project endpoints including:
- CRUD operations
- Edge cases
- Error handling
- Data validation
"""

import pytest
from datetime import datetime


def test_create_project_success(client, test_db):
    """Test creating a new project with valid data."""
    project_data = {
        "name": "Test Project",
        "description": "Test project description",
        "status": "active",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]
    assert data["description"] == project_data["description"]
    assert data["status"] == project_data["status"]
    assert "id" in data


def test_create_project_minimal(client, test_db):
    """Test creating a project with only required fields."""
    project_data = {
        "name": "Minimal Project",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == project_data["name"]
    assert "id" in data


def test_create_project_missing_name(client, test_db):
    """Test that creating a project without name fails."""
    project_data = {
        "description": "No name project",
        "status": "active",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 422  # Validation error


@pytest.mark.xfail(reason="SQLite does not enforce ENUM constraints")
def test_create_project_invalid_status(client, test_db):
    """Test that invalid status values are rejected."""
    project_data = {
        "name": "Bad Status Project",
        "status": "invalid_status",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 422


def test_get_all_projects(client, test_db, sample_projects):
    """Test retrieving all projects."""
    response = client.get("/projects")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= len(sample_projects)


def test_get_projects_with_pagination(client, test_db, sample_projects):
    """Test pagination parameters for projects."""
    response = client.get("/projects?skip=0&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert len(data) <= 2


def test_get_project_by_id(client, test_db, sample_projects):
    """Test retrieving a specific project by ID."""
    project_id = sample_projects[0]["id"]
    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id


def test_get_project_not_found(client, test_db):
    """Test that requesting non-existent project returns 404."""
    response = client.get("/projects/99999")
    assert response.status_code == 404


def test_update_project(client, test_db, sample_projects):
    """Test updating an existing project."""
    project_id = sample_projects[0]["id"]
    update_data = {
        "name": "Updated Project Name",
        "description": "Updated Description",
        "status": "completed",
    }
    response = client.put(f"/projects/{project_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["status"] == update_data["status"]


def test_update_project_not_found(client, test_db):
    """Test that updating non-existent project returns 404."""
    update_data = {
        "name": "Not Found Project",
        "status": "active",
    }
    response = client.put("/projects/99999", json=update_data)
    assert response.status_code == 404


def test_update_project_name_only(client, test_db, sample_projects):
    """Test updating only the project name."""
    project_id = sample_projects[0]["id"]
    original_desc = sample_projects[0].get("description", "")

    update_data = {
        "name": "New Name Only",
    }
    response = client.put(f"/projects/{project_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]


def test_project_with_very_long_name(client, test_db):
    """Test handling of very long project names."""
    long_name = "P" * 500
    project_data = {
        "name": long_name,
        "status": "active",
    }
    response = client.post("/projects", json=project_data)
    # Should either succeed or return validation error
    assert response.status_code in [200, 422]


def test_project_with_special_characters(client, test_db):
    """Test handling of special characters in project fields."""
    project_data = {
        "name": "Project <special> & chars!",
        "description": "Desc with émojis 🎉 and symbols @#$",
        "status": "active",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    data = response.json()
    # Verify special characters are preserved
    assert "<special>" in data["name"]
    assert "🎉" in data["description"]


def test_create_multiple_projects_same_name(client, test_db):
    """Test that multiple projects can have the same name."""
    project_data = {
        "name": "Duplicate Name",
        "status": "active",
    }
    response1 = client.post("/projects", json=project_data)
    response2 = client.post("/projects", json=project_data)

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["id"] != response2.json()["id"]


def test_project_status_completed(client, test_db):
    """Test creating and using completed status."""
    project_data = {
        "name": "Completed Project",
        "status": "completed",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"


def test_project_empty_description(client, test_db):
    """Test creating project with empty description."""
    project_data = {
        "name": "No Description",
        "description": "",
        "status": "active",
    }
    response = client.post("/projects", json=project_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == ""
