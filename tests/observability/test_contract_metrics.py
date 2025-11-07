import pytest
import httpx
import time


# Mark as expected to fail until the metrics endpoint is implemented
@pytest.mark.xfail(reason="Metrics endpoint not yet implemented")
def test_metrics_endpoint_available():
    """Test that the metrics endpoint exists and returns Prometheus formatted metrics."""
    # Allow some time for the server to start in CI environments
    max_retries = 3
    retry_delay = 2

    for attempt in range(max_retries):
        try:
            # Connect to the metrics endpoint
            response = httpx.get("http://localhost:8000/metrics", timeout=5.0)

            # Check status code
            assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"

            # Check content type (Prometheus text format)
            assert "text/plain" in response.headers.get("content-type", ""), (
                f"Expected content-type to contain 'text/plain', got {response.headers.get('content-type')}"
            )

            # Check for common Prometheus metric format patterns
            content = response.text
            assert any(pattern in content for pattern in ["# HELP", "# TYPE", "request_count"]), (
                "Response doesn't contain expected Prometheus metric format"
            )

            return  # Test passed

        except (httpx.ConnectError, AssertionError) as e:
            if attempt < max_retries - 1:
                print(f"Retry {attempt + 1}/{max_retries} after error: {str(e)}")
                time.sleep(retry_delay)
            else:
                raise  # Re-raise on final attempt


# Additional test to verify specific metrics once implemented
@pytest.mark.xfail(reason="Specific metrics not yet implemented")
def test_specific_metrics_present():
    """Test that specific required metrics are present in the response."""
    response = httpx.get("http://localhost:8000/metrics", timeout=5.0)
    content = response.text

    # Check for our required metrics
    required_metrics = ["request_count", "request_duration_seconds"]

    for metric in required_metrics:
        assert metric in content, f"Required metric '{metric}' not found in metrics endpoint response"
