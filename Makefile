.PHONY: up down migrate-dev migrate-test migrate-all test

up:
	docker-compose up -d

make -n down:
	docker-compose down -v

migrate-dev:
	ALEMBIC_DATABASE_URL=$$(uv run python scripts/db_url.py) uv run alembic upgrade head

migrate-test:
	ALEMBIC_DATABASE_URL=$$(uv run python scripts/db_url.py test) uv run alembic upgrade head

migrate-all: migrate-dev migrate-test
	@echo "Миграции успешно применены к обеим БД"

test: migrate-test
	uv run pytest -v