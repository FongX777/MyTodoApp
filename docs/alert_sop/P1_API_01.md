# P1_API_01 - Critical HTTP 5XX Rate > 10%

## Impact

Users are experiencing critical service failures with server errors. More than 10% of requests are returning 5XX status codes, indicating severe backend issues that prevent users from accessing core functionality.

## Diagnose

### Step 1: Check Prometheus Metrics

1. Open Prometheus UI at `http://localhost:9090`
2. Run query: `rate(request_count{service="mytodoapp",status=~"5.."}[5m]) / rate(request_count{service="mytodoapp"}[5m])`
3. Check the current error rate percentage
4. Run query: `sum by(status, endpoint) (rate(request_count{service="mytodoapp",status=~"5.."}[5m]))` to identify which endpoints are failing

### Step 2: Check Grafana Dashboard

1. Open Grafana at `http://localhost:3000`
2. Navigate to "MyTodoApp Observability" dashboard
3. Look at the "Error Rate" panel to see the trend over time
4. Check "Response Time" panels to correlate with latency issues
5. Review "Request Rate by Endpoint" to identify problematic endpoints

### Step 3: Check Application Logs

1. Open Kibana at `http://localhost:5601`
2. Search for recent logs with level "ERROR" or "CRITICAL"
3. Filter by timestamp to match the alert timeframe
4. Look for stack traces, database connection errors, or external service failures

### Step 4: Check Container Health

1. Run `docker compose logs backend` to see recent application logs
2. Check if containers are restarting: `docker compose ps`
3. Monitor resource usage: `docker stats`

## Fix

### Step 1: Immediate Actions

1. **Check Database Connectivity**:
   - Verify PostgreSQL is running: `docker compose exec db pg_isready -U user`
   - Check database logs: `docker compose logs db`

### Step 2: Backend Service Issues

1. **Restart Backend Service**:

   ```bash
   docker compose restart backend
   ```

2. **Check Dependencies**:
   - Verify all required environment variables are set
   - Check external service dependencies (if any)

### Step 3: Database Issues

1. **Check Database Space**:
   - Connect to DB: `docker compose exec db psql -U user -d tododb`
   - Check disk space and table sizes

2. **Database Connection Pool**:
   - Check if connection pool is exhausted
   - Review database connection settings in application

### Step 4: Code Issues

1. **Review Recent Deployments**:
   - Check if error spike correlates with recent code changes
   - Review git log for recent commits

2. **Check Application Logic**:
   - Look for unhandled exceptions in error logs
   - Review database queries for performance issues

### Step 5: Escalation

If errors persist after basic fixes:

1. Scale backend service: `docker compose up --scale backend=2 -d`
2. Contact development team with error logs and metrics
3. Consider rolling back recent deployments if correlation is found
