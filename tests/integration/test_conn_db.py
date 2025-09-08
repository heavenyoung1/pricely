import pytest
import asyncio
from sqlalchemy import text, inspect
from src.core import DatabaseConnection, DataBaseSettings
import os

class TestDatabaseConnections:
    '''Интеграционные тесты для проверки подключения к базам данных'''
    
    @pytest.mark.integration
    def test_connection_to_both_databases(self):
        '''
        Интеграционный тест:
        Проверяет, что можно подключиться к основной и тестовой БД.
        '''
        settings = DataBaseSettings()

        # Проверка основной базы
        dev_db = DatabaseConnection(settings)
        assert dev_db.test_connection(), (
            'Не удалось подключиться к основной БД. '
            'Проверьте .env или доступность контейнера postgres_dev.'
        )
        print('✅ Основная БД подключена успешно')

        # Проверка тестовой базы
        if not settings.is_test_db_configured:
            pytest.skip('Тестовая БД не настроена в .env')
            
        # Создаем настройки для тестовой БД с правильным портом
        test_settings = DataBaseSettings(
            NAME=settings.TEST_NAME,
            PORT=settings.TEST_PORT or 5433  # Используем порт 5433 для тестовой БД
        )
        test_db = DatabaseConnection(test_settings)
        assert test_db.test_connection(), (
            'Не удалось подключиться к тестовой БД. '
            'Проверьте .env или доступность контейнера postgres_test.'
        )