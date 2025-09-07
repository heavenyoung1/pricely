import pytest
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command
from src.core.db_config import DataBaseSettings
from src.core.db_connection import DatabaseConnection
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def test_db_settings():
    """Фикстура для настроек тестовой БД."""
    return DataBaseSettings()

@pytest.fixture(scope="session")
def test_db(test_db_settings):
    """Фикстура для тестовой БД: создаёт БД и применяет миграции."""
    test_db_name = "test_db"
    db = DatabaseConnection(test_db_settings)
    
    # Создаём тестовую БД
    db.recreate_test_db(test_db_name)
    
    # Настраиваем Alembic для тестовой БД
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", test_db_settings.get_test_db_url(test_db_name))
    
    # Применяем миграции
    logger.info("Применение миграций к тестовой БД")
    command.upgrade(alembic_cfg, "head")
    
    yield db
    
    # Очищаем БД после тестов
    logger.info("Очистка тестовой БД")
    command.downgrade(alembic_cfg, "base")
    db.dispose()

@pytest.fixture
def db_session(test_db):
    """Фикстура для сессии БД с транзакцией для каждого теста."""
    with test_db.get_session() as session:
        yield session