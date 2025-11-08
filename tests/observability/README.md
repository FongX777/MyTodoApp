# Observability Tests

This directory contains tests for the observability features of MyTodoApp.

## Running Tests

To run all observability tests:

```bash
pytest tests/observability -v
```

To run a specific test:

```bash
pytest tests/observability/test_request_id.py -v
```

## Test Categories

- **Contract Tests**: Verify API contracts for observability endpoints like `/metrics`
- **Unit Tests**: Test individual components like middleware and instrumentation
- **E2E Tests**: Test full observability pipeline (metrics collection, logging, etc.)
