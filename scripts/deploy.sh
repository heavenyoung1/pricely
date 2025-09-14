#!/bin/bash
docker-compose up -d
sleep 10  # Подождать, пока БД запустятся
alembic -c alembic_dev.ini upgrade head
alembic -c alembic_test.ini upgrade head
pytest  # Или ваши тесты
# Если тесты прошли, запустить app