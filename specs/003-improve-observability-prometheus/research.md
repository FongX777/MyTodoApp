# Research: Improve observability — Prometheus & Elasticsearch

Date: 2025-09-29

Decision: Prototype observability using Prometheus for metrics collection and Elasticsearch for centralized logs, visualized with Grafana and Kibana. Use docker-compose and instrument the FastAPI backend locally.

Rationale:

- Prometheus is a widely adopted open-source metrics system with lightweight scrape model and strong Grafana integration for dashboards. It is simple to prototype with docker-compose.
- Elasticsearch provides fast, full-text search and structured indexing suitable for log exploration; Kibana gives immediate query and dashboard capabilities.
- FastAPI is already the backend target for instrumentation; Python ecosystem has mature Prometheus client libraries and structured logging libraries.
- Docker-compose allows a contained developer environment (no cluster) to iterate and validate metrics/log formats and dashboards quickly.

Alternatives considered:

- Hosted managed metrics (e.g., Prometheus remote write to Cortex/Thanos) — pros: scalable, managed; cons: cost and setup complexity. Deferred to platform decision.
- Managed logging (e.g., Elastic Cloud, Logz.io) — pros: lower ops; cons: cost and potential data residency constraints.
- Use Loki instead of Elasticsearch for logs — pros: lower cost and better integration with Grafana; cons: less powerful full-text search for unstructured logs. Keep as possible alternative.

Key findings / Constraints:

- Cardinality: Keep Prometheus label cardinality low (avoid per-request unique labels beyond request_id for correlation). Use label for endpoint, method, status, project_id.
- Logging: Emit structured JSON logs with a request_id field. Do not log PII; redact or omit sensitive fields.
- Performance: Aim for <3% CPU overhead or <5ms median added latency for instrumentation and shipping.

Next steps (Phase 1):

- Produce data-model.md describing log schema and metric labels.
- Produce OpenAPI contract changes (if instrumenting affects endpoints) and quickstart for docker-compose prototype.
