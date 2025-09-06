# src/infrastructure/database/core.py
import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager
from typing import Generator

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class DataBaseSettings(BaseSettings):
    '''Настройки подключения к базе данных PostgreSQL.

    Читает параметры из .env файла с префиксом DB_CONFIG_.
    Автоматически проверяет типы данных и обязательные поля.

    Attributes:
        HOST (str): Хост базы данных (например, 'localhost').
        PORT (int): Порт базы данных (обычно 5432 для PostgreSQL).
        USER (str): Имя пользователя БД.
        PASS (str): Пароль пользователя.
        NAME (str): Название базы данных.
        CONN (str): Драйвер подключения (по умолчанию 'postgresql+psycopg2').
    '''
    HOST: str
    PORT: int = 5432
    USER: str
    PASS: str
    NAME: str
    CONN: str = 'postgresql+psycopg2'

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_prefix='DB_CONFIG_', 
        env_file_encoding='utf-8',
        extra='ignore',  # Игнорировать лишние переменные
    )

    def get_db_url(self) -> str:
        '''Возвращает URL для подключения к базе данных.'''
        return f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'

# def get_engine():
#     '''Создает и возвращает движок SQLAlchemy для работы с БД.

#     Движок управляет пулом подключений и является точкой входа для всех операций с БД.

#     Returns:
#         Engine: Объект движка SQLAlchemy.
#     '''
#     try:
#         db_settings = DataBaseSettings()
#         engine = create_engine(
#             db_settings.get_connection_db(),
#             pool_size=10,
#             max_overflow=20,
#             pool_pre_ping=True,
#             echo=False  # Логирование SQL-запросов (True для отладки)
#         )
#         logger.info('Движок БД успешно создан')
#         return engine
#     except Exception as e:
#         logger.error(f'Ошибка создания движка БД: {e}')
#         raise

# @contextmanager
# def get_session() -> Generator:
#     '''Создаёт и возвращает сессию SQLAlchemy как контекстный менеджер.

#     Returns:
#         Session: Объект сессии SQLAlchemy.
#     '''
#     try:
#         engine = get_engine()
#         SessionLocal = sessionmaker(
#             autocommit=False,
#             autoflush=False,
#             bind=engine,
#             expire_on_commit=False
#         )
#         session = SessionLocal()
#         logger.info('Сессия БД успешно инициализирована')
#         yield session
#     except Exception as e:
#         logger.error(f'Ошибка создания сессии: {e}')
#         raise
#     finally:
#         session.close()
#         logger.info('Сессия БД закрыта')