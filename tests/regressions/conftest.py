"""
Pytest configuration and fixtures for API regression tests.

Provides common fixtures for database setup, test client,
and sample data for testing.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import sys
import os

# Set testing flag before imports
os.environ["TESTING"] = "1"

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from backend.app.main import app
from backend.app.database import Base


# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def test_db():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(test_db):
    """Create a test client with overridden database."""
    from backend.app.routes.todos import get_db as todos_get_db
    from backend.app.routes.projects import get_db as projects_get_db

    app.dependency_overrides[todos_get_db] = override_get_db
    app.dependency_overrides[projects_get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_project(client):
    """Create a sample project for testing."""
    project_data = {
        "name": "Test Project",
        "description": "A test project",
        "status": "active",
    }
    response = client.post("/projects", json=project_data)
    return response.json()


@pytest.fixture
def sample_projects(client):
    """Create multiple sample projects for testing."""
    projects = []
    for i in range(3):
        project_data = {
            "name": f"Test Project {i + 1}",
            "description": f"Description {i + 1}",
            "status": "active",
        }
        response = client.post("/projects", json=project_data)
        projects.append(response.json())
    return projects


@pytest.fixture
def sample_todo(client):
    """Create a sample todo for testing."""
    todo_data = {
        "title": "Test Todo",
        "description": "A test todo",
        "priority": "medium",
        "status": "pending",
    }
    response = client.post("/todos", json=todo_data)
    return response.json()


@pytest.fixture
def sample_todos(client, sample_project):
    """Create multiple sample todos for testing."""
    todos = []
    for i in range(5):
        todo_data = {
            "title": f"Test Todo {i + 1}",
            "description": f"Description {i + 1}",
            "priority": ["low", "medium", "high"][i % 3],
            "status": "pending",
            "project_id": sample_project["id"] if i < 3 else None,
            "order": i + 1,
        }
        response = client.post("/todos", json=todo_data)
        todos.append(response.json())
    return todos


@pytest.fixture
def completed_todo(client, sample_todo):
    """Create a completed todo for testing."""
    update_data = {
        "title": sample_todo["title"],
        "priority": sample_todo["priority"],
        "status": "completed",
    }
    response = client.put(f"/todos/{sample_todo['id']}", json=update_data)
    return response.json()
