import pytest
from src.infrastructure.database.core import DataBaseSettings, DatabaseConnection, get_session, get_engine
from src.core.db_config import DataBaseSettings
from src.core.db_connection import DatabaseConnection, 


class TestDatabaseConnection:
    """Тесты для проверки подключения к базе данных."""

    @pytest.fixture
    def db_settings(self):
        """Фикстура с настройками БД."""
        return DataBaseSettings()

    @pytest.fixture
    def db_connection(self, db_settings):
        """Фикстура с подключением к БД."""
        return DatabaseConnection(db_settings)

    def test_settings_load(self, db_settings):
        """Тест загрузки настроек."""
        assert db_settings.HOST is not None
        assert db_settings.PORT > 0
        assert db_settings.USER is not None
        assert db_settings.PASS is not None
        assert db_settings.NAME is not None
        assert "postgresql" in db_settings.CONN

    def test_database_url_format(self, db_settings):
        """Тест правильности формата URL подключения."""
        url = db_settings.get_db_url()
        assert url.startswith("postgresql")
        assert db_settings.HOST in url
        assert str(db_settings.PORT) in url
        assert db_settings.USER in url
        assert db_settings.NAME in url

    def test_connection_success(self, db_connection):
        """Тест успешного подключения к БД."""
        is_connected = db_connection.test_connection()
        assert is_connected is True, "Не удалось подключиться к базе данных"

    def test_session_creation(self, db_connection):
        """Тест создания сессии."""
        with db_connection.get_session() as session:
            assert session is not None
            # Простой запрос для проверки работы сессии
            result = session.execute(text("SELECT 1")).fetchone()
            assert result[0] == 1

    def test_database_info(self, db_connection):
        """Тест получения информации о БД."""
        info = db_connection.get_database_info()
        assert info["status"] == "connected"
        assert "database" in info
        assert "user" in info
        assert "version" in info

        # Проверяем, что подключились к правильной БД
        expected_db = db_connection.settings.NAME
        assert info["database"] == expected_db
        
        # Проверяем пользователя
        expected_user = db_connection.settings.USER
        assert info["user"] == expected_user

    def test_global_functions(self):
        """Тест глобальных функций для совместимости."""
        # Тест get_engine()
        engine = get_engine()
        assert engine is not None

        # Тест get_session()
        with get_session() as session:
            assert session is not None
            result = session.execute(text("SELECT 1")).fetchone()
            assert result[0] == 1

    def test_session_rollback_on_error(self, db_connection):
        """Тест отката транзакции при ошибке."""
        try:
            with db_connection.get_session() as session:
                # Намеренно вызываем ошибку
                session.execute(text("SELECT * FROM non_existent_table"))
        except Exception:
            # Ошибка ожидаема, проверяем что сессия корректно закрылась
            pass

        # Проверяем что новая сессия работает нормально
        with db_connection.get_session() as session:
            result = session.execute(text("SELECT 1")).fetchone()
            assert result[0] == 1


# example_usage.py - Примеры использования
def example_usage():
    """Примеры использования DatabaseConnection."""
    
    # Способ 1: Использование класса напрямую
    db = DatabaseConnection()
    
    # Проверка подключения
    if db.test_connection():
        print("✅ Подключение успешно!")
        
        # Получение информации о БД
        info = db.get_database_info()
        print(f"База данных: {info['database']}")
        print(f"Пользователь: {info['user']}")
        
        # Использование сессии
        with db.get_session() as session:
            result = session.execute(text("SELECT current_timestamp")).fetchone()
            print(f"Текущее время в БД: {result[0]}")
    
    # Способ 2: Использование глобальных функций (как в вашем коде)
    print("\nИспользование глобальных функций:")
    with get_session() as session:
        result = session.execute(text("SELECT version()")).fetchone()
        print(f"Версия PostgreSQL: {result[0].split()[0:2]}")


if __name__ == "__main__":
    example_usage()