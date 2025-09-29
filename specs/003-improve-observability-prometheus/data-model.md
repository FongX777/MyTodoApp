# Data Model: Observability (metrics & logs)

## Metric labels and conventions
- metric: request_count
- labels: { service, endpoint, method, status, project_id }
- metric: request_duration_seconds (histogram)
- labels: { service, endpoint, method, project_id }

Notes:
- Keep cardinality low: avoid adding high-cardinality labels (user_id, todo_id) to metrics.

## LogEntry schema (Elasticsearch index)
- timestamp: date
- service: keyword
- level: keyword (DEBUG/INFO/WARN/ERROR)
- message: text
- request_id: keyword
- project_id: keyword
- user_id: keyword (nullable)
- stack_trace: text (nullable)
- metadata: object (free-form JSON for additional context)

Indexing strategy:
- Use a time-based index (e.g., alertingscout-logs-YYYY.MM.DD)
- Configure mappings for keyword fields (service, request_id, project_id) to enable fast filtering
- Use ingest pipeline to parse common structured fields if logs come as free-form strings
