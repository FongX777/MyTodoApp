# P2_API_06 - Critical P95 Response Time > 2s

## Impact

Users are experiencing severely degraded performance with the 95th percentile of requests taking over 2 seconds. This level of latency significantly impacts user experience, may cause client-side timeouts, and indicates serious performance issues requiring immediate attention.

## Diagnose

### Step 1: Critical Performance Assessment

1. Open Prometheus UI at `http://localhost:9090`
2. Check current P95 latency: `histogram_quantile(0.95, sum(rate(request_duration_seconds_bucket{service="mytodoapp"}[5m])) by (le))`
3. Check P99 for worst-case: `histogram_quantile(0.99, sum(rate(request_duration_seconds_bucket{service="mytodoapp"}[5m])) by (le))`
4. Identify slowest endpoints: `topk(5, histogram_quantile(0.95, sum(rate(request_duration_seconds_bucket{service="mytodoapp"}[10m])) by (le,endpoint)))`

### Step 2: System Resource Analysis

1. Check immediate resource usage: `docker stats`
2. Look for CPU/memory bottlenecks
3. Check disk I/O if persistent storage is involved
4. Monitor network latency to external dependencies

### Step 3: Database Deep Dive

1. Connect to database: `docker compose exec db psql -U user -d tododb`
2. Check active connections: `SELECT count(*) FROM pg_stat_activity;`
3. Identify slow/blocking queries: `SELECT * FROM pg_stat_activity WHERE state = 'active' AND query_start < now() - interval '10 seconds';`
4. Look for lock contentions: `SELECT * FROM pg_locks WHERE NOT granted;`

### Step 4: Application Analysis

1. Check Kibana for errors correlating with slow responses
2. Look for patterns in slow requests (endpoints, request size, etc.)
3. Review recent code deployments that might have introduced performance regressions

## Fix

### Step 1: Emergency Response

1. **Immediate Scaling**:

   ```bash
   # Scale up backend instances immediately
   docker compose up --scale backend=3 -d
   ```

2. **Kill Long-Running Queries** (if database-related):

   ```sql
   -- In postgres, kill queries running longer than 30 seconds
   SELECT pg_terminate_backend(pid) FROM pg_stat_activity 
   WHERE state = 'active' AND query_start < now() - interval '30 seconds';
   ```

### Step 2: Database Optimization

1. **Connection Pool Emergency Increase**:
   - Temporarily increase max database connections
   - Monitor connection pool metrics

2. **Query Optimization**:
   - Identify and optimize the slowest queries
   - Add emergency indexes for critical queries
   - Consider query timeouts to prevent resource exhaustion

### Step 3: Application-Level Fixes

1. **Circuit Breaker Implementation**:
   - Implement timeouts for external service calls
   - Add circuit breakers to prevent cascade failures

2. **Temporary Feature Disabling**:
   - Disable non-critical features that are performance-heavy
   - Implement graceful degradation

### Step 4: Traffic Management

1. **Rate Limiting**:
   - Implement emergency rate limiting to reduce load
   - Prioritize critical API endpoints

2. **Load Balancing**:
   - Ensure traffic is properly distributed across instances
   - Consider directing traffic away from problematic endpoints

### Step 5: Long-term Resolution

1. **Performance Profiling**:
   - Run detailed application profiling
   - Identify bottlenecks in code

2. **Infrastructure Scaling**:
   - Plan for increased resources (CPU, memory, database)
   - Consider horizontal scaling solutions

3. **Architecture Review**:
   - Evaluate caching strategies
   - Consider async processing for heavy operations
   - Review database schema and query patterns
