# P3_API_05 - High P95 Response Time > 1s

## Impact

Users are experiencing slower than expected response times. The 95th percentile of requests taking longer than 1 second indicates performance degradation that affects user experience and may lead to timeouts in client applications.

## Diagnose

### Step 1: Response Time Analysis

1. Open Prometheus UI at `http://localhost:9090`
2. Check current P95: `histogram_quantile(0.95, sum(rate(request_duration_seconds_bucket{service="mytodoapp"}[5m])) by (le))`
3. Compare P50 and P99: Replace 0.95 with 0.50 and 0.99 in the query above
4. Identify slow endpoints: `histogram_quantile(0.95, sum(rate(request_duration_seconds_bucket{service="mytodoapp"}[10m])) by (le,endpoint))`

### Step 2: Grafana Performance Review

1. Open Grafana at `http://localhost:3000`
2. Review response time trends over the past hour
3. Check if slowness correlates with increased traffic
4. Look at database query performance metrics if available

### Step 3: Resource Usage Check

1. Check container resources: `docker stats`
2. Monitor CPU and memory usage patterns
3. Check database connection pool status
4. Review Kibana for any performance-related log entries

### Step 4: Database Performance

1. Connect to database: `docker compose exec db psql -U user -d tododb`
2. Check for slow queries: `SELECT * FROM pg_stat_statements ORDER BY mean_time DESC LIMIT 10;`
3. Look for blocking queries or lock waits

## Fix

### Step 1: Immediate Optimization

1. **Database Query Optimization**:
   - Identify and optimize slow queries
   - Add missing indexes if needed
   - Check for N+1 query problems

2. **Connection Pool Tuning**:
   - Increase database connection pool size if needed
   - Optimize connection timeout settings

### Step 2: Application Performance

1. **Code Optimization**:
   - Profile application code for bottlenecks
   - Optimize expensive operations
   - Consider caching for frequently accessed data

2. **Resource Scaling**:

   ```bash
   # Temporarily scale up if resource-constrained
   docker compose up --scale backend=2 -d
   ```

### Step 3: Caching Implementation

1. **Add Response Caching**:
   - Implement Redis caching for expensive operations
   - Cache frequently requested data

2. **Database Query Caching**:
   - Enable query result caching where appropriate
   - Use application-level caching for static data

### Step 4: Long-term Solutions

1. **Performance Monitoring**:
   - Add more detailed performance metrics
   - Implement distributed tracing for complex operations

2. **Capacity Planning**:
   - Plan for traffic growth
   - Implement auto-scaling if needed

3. **Architecture Review**:
   - Consider microservices for heavy operations
   - Evaluate async processing for non-real-time tasks
