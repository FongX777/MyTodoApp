# SOP for Alerting

## Rules

Format: `[Priority Level]_[Alert Type]_[Alert ID] - [Condition]`

- Priority Levels:
  - P1: Critical, requires immediate attention
  - P2: High, requires attention within 2 hour
  - P3: Medium, requires attention within 24 hours
- Alert Type can be API, DB, AUTH, etc.
- Alert ID is incremental.

## Alerts

- P1_API_01 - HTTP 5XX Rate > 10% in 5 minutes
- P2_API_02 - HTTP 5XX Rate > 5% in 5 minutes
- P2_API_03 - HTTP 4XX Rate > 20% in 5 minutes
- P3_API_04 - HTTP 4XX Rate > 10% in 5 minutes
- P3_API_05 - p95 Response Time > 1s in 5 minutes
- P2_API_06 - p95 Response Time > 2s in 5 minutes
- P1_API_07 - Endpoints Unhealthy for more than 5 minutes (/healthz)

## SOP Files

Each alert has a corresponding Standard Operating Procedure (SOP) file with detailed diagnosis and fix instructions:

- [P1_API_01.md](P1_API_01.md) - Critical HTTP 5XX Rate > 10%
- [P2_API_02.md](P2_API_02.md) - High HTTP 5XX Rate > 5%
- [P2_API_03.md](P2_API_03.md) - High HTTP 4XX Rate > 20%
- [P3_API_04.md](P3_API_04.md) - Medium HTTP 4XX Rate > 10%
- [P3_API_05.md](P3_API_05.md) - High P95 Response Time > 1s
- [P2_API_06.md](P2_API_06.md) - Critical P95 Response Time > 2s
- [P1_API_07.md](P1_API_07.md) - Service Down/Unhealthy

## Quick Reference

### Monitoring URLs

- Prometheus: <http://localhost:9090>
- Grafana: <http://localhost:3000>
- Kibana: <http://localhost:5601>
- Application: <http://localhost:8000>

### Emergency Commands

```bash
# Check service status
docker compose ps

# Restart all services
docker compose restart

# View logs
docker compose logs backend

# Check metrics
curl http://localhost:8000/metrics
```

## Escalation Process

1. **P1 Alerts**: Immediate response required
   - Follow SOP within 5 minutes
   - Escalate to on-call engineer if not resolved in 15 minutes

2. **P2 Alerts**: High priority
   - Follow SOP within 2 hours
   - Escalate if not resolved within 4 hours

3. **P3 Alerts**: Medium priority
   - Follow SOP within 24 hours
   - Can be handled during business hours
