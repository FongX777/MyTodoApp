# Middleware to add request_id to every request

import uuid
from typing import Optional
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

REQUEST_ID_HEADER_KEY = "X-Request-Id"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to ensure each request has a unique ID in X-Request-Id header.

    If the header is already present, it will be preserved.
    If not, a new UUID4 will be generated and added.
    The ID is also made available in the request state for logging.
    """

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response:
        # Get request_id from header or generate a new one
        request_id = request.headers.get(REQUEST_ID_HEADER_KEY)
        if not request_id:
            request_id = str(uuid.uuid4())

        # Store in request state for logging
        request.state.request_id = request_id

        # Process the request
        response = await call_next(request)

        # Add or update the header in the response
        response.headers[REQUEST_ID_HEADER_KEY] = request_id

        return response


def add_request_id_middleware(app: FastAPI) -> None:
    """
    Add the RequestIDMiddleware to the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    app.add_middleware(RequestIDMiddleware)


def get_request_id(request: Request) -> Optional[str]:
    """
    Get the request ID from the request state.

    Args:
        request: The FastAPI request object

    Returns:
        The request ID or None if not present
    """
    return getattr(request.state, "request_id", None)
