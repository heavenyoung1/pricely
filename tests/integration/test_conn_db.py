import pytest
from src.core.db_connection import DatabaseConnection
from src.core.db_config import DataBaseSettings


@pytest.mark.integration
def test_connection_to_both_databases():
    """
    Интеграционный тест:
    Проверяет, что можно подключиться к основной и тестовой БД.
    """

    settings = DataBaseSettings()

    # Проверка основной базы
    dev_db = DatabaseConnection(settings)
    assert dev_db.test_connection(), (
        "Не удалось подключиться к основной БД. "
        "Проверьте .env или доступность контейнера postgres_dev."
    )

    # Проверка тестовой базы
    if not settings.is_test_db_configured:
        pytest.skip("Тестовая БД не настроена в .env")
    test_settings = DataBaseSettings(NAME=settings.TEST_NAME)
    test_db = DatabaseConnection(test_settings)
    assert test_db.test_connection(), (
        "Не удалось подключиться к тестовой БД. "
        "Проверьте .env или доступность контейнера postgres_test."
    )
