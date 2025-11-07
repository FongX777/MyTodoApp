
.PHONY: dev
dev:
	docker compose -f docker-compose.yaml up --build -d

test:
	pytest -v tests/