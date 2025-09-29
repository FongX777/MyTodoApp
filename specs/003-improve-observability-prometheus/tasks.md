# Tasks — Observability feature (#003)

This file lists actionable, dependency-ordered tasks. Tasks marked with [P] may be executed in parallel when they touch independent files or services.

T001 - Setup & CI scaffolding [P]

- Goal: Prepare test scaffolding and CI job stub for observability checks.
- Output: `tests/observability/`, `.github/workflows/observability-ci.yml`
- Steps:
  1. Create directory `tests/observability/` and add README with run instructions.
  2. Add `.github/workflows/observability-ci.yml` that runs `pytest tests/observability -q` (job can be a no-op until tests exist).
  3. Locally validate with `pytest -q tests/observability` (should initially fail or print placeholder).

T002 [P] - Contract test: metrics endpoint

- Goal: Create a failing contract test that asserts `/metrics` is present and returns Prometheus text.
- File: `tests/observability/test_contract_metrics.py`
- Requirements:
  - Use `httpx` or `requests` to GET `http://localhost:8000/metrics` and assert status 200 and response contains `# HELP` or metric name `request_count`.
  - Mark test as xfail or skip until service is available locally.

T010 [P] - Add request_id middleware to FastAPI

- Goal: Ensure each request has a stable `X-Request-Id` header and the value appears in logs.
- Files to modify/create:
  - `backend/app/middleware/request_id.py` (new)
  - `backend/app/main.py` (register middleware)
  - `tests/observability/test_request_id.py` (unit test)
- Implementation notes:
  - If `X-Request-Id` header provided, forward; else generate UUID4.
  - Add header to response and store in request context for logging.

T011 [P] - Add Prometheus instrumentation to FastAPI

- Goal: Expose `/metrics` and instrument requests with `request_count`, `request_duration_seconds` (histogram) and `response_status_count` labels: service, endpoint, method, status, project_id.
- Files to modify/create:
  - `backend/app/metrics.py` (new)
  - `backend/app/main.py` (mount `/metrics` and call instrumentation middleware)
- Acceptance test: `curl http://localhost:8000/metrics` returns 200 and contains `request_count`.

T012 [P] - Add structured JSON logging

- Goal: Configure structured logging (json) including `timestamp, service, level, message, request_id, project_id`.
- Files: `backend/app/logging_config.py` (new), update `backend/app/main.py` to use it.
- Acceptance: Logs on stdout are valid JSON and contain `request_id` field.

T020 - Compose prototype: add `docker-compose.observability.yml`

- Goal: Provide a local prototype to run instrumented FastAPI + Prometheus + Grafana + Elasticsearch + Kibana.
- File: repo root `docker-compose.observability.yml`
- Compose services (suggested images):
  - backend: build from repo `backend/` (port 8000)
  - prometheus: `prom/prometheus:latest` (9090) with volume-mounted `prometheus.yml`
  - grafana: `grafana/grafana` (3000)
  - elasticsearch: `docker.elastic.co/elasticsearch/elasticsearch:8.8.0` (9200)
  - kibana: `docker.elastic.co/kibana/kibana:8.8.0` (5601)
- Acceptance: `docker compose -f docker-compose.observability.yml up --build` starts all containers and ports are reachable.

T021 [P] - Add Prometheus config and Grafana dashboard

- Goal: Add `prometheus.yml` pointing to `backend:8000` and a Grafana dashboard JSON that visualizes request rate and latency.
- Files:
  - `specs/003-improve-observability-prometheus/prometheus/prometheus.yml`
  - `specs/003-improve-observability-prometheus/grafana/observability.json`
- Acceptance: Grafana dashboard loads and shows Prometheus metrics after compose up.

T022 - Elasticsearch ingest pipeline & index template

- Goal: Provide ingest pipeline and index template to map `request_id`, `service`, `project_id` as keywords.
- Files:
  - `specs/003-improve-observability-prometheus/elasticsearch/ingest-pipeline.json`
  - `specs/003-improve-observability-prometheus/elasticsearch/index-template.json`
- Acceptance: On indexing logs, fields appear with correct types in Kibana.

T030 [P] - E2E integration test: request -> metrics & logs

- Goal: Automated test sending an HTTP request, checking `/metrics` and querying Elasticsearch for the log with the same `request_id`.
- File: `tests/observability/test_e2e_metrics_logs.py`
- Acceptance: Test asserts both metric increment and a corresponding log entry exist.

T031 - Load test and performance validation

- Goal: Run a lightweight load test (wrk/locust) to measure p99 latency and CPU overhead.
- Files: `specs/003-improve-observability-prometheus/load-tests/README.md` and an example script `specs/003-improve-observability-prometheus/load-tests/run_wrk.sh`
- Acceptance: p99 < 1s and instrumentation overhead <3% CPU / <5ms median latency. If not met, adjust sampling/labels.

T032 - Alerting smoke test

- Goal: Simulate 5xx spike and verify Prometheus alert rule triggers (using a local Alertmanager or webhook stub).
- File: `specs/003-improve-observability-prometheus/alert-testing/trigger_error_spike.sh`
- Acceptance: Alert rule for 5xx > 10% for 5m transitions to firing state in Alertmanager (or local stub receives webhook).

T040 - Update quickstart & runbook

- Goal: Finalize `quickstart.md` with exact compose commands, env vars, troubleshooting, and how to query Prometheus/Grafana/Kibana.
- File: `specs/003-improve-observability-prometheus/quickstart.md` (update)
- Acceptance: A developer can run `docker compose -f docker-compose.observability.yml up --build` and see Grafana/Prometheus/Kibana up and data flowing.

Parallel groups

- Group A (parallel): T001, T002, T010, T011, T012 (different devs can scaffold tests and instrumentation concurrently).
- Group B (parallel): T021, T022 once T011/T012 are available.

Local smoke-check (what you'll do to verify browsers show services)

1. Start the prototype stack:

```bash
docker compose -f docker-compose.observability.yml up --build
```

2. Verify endpoints in browser:

- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>
- Kibana: <http://localhost:5601>

3. Run E2E test once stack is healthy:

```bash
pytest tests/observability/test_e2e_metrics_logs.py -q
```
