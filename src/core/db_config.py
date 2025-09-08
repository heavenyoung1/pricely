import logging
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

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

    # Опциональные настройки для тестовой БД
    TEST_NAME: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file='.env', 
        env_prefix='DB_', 
        env_file_encoding='utf-8',
        extra='ignore',  # Игнорировать лишние переменные
    )

    def get_db_url(self) -> str:
        '''Возвращает URL для подключения к базе данных.'''
        return f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'
    
    def get_test_db_url(self) -> str:
        '''Возвращает URL для подключения к тестовой базе данных.'''
        return f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.TEST_NAME}'
    
    def get_alembic_url(self, use_test: bool = False) -> str:
        '''
        Возвращает строку подключения для Alembic.
        (Alembic работает с драйвером postgresql, без +psycopg2)
        '''
        conn = 'postgresql'  # Alembic ожидает именно это
        name = self.TEST_NAME if use_test else self.NAME
        if not name:
            raise ValueError('Имя базы данных не указано')
        return f'{conn}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{name}'

    @property
    def is_test_db_configured(self) -> bool:
        '''Проверяет, настроена ли тестовая БД.'''
        return self.TEST_NAME is not None