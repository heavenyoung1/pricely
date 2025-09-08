.PHONY: up down migrate-dev migrate-test migrate-all test

up:
	docker-compose up -d

down:
	docker-compose down -v

migrate-dev:
	uv run alembic upgrade head -x sqlalchemy.url=$$(uv run python scripts/db_url.py)

migrate-test:
	uv run alembic upgrade head -x sqlalchemy.url=$$(uv run python scripts/db_url.py test)

migrate-all: migrate-dev migrate-test
	@echo "Миграции успешно применены к обеим БД"

test: migrate-test
	uv run pytest -v
