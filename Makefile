.PHONY: up down migrate-dev migrate-test migrate-all test bot tests

up:
	docker-compose up -d

make -n down:
	docker-compose down -v

migrate-dev:
	@echo "Формирование ALEMBIC_DATABASE_URL для dev..."
	@ALEMBIC_DATABASE_URL=$$(uv run python -c "from src.core.db_connection import db_settings; print(db_settings.get_alembic_url(use_test=False))"); \
	echo "ALEMBIC_DATABASE_URL=$$ALEMBIC_DATABASE_URL"; \
	ALEMBIC_DATABASE_URL=$$ALEMBIC_DATABASE_URL uv run alembic upgrade head

migrate-test:
	@echo "Формирование ALEMBIC_DATABASE_URL для test..."
	@ALEMBIC_DATABASE_URL=$$(uv run python -c "from src.core.db_connection import db_settings; print(db_settings.get_alembic_url(use_test=True))"); \
	echo "ALEMBIC_DATABASE_URL=$$ALEMBIC_DATABASE_URL"; \
	ALEMBIC_DATABASE_URL=$$ALEMBIC_DATABASE_URL uv run alembic upgrade head
	
migrate-all: migrate-dev migrate-test
	@echo "Миграции успешно применены к обеим БД"
	
# Запуск бота
bot:
	uv run python -m src.main

# Запуск тестов
tests:
	uv run python -m pytest tests -v -s --log-level=DEBUG
