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
        self.settings = settings or DataBaseSettings()
        self._engine = None
        self._session_factory = None

    def init_engine(self):
        '''Инициализирует движок SQLAlchemy и фабрику сессий (ленивая инициализация).'''
        if self._engine is None:
            db_url = self._settings.get_db_url()
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
                autoflush=False,
                autocommit=False,
                expire_on_commit=False,
                class_=None,  # по умолчанию orm.Session
            )

    @contextmanager
    def get_session(self):
        '''
        Фабрика для получения контекстного менеджера сессии.
        Используется в UnitOfWork.
        '''
        if self._session_factory is None:
            self.init_engine()

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

db_settings = DataBaseSettings()
db = DatabaseConnection(db_settings)


# Это фабрика, которую будет использовать UnitOfWork
get_session = db.get_session