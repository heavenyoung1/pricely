.PHONY: up down migrate-dev migrate-test migrate-all test bot tests

up:
	docker-compose up -d

make -n down:
	docker-compose down -v

migrate-dev:
	ALEMBIC_DATABASE_URL=$$(python3 -c "from src.core.db_config import DataBaseSettings; db = DataBaseSettings(); print(db.get_alembic_url(use_test=False))") uv run alembic upgrade head

migrate-test:
	ALEMBIC_DATABASE_URL=$$(python3 -c "from src.core.db_config import DataBaseSettings; db = DataBaseSettings(); print(db.get_alembic_url(use_test=True))") uv run alembic upgrade head

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