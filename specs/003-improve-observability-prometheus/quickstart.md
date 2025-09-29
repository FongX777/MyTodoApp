# Quickstart: Observability Stack with Prometheus & Elasticsearch

This guide helps you run a local development stack with instrumented FastAPI, React frontend, PostgreSQL database, Prometheus for metrics, Grafana for dashboards, Elasticsearch for logs, and Kibana for log visualization.

## Prerequisites

- Docker & docker-compose installed
- Git repository clone of AlertingScout

## Quick Start

1. Start the entire stack:

```bash
docker compose -f docker-compose.observability.yml up --build
```

2. Wait for all services to become healthy (usually takes 1-2 minutes for Elasticsearch).

3. Access the services:
   - Frontend: [http://localhost:3001](http://localhost:3001)
   - Backend API: [http://localhost:8000](http://localhost:8000)
   - Prometheus: [http://localhost:9090](http://localhost:9090)
   - Grafana: [http://localhost:3000](http://localhost:3000) (login: admin/admin)
   - Kibana: [http://localhost:5601](http://localhost:5601)

4. Generate some traffic to see metrics and logs:

```bash
# Make some requests to the API
curl http://localhost:8000/
curl http://localhost:8000/todos
curl http://localhost:8000/projects
```

## Metrics & Dashboards

1. **Prometheus metrics**:
   - View raw metrics at [http://localhost:8000/metrics](http://localhost:8000/metrics)
   - Query metrics in Prometheus UI: [http://localhost:9090/graph](http://localhost:9090/graph)
   - Example query: `sum(rate(request_count[5m])) by (endpoint)`

2. **Grafana dashboards**:
   - Open [http://localhost:3000](http://localhost:3000)
   - The "AlertingScout API Monitoring" dashboard is pre-configured
   - Datasource is auto-configured to connect to Prometheus

## Logs in Kibana

1. Open Kibana: [http://localhost:5601](http://localhost:5601)

2. Set up the index pattern (first time only):
   - Go to Stack Management > Index Patterns
   - Create index pattern: `alertingscout-logs-*`
   - Select `@timestamp` as time field
   - Click "Create index pattern"

3. View logs in Discover:
   - Go to Discover tab
   - Select time range (top right)
   - Search for specific request_id: `trace.id: "your-request-id"`
   - Filter by log level: `log.level: "ERROR"`

## Environment Variables

Customize behavior with these environment variables:

```bash
# In docker-compose.observability.yml or export before running
export LOG_LEVEL=DEBUG  # Set logging verbosity (DEBUG, INFO, WARNING, ERROR)
```

## Running Tests

To run the end-to-end test (verifies metrics and logging pipeline):

```bash
# With stack running
pytest tests/observability/test_e2e_metrics_logs.py -v
```

To run load tests:

```bash
cd specs/003-improve-observability-prometheus/load-tests
./run_wrk.sh
```

## Alerting

To test alerting rules:

```bash
cd specs/003-improve-observability-prometheus/alert-testing
./trigger_error_spike.sh
```

Then check [http://localhost:9090/alerts](http://localhost:9090/alerts) to see if alerts are firing.

## Teardown

When finished, stop and remove containers:

```bash
docker compose -f docker-compose.observability.yml down -v
```

## Troubleshooting

- **Elasticsearch fails to start**: Increase Docker memory limits (needs at least 2GB)
- **No metrics appearing**: Verify backend is running with `curl http://localhost:8000/metrics`
- **No logs in Kibana**: Check Elasticsearch health with `curl http://localhost:9200/_cluster/health`