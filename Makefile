
.PHONY: dev
dev:
	docker compose -f docker-compose.yaml up --build -d

.PHONY: test
test:
	. venv/bin/activate && pytest

.PHONY: test-all
test-all:
	. venv/bin/activate && pytest -m ""

.PHONY: test-integration
test-integration:
	. venv/bin/activate && pytest -m integration