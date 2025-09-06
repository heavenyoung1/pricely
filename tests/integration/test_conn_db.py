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

    def get_engine(self):
        '''Создает и возвращает движок SQLAlchemy для работы с БД.

        Движок управляет пулом подключений и является точкой входа для всех операций с БД.

        Returns:
            Engine: Объект движка SQLAlchemy.
        '''
        if self._engine is None:
            try:
                self._engine = create_engine(
                    self.settings.get_db_url(),
                    pool_size=10,
                    max_overflow=20,
                    pool_pre_ping=True,
                    echo=False  # Логирование SQL-запросов (True для отладки)
                )
                logger.info('Движок БД успешно создан')
            except Exception as e:
                logger.error(f'Ошибка создания движка БД: {e}')
                raise
        return self._engine

    def get_session_factory(self):
        '''Создает и возвращает фабрику сессий.'''
        if self._session_factory is None:
            engine = self.get_engine()
            self._session_factory = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=engine,
                expire_on_commit=False
            )
        return self._session_factory

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        '''Создаёт и возвращает сессию SQLAlchemy как контекстный менеджер.

        Returns:
            Session: Объект сессии SQLAlchemy.
        '''
        session = None
        try:
            SessionLocal = self.get_session_factory()
            session = SessionLocal()
            logger.info('Сессия БД успешно инициализирована')
            yield session
        except Exception as e:
            if session:
                session.rollback()
            logger.error(f'Ошибка в сессии БД: {e}')
            raise
        finally:
            if session:
                session.close()
                logger.info('Сессия БД закрыта')

    def test_connection(self) -> bool:
        '''Проверяет подключение к базе данных.'''
        try:
            engine = self.get_engine()
            with engine.connect() as conn:
                result = conn.execute(text('SELECT 1'))
                return result.fetchone()[0] == 1
        except SQLAlchemyError as e:
            logger.error(f'Ошибка подключения к БД: {e}')
            return False

    def get_database_info(self) -> dict:
        '''Получает информацию о подключенной базе данных.'''
        try:
            with self.get_session() as session:
                # Получаем название БД
                db_name = session.execute(text('SELECT current_database()')).fetchone()[0]
                # Получаем версию PostgreSQL
                version = session.execute(text('SELECT version()')).fetchone()[0]
                # Получаем текущего пользователя
                user = session.execute(text('SELECT current_user')).fetchone()[0]

                return {
                    'database': db_name,
                    'user': user,
                    'version': version.split()[0:2],  # PostgreSQL version
                    'status': 'connected'
                }
        except SQLAlchemyError as e:
            logger.error(f'Ошибка получения информации о БД: {e}')
            return {
                'status': 'error',
                'error': str(e)
            }


# Глобальный экземпляр для удобного использования
db_connection = DatabaseConnection()

