import logging
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import wraps
from typing import Any, Callable

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
    model_config = SettingsConfigDict(
        env_file = '.env', 
        env_prefix='DB_CONFIG_', 
        env_file_encoding = 'utf-8',
        extra='ignore', # Игнорировать лишние переменные
        )

    HOST: str
    PORT: int
    USER: str
    PASS: str
    NAME: str
    CONN: str = 'postgresql+psycopg2'

    def get_connection_db(self):
        '''Формирует строку подключения к PostgreSQL.

        Returns:
            str: Строка подключения в формате: 
            'postgresql+psycopg2://user:password@host:port/dbname'
        '''
        return f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'

def get_db_engine() -> Any:
    '''Создает и возвращает движок SQLAlchemy для работы с БД.

    Движок управляет пулом подключений и является точкой входа для всех операций с БД.

    Returns:
        Engine: Объект движка SQLAlchemy.
    '''
    try:
        db_settings = DataBaseSettings()
        engine = create_engine(
            db_settings.get_connection_db(),
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            echo=False  # Логирование SQL-запросов (True для отладки)
        )
        logger.info("Движок БД успешно создан")
        return engine
    except Exception as e:
        logger.error(f"Ошибка создания движка БД: {e}")
        raise

def get_db_session() -> str:
    '''Создаёт и возвращает фабрику сессий SQLAlchemy'''
    try:
        engine = get_db_engine()
        SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            expire_on_commit=False
        )
        logger.info("Фабрика сессий успешно инициализирована")
        return SessionLocal
    except Exception as e:
        logger.error(f"Ошибка создания фабрики сессий: {e}")
        raise

def with_session(func) -> Callable:
    '''Декоратор для автоматического управления сессиями БД.

    Автоматически:
    - Создает новую сессию
    - Передает ее в функцию как аргумент 'session'
    - Фиксирует изменения (commit) при успешном выполнении
    - Откатывает (rollback) при ошибках
    - Закрывает сессию

    Args:
        func (Callable): Функция, которая будет работать с БД.

    Returns:
        Callable: Обернутая функция с управлением сессией.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        SessionLocal = get_db_session()
        session = SessionLocal()
        try:
            logger.debug(f"Сессия БД запущена {func.__name__}")
            result = func(*args, session=session, **kwargs)
            session.commit()
            logger.debug("Коммит транзакции")
            return result
        except Exception as e:
            session.rollback()
            logger.error(f"ROLLBACK Транзакции с ошибкой: {e}")
            raise
        finally:
            session.close()
            logger.debug("Сессия БД закрыта")
    return wrapper