import pytest
import httpx
import time
import json
import uuid
import os
from elasticsearch import Elasticsearch


# Mark test as xfail until the full stack is available
@pytest.mark.xfail(reason="Full observability stack not yet running")
def test_request_metrics_and_logs_correlation():
    """
    End-to-end test that:
    1. Sends a request to the backend API
    2. Checks that metrics were updated in Prometheus
    3. Checks that logs were shipped to Elasticsearch
    4. Verifies the same request_id appears in both
    """
    # Generate a unique request_id for this test run
    request_id = str(uuid.uuid4())

    # 1. Send a request to the backend with our custom request_id
    backend_url = os.environ.get("BACKEND_URL", "http://localhost:8000")

    try:
        # Send a request to the todos endpoint with our request_id
        response = httpx.get(f"{backend_url}/todos", headers={"X-Request-Id": request_id}, timeout=5.0)

        # Ensure request succeeded
        assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"

        # Verify the same request_id is returned in response headers
        assert response.headers.get("X-Request-Id") == request_id, (
            "Response is missing or has incorrect X-Request-Id header"
        )

        # 2. Wait a moment for metrics and logs to be processed
        time.sleep(2)

        # 3. Check Prometheus for updated metrics
        prometheus_url = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")

        # Query Prometheus to see if our request was counted
        prom_response = httpx.get(
            f"{prometheus_url}/api/v1/query",
            params={"query": 'request_count{endpoint="/todos",method="GET"}'},
            timeout=5.0,
        )

        # Check that we got a valid response from Prometheus
        assert prom_response.status_code == 200, f"Prometheus API returned {prom_response.status_code}"

        # Parse response and check if our metrics exist
        prom_data = prom_response.json()
        assert prom_data["status"] == "success", f"Prometheus query failed: {prom_data}"

        # Should have at least one result for our metrics
        assert len(prom_data["data"]["result"]) > 0, "No metrics found for request_count"

        # 4. Check Elasticsearch for logs with our request_id
        es_url = os.environ.get("ELASTICSEARCH_URL", "http://localhost:9200")
        es = Elasticsearch(es_url)

        # Give a moment for logs to be indexed
        max_retries = 5
        retry_delay = 2
        found_log = False

        for attempt in range(max_retries):
            try:
                # Search for logs with our request_id
                result = es.search(index="alertingscout-logs-*", body={"query": {"match": {"trace.id": request_id}}})

                # Check if we found matching logs
                if result["hits"]["total"]["value"] > 0:
                    found_log = True
                    break

            except Exception as e:
                print(f"Elasticsearch search attempt {attempt + 1} failed: {str(e)}")

            if attempt < max_retries - 1:
                print(f"Waiting for logs to be indexed (attempt {attempt + 1}/{max_retries})")
                time.sleep(retry_delay)

        # Verify we found logs with our request_id
        assert found_log, f"No logs found with request_id {request_id} after {max_retries} attempts"

    except httpx.ConnectError:
        pytest.skip("Backend service not available")


if __name__ == "__main__":
    test_request_metrics_and_logs_correlation()
