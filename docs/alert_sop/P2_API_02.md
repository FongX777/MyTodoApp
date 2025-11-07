# P2_API_02 - High HTTP 5XX Rate > 5%

## Impact

Users are experiencing intermittent service failures. Between 5-10% of requests are returning server errors, causing degraded user experience and potential data loss on failed operations.

## Diagnose

### Step 1: Check Prometheus Metrics

1. Open Prometheus UI at `http://localhost:9090`
2. Run query: `rate(request_count{service="mytodoapp",status=~"5.."}[5m]) / rate(request_count{service="mytodoapp"}[5m])`
3. Compare current rate with baseline (should be < 1%)
4. Check error distribution: `sum by(endpoint) (rate(request_count{service="mytodoapp",status=~"5.."}[10m]))`

### Step 2: Check Grafana Dashboard

1. Open Grafana at `http://localhost:3000`
2. Review error rate trends over the last hour
3. Correlate with traffic patterns and response times
4. Check if errors are endpoint-specific

### Step 3: Application Log Analysis

1. Open Kibana at `http://localhost:5601`
2. Filter logs by: `level:(ERROR OR WARN) AND timestamp:[now-15m TO now]`
3. Look for patterns in error messages
4. Check for database timeout errors or connection issues

## Fix

### Step 1: Identify Error Patterns

1. **Check Recent Changes**:
   - Review recent deployments or configuration changes
   - Check if error rate correlates with specific time periods

### Step 2: Resource Optimization

1. **Monitor Resource Usage**:

   ```bash
   docker stats
   ```

2. **Check Memory Usage**: Look for memory leaks or high usage
3. **Database Performance**: Check slow query logs

### Step 3: Temporary Mitigation

1. **Increase Timeout Settings**: Temporarily increase request timeouts if network-related
2. **Add Retry Logic**: Ensure proper retry mechanisms are in place
3. **Load Balancing**: If possible, distribute load across multiple instances

### Step 4: Long-term Solutions

1. **Code Review**: Review error-prone endpoints
2. **Database Optimization**: Optimize slow queries
3. **Monitoring Enhancement**: Add more detailed metrics for early detection
