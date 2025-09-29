"""
Structured JSON logging configuration for FastAPI.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware


class JSONLogFormatter(logging.Formatter):
    """
    Custom formatter to output logs in JSON format.

    This allows structured logging with consistent fields for better
    parsing in Elasticsearch and other log management systems.
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format the log record as a JSON string."""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": getattr(record, "service", "alertingscout"),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }

        # Include request_id if available
        request_id = getattr(record, "request_id", None)
        if request_id:
            log_data["request_id"] = request_id

        # Include project_id if available
        project_id = getattr(record, "project_id", None)
        if project_id:
            log_data["project_id"] = project_id

        # Include user_id if available
        user_id = getattr(record, "user_id", None)
        if user_id:
            log_data["user_id"] = user_id

        # Include exception information if available
        if record.exc_info:
            log_data["stack_trace"] = self.formatException(record.exc_info)

        # Include any additional fields from record.__dict__
        # Exclude standard LogRecord attributes to avoid duplication
        standard_attrs = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "lineno",
            "funcName",
            "created",
            "asctime",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "service",
            "request_id",
            "project_id",
            "user_id",
        }

        # Add any extra attributes as metadata
        metadata = {}
        for key, value in record.__dict__.items():
            if key not in standard_attrs and not key.startswith("_"):
                metadata[key] = value

        if metadata:
            log_data["metadata"] = metadata

        return json.dumps(log_data)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log requests with correlation IDs and timing.

    This middleware logs the start and end of each request, including
    the request_id, method, path, status code, and duration.
    """

    async def dispatch(self, request: Request, call_next):
        """Process the request and log request information."""
        # Get start time
        start_time = datetime.utcnow()

        # Extract request_id from request state (set by RequestIDMiddleware)
        request_id = getattr(request.state, "request_id", None)

        # Extract project_id from request path or query params if available
        project_id = None
        if "project_id" in request.path_params:
            project_id = request.path_params["project_id"]
        elif "project_id" in request.query_params:
            project_id = request.query_params["project_id"]

        # Log request start
        logger = logging.getLogger("api")
        logger.info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                "request_id": request_id,
                "project_id": project_id,
                "http_method": request.method,
                "path": request.url.path,
            },
        )

        try:
            # Process the request
            response = await call_next(request)

            # Calculate duration
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

            # Log request completion
            logger.info(
                f"Request completed: {request.method} {request.url.path} {response.status_code} ({duration_ms:.2f}ms)",
                extra={
                    "request_id": request_id,
                    "project_id": project_id,
                    "http_method": request.method,
                    "path": request.url.path,
                    "status_code": response.status_code,
                    "duration_ms": duration_ms,
                },
            )

            return response

        except Exception as exc:
            # Calculate duration
            duration_ms = (datetime.utcnow() - start_time).total_seconds() * 1000

            # Log exception
            logger.exception(
                f"Request failed: {request.method} {request.url.path} ({duration_ms:.2f}ms)",
                extra={
                    "request_id": request_id,
                    "project_id": project_id,
                    "http_method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                },
            )

            # Re-raise the exception
            raise


def setup_logging(service_name: str = "alertingscout") -> None:
    """
    Configure structured JSON logging for the application.

    Args:
        service_name: Name of the service for logging context
    """
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create and configure handler with JSON formatter
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONLogFormatter())
    root_logger.addHandler(handler)

    # Set service name in logger context
    logging.LoggerAdapter(root_logger, {"service": service_name})

    # Log setup completion
    root_logger.info(f"Logging initialized for service: {service_name}")


def setup_request_logging(app: FastAPI) -> None:
    """
    Add request logging middleware to the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    app.add_middleware(RequestLoggingMiddleware)
