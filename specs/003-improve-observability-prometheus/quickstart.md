# Quickstart: Local prototype with docker-compose

This quickstart shows how to run a local prototype of FastAPI instrumented with Prometheus, a Prometheus server, Grafana, Elasticsearch and Kibana using docker-compose for validation and developer testing.

Prereqs:
- Docker & docker-compose installed
- Local FastAPI app (instrumented) or the repository's backend in a local dev mode

Steps:
1. Copy `docker-compose.observability.yml` into repository root (or use the provided compose file in this spec).
2. Start the stack:

```bash
docker compose -f docker-compose.observability.yml up --build
```

3. Verify Prometheus scraping: open Grafana (http://localhost:3000) and add Prometheus datasource pointing to http://prometheus:9090 (in compose network). Load the provided dashboard.
4. Verify logs in Kibana (http://localhost:5601) and query for `request_id` values.

Teardown:

```bash
docker compose -f docker-compose.observability.yml down -v
```

Notes:
- This is a dev prototype. For production use, replace local-compose services with managed or cluster components and tune retention/replication accordingly.
