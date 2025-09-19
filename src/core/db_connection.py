import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
from contextlib import contextmanager
from typing import Generator

from src.core.db_config import DataBaseSettings

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class DatabaseConnection:
    '''Класс для управления подключением к базе данных и сессиями.'''

    def __init__(self, settings: DataBaseSettings = None):
        '''
        Инициализация подключения к базе данных.
        
        Args:
            settings: Настройки БД. Если не указаны, будут загружены автоматически.
        '''
        self._settings = settings or DataBaseSettings()
        self._engine = None
        self._session_factory = None

    def init_engine(self, db_url: str = None):
        '''Инициализирует движок SQLAlchemy и фабрику сессий (ленивая инициализация).'''
        if self._engine is None:
            db_url = db_url or self._settings.get_database_url(use_test=False)
            logger.info(f'Инициализация подключения к БД: {db_url}')

            # создаём Engine
            self._engine = create_engine(
                db_url,
                echo=False,            # можно True для отладки SQL
                future=True,           # включаем SQLAlchemy 2.0 API
                pool_pre_ping=True,    # проверка соединения перед использованием
            )

            # создаём sessionmaker
            self._session_factory = sessionmaker(
                bind=self._engine,
                class_=Session,
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
            )

    @contextmanager
    def get_session(self, db_url: str = None) -> Generator[Session, None, None]:
        '''
        Фабрика для получения контекстного менеджера сессии.
        Используется в UnitOfWork.
        '''
        if self._session_factory is None:
            self.init_engine(db_url)

        session = self._session_factory()
        try:
            yield session
        finally:
            session.close()

    def dispose(self):
        '''Закрывает все соединения и освобождает ресурсы.'''
        if self._engine is not None:
            logger.info('Закрытие всех соединений с БД')
            self._engine.dispose()
            self._engine = None
            self._session_factory = None

    def test_connection(self, db_url: str = None) -> bool:
        '''Проверка доступности БД (выполняется SELECT 1).

        Args:
            db_url (str, optional): URL для подключения к БД. Если None, используется get_db_url.
        '''
        self.init_engine(db_url)
        try:
            with self._engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Подключение к БД успешно установлено")
            return True
        except Exception as e:
            logger.error(f"Ошибка подключения к БД: {e}")
            return False

db_settings = DataBaseSettings()
db = DatabaseConnection(db_settings)


# Это фабрика, которую будет использовать UnitOfWork
get_session = db.get_session