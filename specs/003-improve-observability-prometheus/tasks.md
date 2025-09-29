# Tasks (Draft) — Observability feature (#003)

NOTE: This is a draft task list produced by the /plan step. The /tasks command or a follow-up will expand these into numbered, ordered tasks with estimates.

## Phase A — Instrumentation
- A.1 Add request_id middleware to FastAPI and ensure it is propagated in logs and responses
- A.2 Add Prometheus client instrumentation to FastAPI (metrics: request_count, request_duration_seconds, response_status_count)
- A.3 Add structured JSON logging with request_id and project_id fields

## Phase B — Local prototype
- B.1 Create `docker-compose.observability.yml` that runs instrumented FastAPI, Prometheus, Grafana, Elasticsearch, Kibana
- B.2 Create Grafana dashboard JSON and Prometheus scrape config for local compose
- B.3 Create Elasticsearch ingest pipeline for structured logs

## Phase C — Validation & Tests
- C.1 Integration test: single request => request_id present in logs and metrics
- C.2 Load test: verify p99 latency reporting and performance overhead (target <3% CPU / <5ms)
- C.3 Alert test: simulate elevated 5xx errors and verify alert triggers

## Phase D — Documentation & Rollout
- D.1 quickstart.md and runbook for devs to spin up local prototype
- D.2 Add monitoring ownership and runbook entries
