
.DEFAULT_GOAL := help

# Variables
COMPOSE_FILE := docker-compose.yaml
COMPOSE_OBSERVABILITY := docker-compose.observability.yml
BACKEND_DIR := backend
FRONTEND_DIR := frontend
DOCKER_PATH := /Applications/Docker.app/Contents/Resources/bin
DOCKER := docker
DOCKER_COMPOSE := docker compose

# Check if Docker is available in PATH, otherwise use full path
ifeq ($(shell which docker),)
    DOCKER := /Applications/Docker.app/Contents/Resources/bin/docker
    DOCKER_COMPOSE := /Applications/Docker.app/Contents/Resources/bin/docker compose
endif

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

.PHONY: help
help: ## Show this help message
	@echo "$(BLUE)MyTodoApp Development Commands$(NC)"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ {printf "$(GREEN)%-20s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Commands
.PHONY: dev
dev: ## Start all services with Docker Compose
	@echo "$(BLUE)Starting development environment...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) up --build -d
	@echo "$(GREEN)Services started successfully!$(NC)"
	@echo "Frontend: http://localhost:3001"
	@echo "Backend:  http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "API Healthcheck: http://localhost:8000/healthz"
	@echo "Grafana：http://localhost:3000 (admin/admin)"
	@echo "Elasticsearch：http://localhost:9200 (elastic/password)"
	@echo "Prometheus：http://localhost:9090"
	@echo "Kibana：http://localhost:5601 (elastic/password)"
	@make reset-kibana-password

load_test: ## Load test data into the database
	@echo "$(BLUE)Loading test data into the database...$(NC)"
	./scripts/load_test.py
	@echo "$(GREEN)Test data loaded successfully!$(NC)"

.PHONY: dev-observability
dev-observability: ## Start with full observability stack
	@echo "$(BLUE)Starting with observability stack...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_OBSERVABILITY) up --build -d
	@echo "$(GREEN)Observability stack started successfully!$(NC)"
	@echo "Frontend:      http://localhost:3001"
	@echo "Backend:       http://localhost:8000"
	@echo "Grafana:       http://localhost:3000"
	@echo "Prometheus:    http://localhost:9090"
	@echo "Kibana:        http://localhost:5601"

.PHONY: dev-db
dev-db: ## Start only the database for local development
	@echo "$(BLUE)Starting database only...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) up -d db
	@echo "$(GREEN)Database started successfully!$(NC)"

.PHONY: frontend-install
frontend-install: ## Install frontend dependencies
	@echo "$(BLUE)Installing frontend dependencies...$(NC)"
	cd $(FRONTEND_DIR) && npm install
	@echo "$(GREEN)Frontend dependencies installed!$(NC)"

.PHONY: frontend-dev
frontend-dev: ## Run frontend in development mode
	@echo "$(BLUE)Starting frontend development server...$(NC)"
	cd $(FRONTEND_DIR) && npm start

.PHONY: backend-dev
backend-dev: ## Run backend locally with hot reload
	@echo "$(BLUE)Starting backend development server...$(NC)"
	@echo "$(YELLOW)Make sure database is running: make dev-db$(NC)"
	cd $(BACKEND_DIR) && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Testing Commands
.PHONY: test
test: ## Run backend tests
	@echo "$(BLUE)Running backend tests...$(NC)"
	cd $(BACKEND_DIR) && python -m pytest

.PHONY: test-verbose
test-verbose: ## Run backend tests with verbose output
	@echo "$(BLUE)Running backend tests (verbose)...$(NC)"
	cd $(BACKEND_DIR) && python -m pytest -v

.PHONY: test-frontend
test-frontend: ## Run frontend tests
	@echo "$(BLUE)Running frontend tests...$(NC)"
	cd $(FRONTEND_DIR) && npm test

.PHONY: test-integration
test-integration: ## Run integration tests
	@echo "$(BLUE)Running integration tests...$(NC)"
	cd $(BACKEND_DIR) && python -m pytest -m integration

.PHONY: test-all
test-all: ## Run all tests
	@echo "$(BLUE)Running all tests...$(NC)"
	$(MAKE) test
	$(MAKE) test-frontend

# Utility Commands
.PHONY: logs
logs: ## Show application logs
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) logs -f

.PHONY: logs-backend
logs-backend: ## Show backend logs only
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) logs -f backend

.PHONY: logs-frontend
logs-frontend: ## Show frontend logs only
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) logs -f frontend

.PHONY: shell-backend
shell-backend: ## Open shell in backend container
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) exec backend bash

.PHONY: shell-frontend
shell-frontend: ## Open shell in frontend container
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) exec frontend sh

.PHONY: shell-db
shell-db: ## Connect to PostgreSQL database
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) exec db psql -U postgres -d mytodoapp



.PHONY: reset-kibana-password
reset-kibana-password: # Reset kibana_system password because Kibana by default uses 'kibana_system' user and its initial password is unknowingly random
	@curl -X POST "http://localhost:9200/_security/user/kibana_system/_password" \
	-u elastic:password \
	-H "Content-Type: application/json" \
	-d '{ "password": "password" }'

.PHONY: install-n8n
install-n8n: ## Create n8n database and restart n8n service
	@echo "$(BLUE)Creating n8n database...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) exec -T db psql -U postgres -c "CREATE DATABASE n8n;"
	@echo "$(BLUE)Restarting n8n service...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) restart n8n
	@echo "$(GREEN)n8n database created and service restarted!$(NC)"

# Cleanup Commands
.PHONY: stop
stop: ## Stop all services
	@echo "$(BLUE)Stopping services...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) down
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_OBSERVABILITY) down 2>/dev/null || true
	@echo "$(GREEN)Services stopped!$(NC)"

.PHONY: clean
clean: ## Stop services and remove containers/volumes
	@echo "$(BLUE)Cleaning up containers and volumes...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) down -v --remove-orphans
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_OBSERVABILITY) down -v --remove-orphans 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

.PHONY: reset
reset: clean ## Full reset (clean + rebuild)
	@echo "$(BLUE)Performing full reset...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker system prune -f
	$(MAKE) dev
	@echo "$(GREEN)Reset complete!$(NC)"

# Setup Commands
.PHONY: setup
setup: ## Initial setup for new developers
	@echo "$(BLUE)Setting up development environment...$(NC)"
	$(MAKE) frontend-install
	$(MAKE) dev
	@echo "$(GREEN)Setup complete!$(NC)"
	@echo ""
	@echo "$(YELLOW)Next steps:$(NC)"
	@echo "1. Wait for services to start (30-60 seconds)"
	@echo "2. Visit http://localhost:3001 for the frontend"
	@echo "3. Visit http://localhost:8000/docs for API documentation"

.PHONY: check-ports
check-ports: ## Check if required ports are available
	@echo "$(BLUE)Checking required ports...$(NC)"
	@echo "Port 3001 (frontend): $$(lsof -ti:3001 >/dev/null 2>&1 && echo '$(RED)BUSY$(NC)' || echo '$(GREEN)AVAILABLE$(NC)')"
	@echo "Port 8000 (backend):  $$(lsof -ti:8000 >/dev/null 2>&1 && echo '$(RED)BUSY$(NC)' || echo '$(GREEN)AVAILABLE$(NC)')"
	@echo "Port 5432 (database): $$(lsof -ti:5432 >/dev/null 2>&1 && echo '$(RED)BUSY$(NC)' || echo '$(GREEN)AVAILABLE$(NC)')"

# Development helpers
.PHONY: format-backend
format-backend: ## Format backend code
	@echo "$(BLUE)Formatting backend code...$(NC)"
	cd $(BACKEND_DIR) && python -m black app/ tests/ 2>/dev/null || echo "$(YELLOW)black not installed$(NC)"
	cd $(BACKEND_DIR) && python -m isort app/ tests/ 2>/dev/null || echo "$(YELLOW)isort not installed$(NC)"

.PHONY: lint-backend
lint-backend: ## Lint backend code
	@echo "$(BLUE)Linting backend code...$(NC)"
	cd $(BACKEND_DIR) && python -m flake8 app/ tests/ 2>/dev/null || echo "$(YELLOW)flake8 not installed$(NC)"
	cd $(BACKEND_DIR) && python -m mypy app/ 2>/dev/null || echo "$(YELLOW)mypy not installed$(NC)"

.PHONY: format-frontend
format-frontend: ## Format frontend code
	@echo "$(BLUE)Formatting frontend code...$(NC)"
	cd $(FRONTEND_DIR) && npm run format 2>/dev/null || echo "$(YELLOW)format script not available$(NC)"

.PHONY: build
build: ## Build production images
	@echo "$(BLUE)Building production images...$(NC)"
	export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) build
	@echo "$(GREEN)Build complete!$(NC)"

# Status check
.PHONY: status
status: ## Show status of all services
	@echo "$(BLUE)Service Status:$(NC)"
	@export PATH="$(DOCKER_PATH):$$PATH" && docker compose -f $(COMPOSE_FILE) ps