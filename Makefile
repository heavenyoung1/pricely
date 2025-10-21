.PHONY: up down migrate-dev migrate-test migrate-all test bot tests

up:
	docker-compose up -d

make -n down:
	docker-compose down -v

migrate-dev:
	export DB_HOST=localhost && \
	export DB_USER=$(DB_USER) && \
	export DB_PASS=$(DB_PASS) && \
	export DB_NAME=pricely_db && \
	export DB_PORT=5432 && \
	ALEMBIC_DATABASE_URL="postgresql://$(DB_USER):$(DB_PASS)@localhost:5432/pricely_db" uv run alembic upgrade head

migrate-test:
	export DB_HOST=localhost && \
	export DB_USER=$(DB_USER) && \
	export DB_PASS=$(DB_PASS) && \
	export DB_NAME=pricely_test_db && \
	export DB_PORT=5433 && \
	ALEMBIC_DATABASE_URL="postgresql://$(DB_USER):$(DB_PASS)@localhost:5433/pricely_test_db" uv run alembic upgrade head


migrate-all: migrate-dev migrate-test
	@echo "Миграции успешно применены к обеим БД"

test: migrate-test
	uv run pytest -v
	
# Запуск бота
bot:
	uv run python -m src.main

# Запуск тестов
tests:
	uv run python -m pytest tests -v -s --log-level=DEBUG

# migrate-dev:
# 	ALEMBIC_DATABASE_URL=$$(uv run python scripts/db_url.py dev) uv run alembic upgrade head

# migrate-test:
# 	ALEMBIC_DATABASE_URL=$$(uv run python scripts/db_url.py test) uv run alembic upgrade head