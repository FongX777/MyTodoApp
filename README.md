# AlertingScout

AlertingScout is a task management application with integrated observability features, allowing you to track tasks and monitor system performance.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Node.js and npm

### Running the Basic Application

1. **Start Docker:** Make sure your Docker daemon is running.

2. **Install frontend dependencies:**

   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Run the application:**

   ```bash
   docker compose up --build
   ```

4. The frontend will be available at `http://localhost:3001`.
5. The backend API will be available at `http://localhost:8000`.

### Running with Observability Stack

For enhanced monitoring and logging capabilities, you can run the application with the full observability stack:

```bash
docker compose -f docker-compose.observability.yml up --build
```

This will start the following services:

- Backend API with Prometheus metrics and structured logging: `http://localhost:8000`
- Frontend: `http://localhost:3001`
- PostgreSQL database
- Prometheus (metrics collection): `http://localhost:9090`
- Grafana (metrics visualization): `http://localhost:3000`
- Elasticsearch (log storage): `http://localhost:9200`
- Kibana (log visualization): `http://localhost:5601`

### Testing

The backend tests are located in the `backend/tests` directory. You can run them with:

```bash
docker compose exec backend pytest
```

## Troubleshooting

### Elasticsearch Issues

If Elasticsearch shows unhealthy status:

- Check available disk space on your system
- If necessary, decrease memory allocation in docker-compose.observability.yml
- For development environments, consider disabling disk watermarks as shown in the config
