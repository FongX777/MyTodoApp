"""
Prometheus metrics instrumentation for FastAPI.
"""

import time
from typing import Callable, List, Optional

from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse
from starlette.routing import Match

# Define OpenMetrics content type if not available in current prometheus_client version
CONTENT_TYPE_OPENMETRICS = "application/openmetrics-text; version=1.0.0; charset=utf-8"

# Create a registry for metrics (can be default or custom)
REGISTRY = CollectorRegistry()

# Define metrics
REQUEST_COUNT = Counter(
    "request_count",
    "Total number of requests processed",
    ["service", "endpoint", "method", "status"],
    registry=REGISTRY,
)

REQUEST_DURATION = Histogram(
    "request_duration_seconds",
    "Request duration in seconds",
    ["service", "endpoint", "method"],
    registry=REGISTRY,
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 10],
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect metrics for each request."""

    def __init__(self, app, service_name: str = "fastapi", exclude_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.service_name = service_name
        self.exclude_paths = exclude_paths or ["/metrics"]

    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip metrics collection for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        # Get route pattern or path if no matching route found
        endpoint = self._get_endpoint(request)
        method = request.method

        # Start timer for request duration
        start_time = time.time()

        # Process the request
        try:
            response = await call_next(request)
            status = str(response.status_code)
        except Exception as e:
            status = "500"
            raise e
        finally:
            # Record metrics
            duration = time.time() - start_time

            REQUEST_COUNT.labels(service=self.service_name, endpoint=endpoint, method=method, status=status).inc()

            REQUEST_DURATION.labels(service=self.service_name, endpoint=endpoint, method=method).observe(duration)

        return response

    @staticmethod
    def _get_endpoint(request: Request) -> str:
        """Get the request endpoint name from router match."""
        for route in request.app.routes:
            match, scope = route.matches(request.scope)
            if match == Match.FULL:
                return route.path
        return request.url.path


def metrics_endpoint(request: Request) -> StarletteResponse:
    """Expose metrics for scraping by Prometheus."""
    # Use Prometheus default content type to ensure compatibility
    try:
        content = generate_latest(REGISTRY)
        content_type = CONTENT_TYPE_LATEST
    except Exception as e:
        # Fallback with error message
        content = f"# Error generating metrics: {str(e)}".encode("utf-8")
        content_type = "text/plain"

    return StarletteResponse(content=content, media_type=content_type)


def setup_metrics(
    app: FastAPI,
    service_name: str = "fastapi",
    endpoint_path: str = "/metrics",
    exclude_paths: Optional[List[str]] = None,
) -> None:
    """
    Setup Prometheus metrics collection and endpoint.

    Args:
        app: FastAPI application
        service_name: Name of the service for metrics labels
        endpoint_path: Path where metrics will be exposed
        exclude_paths: List of paths to exclude from metrics
    """
    # Ensure metrics endpoint is in excluded paths
    exclude_paths = exclude_paths or []
    if endpoint_path not in exclude_paths:
        exclude_paths.append(endpoint_path)

    # Add the metrics endpoint
    app.add_route(endpoint_path, metrics_endpoint)

    # Add the metrics middleware
    app.add_middleware(PrometheusMiddleware, service_name=service_name, exclude_paths=exclude_paths)
