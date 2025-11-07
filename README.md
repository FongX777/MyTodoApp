# MyTodoApp

MyTodoApp is a task management application with integrated observability features, allowing you to track tasks and monitor system performance.

## Quick Start

For new users who want to get started immediately:

```bash
# 1. Clone the repository
git clone <repository-url>
cd MyTodoApp

# 2. Start the application
make dev

# 3. Load test data for demonstration purposes
make load_test

# 4. Access the application
# Frontend: http://localhost:3001
# Backend API: http://localhost:8000
# API docs: http://localhost:8000/docs
# API metrics: http://localhost:8000/metrics
# Grafana: http://localhost:3000 (admin/admin)


# 5. Install n8n again
make install-n8n
```

## Prerequisites

- Docker & Docker Compose
- Python 3.12+ (for local development)
- Node.js (v20 or later) and npm (optional, for frontend development)

## Development Commands

Use these Makefile commands for common development tasks:

```bash
make dev                    # Start all services with Docker Compose
make dev-observability      # Start with full observability stack
make frontend-install       # Install frontend dependencies
make frontend-dev           # Run frontend in development mode
make backend-dev            # Run backend locally with hot reload
make test                   # Run backend tests
make test-frontend          # Run frontend tests
make logs                   # Show application logs
make clean                  # Stop and remove all containers
make reset                  # Full reset (clean + rebuild)
```

## Running Options

### 1. Basic Application (Recommended for Development)

```bash
make dev
```

This starts:

- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3001`
- PostgreSQL database
- API documentation: `http://localhost:8000/docs`

### 2. With Observability Stack (Production-like)

```bash
make dev-observability
```

Additional services:

- Prometheus (metrics): `http://localhost:9090`
- Grafana (dashboards): `http://localhost:3000`
- Elasticsearch (logs): `http://localhost:9200`
- Kibana (log analysis): `http://localhost:5601`

### 3. Local Development (Hot Reload)

For active development with hot reload:

```bash
# Terminal 1: Start database
make dev-db

# Terminal 2: Run backend locally
make backend-dev

# Terminal 3: Run frontend locally
make frontend-dev
```

## Project Structure

```text
MyTodoApp/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   ├── tests/           # Backend tests
│   └── Dockerfile       # Backend container
├── frontend/            # React frontend
│   ├── src/            # Frontend source code
│   ├── public/         # Static assets
│   └── Dockerfile      # Frontend container
├── dev/                # Development tools
│   ├── grafana/        # Grafana configuration
│   ├── prometheus/     # Prometheus configuration
│   └── elasticsearch/  # Elasticsearch configuration
└── scripts/            # Utility scripts
```

## API Documentation

Once the backend is running, visit:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

## Testing

```bash
# Backend tests
make test

# Frontend tests (when available)
make test-frontend

# Integration tests
make test-integration

# All tests
make test-all
```

## Development Workflow

1. **Start development environment:**

   ```bash
   make dev
   make frontend-install
   ```

2. **Make changes:**

   - Backend: Edit files in `backend/app/`
   - Frontend: Edit files in `frontend/src/`

3. **Test changes:**

   ```bash
   make test
   ```

4. **View logs:**

   ```bash
   make logs
   ```

## Troubleshooting

### Common Issues

**Port conflicts:**

- Ensure ports 3001, 8000, 5432 are available
- Use `docker compose down` to stop existing containers

**Database connection issues:**

- Wait for database to be ready (may take 30-60 seconds on first start)
- Check logs: `make logs`

**Frontend dependencies:**

- Run `make frontend-install` after any package.json changes
- Clear node_modules: `rm -rf frontend/node_modules && make frontend-install`

**Elasticsearch (observability mode):**

- Requires sufficient disk space and memory
- If unhealthy, try: `make clean && make dev-observability`

### Reset Everything

If you encounter persistent issues:

```bash
make reset
```

This stops all containers, removes volumes, and rebuilds from scratch.

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and test: `make test`
3. Submit a pull request

For detailed development guidelines, see the project's specification documents in `/specs/`.
