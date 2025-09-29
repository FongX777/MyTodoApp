import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient
import re
import uuid

from backend.app.middleware.request_id import (
    RequestIDMiddleware,
    add_request_id_middleware,
    get_request_id,
    REQUEST_ID_HEADER_KEY,
)

# UUID regex pattern for validation
UUID_PATTERN = r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"


@pytest.fixture
def app():
    """Create a FastAPI app with the RequestIDMiddleware."""
    app = FastAPI()
    add_request_id_middleware(app)

    @app.get("/test")
    def test_endpoint(request: Request):
        return {"request_id": get_request_id(request)}

    return app


@pytest.fixture
def client(app):
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_middleware_adds_request_id_header(client):
    """Test that middleware adds X-Request-Id header when not provided."""
    response = client.get("/test")
    assert response.status_code == 200

    # Verify header exists in response
    request_id = response.headers.get(REQUEST_ID_HEADER_KEY)
    assert request_id is not None

    # Verify it's a valid UUID
    assert re.match(UUID_PATTERN, request_id), f"Invalid UUID format: {request_id}"

    # Verify the ID is available in request state (via endpoint return)
    assert response.json()["request_id"] == request_id


def test_middleware_preserves_provided_request_id(client):
    """Test that middleware preserves X-Request-Id header when provided."""
    provided_id = str(uuid.uuid4())
    response = client.get("/test", headers={REQUEST_ID_HEADER_KEY: provided_id})
    assert response.status_code == 200

    # Verify the provided ID is preserved
    returned_id = response.headers.get(REQUEST_ID_HEADER_KEY)
    assert returned_id == provided_id

    # Verify the ID is available in request state (via endpoint return)
    assert response.json()["request_id"] == provided_id
