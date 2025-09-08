.PHONY: up down migrate-dev migrate-test test migrate-all

up:
	docker-compose up -d

down:
	docker-compose down -v

migrate-dev:
	alembic upgrade head --sqlalchemy-url=$$(python3 scripts/db_url.py)

migrate-test:
	alembic upgrade head --sqlalchemy-url=$$(python3 scripts/db_url.py test)

migrate-all: migrate-dev migrate-test
	@echo "Миграции успешно применены к обеим БД"

test: migrate-test
	pytest -v
