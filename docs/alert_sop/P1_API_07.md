# P1_API_07 - Service Down/Unhealthy

## Impact

Critical service outage. The MyTodoApp backend service is completely unreachable or failing health checks for more than 5 minutes. Users cannot access any functionality, resulting in complete service unavailability.

## Diagnose

### Step 1: Service Status Check

1. Check if service is responding: `curl -f http://localhost:8000/health` or visit in browser
2. Check container status: `docker compose ps`
3. Look for crashed/restarting containers
4. Check Prometheus targets at `http://localhost:9090/targets` to see scrape status

### Step 2: Container and Docker Investigation

1. Check container logs: `docker compose logs backend --tail=50`
2. Check if containers are running: `docker compose ps`
3. Look for restart loops: `docker stats` and monitor container uptime
4. Check Docker daemon status: `docker system info`

### Step 3: Resource Availability

1. Check system resources: `docker stats`
2. Check disk space: `df -h`
3. Check memory usage: `free -h`
4. Verify network connectivity between containers: `docker network ls`

### Step 4: Database and Dependencies

1. Check database availability: `docker compose exec db pg_isready -U user`
2. Test database connection: `docker compose exec db psql -U user -d tododb -c "SELECT 1;"`
3. Check if other dependencies are running: `docker compose ps`

## Fix

### Step 1: Immediate Service Recovery

1. **Restart All Services**:

   ```bash
   # Quick restart of all services
   docker compose restart
   ```

2. **If Restart Fails, Rebuild**:

   ```bash
   # Force rebuild if containers are corrupted
   docker compose down
   docker compose up --build -d
   ```

### Step 2: Database Recovery

1. **Check Database Health**:

   ```bash
   # Restart database if it's the issue
   docker compose restart db
   
   # Wait for database to be ready
   docker compose exec db pg_isready -U user
   ```

2. **Database Emergency Recovery**:
   - If database is corrupted, restore from backup
   - Check database logs for corruption indicators

### Step 3: Resource Issues

1. **Free Up Resources**:

   ```bash
   # Clean up unused containers and images
   docker system prune -f
   
   # Remove unused volumes if disk space is critical
   docker volume prune -f
   ```

2. **Scale Down Other Services** (if resource constrained):

   ```bash
   # Temporarily disable non-critical services
   docker compose stop grafana kibana elasticsearch
   ```

### Step 4: Network and Configuration

1. **Check Environment Variables**:
   - Verify all required environment variables are set
   - Check `.env` file for correct configuration

2. **Port Conflicts**:
   - Check if ports are already in use: `lsof -i :8000`
   - Kill processes using required ports if needed

### Step 5: Emergency Fallback

1. **Manual Container Start**:

   ```bash
   # Start only critical services
   docker compose up -d db
   docker compose up -d backend
   docker compose up -d frontend
   ```

2. **Health Check Verification**:
   - Test each service individually
   - Verify backend health endpoint: `curl http://localhost:8000/docs`
   - Check frontend: `curl http://localhost:3001`

### Step 6: Communication and Escalation

1. **Immediate Notification**:
   - Notify stakeholders of service outage
   - Provide estimated recovery time

2. **Post-Recovery Actions**:
   - Monitor service stability for 30 minutes
   - Review logs for root cause
   - Update incident documentation
   - Plan post-mortem if outage was significant
