import logging
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

# Настройка логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)

class DataBaseSettings(BaseSettings):
    '''
    Настройки подключения к базе данных PostgreSQL.

    Читает параметры из .env файла с префиксом DB_CONFIG_.
    Автоматически проверяет типы данных и обязательные поля.

    Attributes:
        HOST (str): Хост базы данных (например, 'localhost').
        PORT (int): Порт базы данных (обычно 5432 для PostgreSQL).
        USER (str): Имя пользователя БД.
        PASS (str): Пароль пользователя.
        NAME (str): Название базы данных.
        CONN (str): Драйвер подключения (по умолчанию 'postgresql+psycopg2').
        TEST_NAME (Optional[str]): Название тестовой базы данных (если используется).
        TEST_PORT (Optional[int]): Порт тестовой базы данных (если используется).
    '''
    HOST: str
    PORT: int = 5432
    USER: str
    PASS: str
    NAME: str
    CONN: str = 'postgresql+psycopg2'

    # Опциональные настройки для тестовой БД
    TEST_NAME: Optional[str] = None
    TEST_PORT: Optional[int] = None

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='DB_',
        env_file_encoding='utf-8',
        extra='ignore',  # Игнорировать лишние переменные
    )

    def __init__(self, **kwargs):
        # Дебаг: выводим все переменные окружения перед инициализацией
        logger.debug(">>> Загружаем настройки базы данных...")
        self._debug_print_env_vars()  # Функция для дебага переменных окружения

        # Инициализация базы данных через Pydantic
        super().__init__(**kwargs)
        
        # Дебаг: выводим атрибуты, загруженные из настроек
        logger.debug(f"DB Settings Loaded: {self.model_dump()}")

    def _debug_print_env_vars(self):
        """
        Печатает все переменные окружения, которые начинаются с DB_.
        """
        logger.debug(">>> Текущие переменные окружения:")
        for key, value in os.environ.items():
            if key.startswith('DB_'):
                logger.debug(f"{key}: {value}")

    def get_database_url(self, use_test: bool = False) -> str:
        '''
        Формирует URL для подключения к базе данных с использованием SQLAlchemy.

        :param use_test: Флаг, указывающий, использовать ли тестовую базу данных.
        :return: Строка подключения для SQLAlchemy.
        '''
        if use_test:
            name = self.TEST_NAME
            port = self.TEST_PORT
        else:
            name = self.NAME
            port = self.PORT

        db_url = f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{port}/{name}'
        logger.debug(f"⚠️ Сгенерирован database URL: {db_url}")
        return db_url

    def get_alembic_url(self, use_test: bool = False) -> str:
        '''
        Формирует URL для Alembic (без использования psycopg2).

        :param use_test: Флаг, указывающий, использовать ли тестовую базу данных.
        :return: Строка подключения для Alembic.
        '''
        if use_test:
            name = self.TEST_NAME
            port = self.TEST_PORT
        else:
            name = self.NAME
            port = self.PORT

        alembic_url = f'postgresql://{self.USER}:{self.PASS}@{self.HOST}:{port}/{name}'
        logger.debug(f"⚠️ Сгенерирован Alembic URL: {alembic_url}")
        return alembic_url

    @property
    def is_test_db_configured(self) -> bool:
        '''
        Проверяет, настроена ли тестовая база данных.

        :return: True, если тестовая база данных настроена, иначе False.
        '''
        return self.TEST_NAME is not None