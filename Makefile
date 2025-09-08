.PHONY: up down migrate-dev migrate-test test

up:
	docker-compose up -d

down:
	docker-compose down -v

migrate-dev:
	alembic upgrade head --sqlalchemy-url=$$(python scripts/db_url.py)

migrate-test:
	alembic upgrade head --sqlalchemy-url=$$(python scripts/db_url.py test)

test: migrate-test
	pytest -v
