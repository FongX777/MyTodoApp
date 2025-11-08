# Load Testing for MyTodoApp

This directory contains tools and scripts for load testing the MyTodoApp API with observability instrumentation enabled.

## Requirements

- [wrk](https://github.com/wg/wrk) or [hey](https://github.com/rakyll/hey) for HTTP load testing
- Docker and docker-compose for running the observability stack

## Running the Load Tests

1. Start the observability stack and backend:

```bash
docker compose -f docker-compose.observability.yml up --build -d
```

2. Run the basic load test:

```bash
./run_wrk.sh
```

3. Check metrics in Grafana (<http://localhost:3000>) to observe performance.

## Performance Goals

The following performance goals are defined for the instrumented service:

- p99 latency < 1 second
- Instrumentation overhead < 3% CPU / < 5ms median latency
- Maximum memory overhead < 100MB compared to non-instrumented service

## Benchmarking Methodology

The load tests compare the instrumented service against a baseline (non-instrumented) version to measure overhead. If overhead exceeds thresholds, consider:

1. Reducing metric cardinality (fewer labels)
2. Using sampling for high-traffic endpoints
3. Optimizing logging (lower verbosity or sampling)

## Profiling

If performance issues are detected, profile the service using:

```bash
py-spy record -o profile.svg --pid $(docker compose -f docker-compose.observability.yml ps -q backend) --rate 100
```
