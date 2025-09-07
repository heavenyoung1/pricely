import pytest
from src.core.db_connection import DatabaseConnection
from src.core.db_config import DataBaseSettings


@pytest.mark.integration
def test_database_connection():
    """
    Интеграционный тест:
    Проверяет, что можно подключиться к БД и выполнить простой запрос.
    """

    settings = DataBaseSettings()
    db = DatabaseConnection(settings)

    assert db.test_connection(), (
        "Не удалось подключиться к БД. "
        "Проверьте .env конфиг или доступность сервера PostgreSQL."
    )
