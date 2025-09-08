.PHONY: up down migrate-dev migrate-test test

up:
	docker-compose up -d

down:
	docker-compose down -v

migrate-dev:
	alembic upgrade head --sqlalchemy-url=postgresql://myuser:mypassword@localhost:5432/mydb

migrate-test:
	alembic upgrade head --sqlalchemy-url=postgresql://myuser:mypassword@localhost:5433/mydb_test

test: migrate-test
	pytest -v
