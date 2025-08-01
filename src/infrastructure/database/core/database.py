from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from typing import Generator


class DataBaseSettings(BaseSettings):
    '''Настройки подключения к базе данных'''
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
        '''Формирует строку подключения для PostgreSQL'''
        return f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'

# Инициализация настроек БД   
db_settings = DataBaseSettings()

# Создание движка (engine)
engine = create_engine(
    db_settings.get_connection_db(),
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False  # Включить для отладки SQL-запросов
)

# Фабрика сессий
SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

# Генератор сессий
def get_db() -> Generator[Session, None, None]:
    """Генератор сессий для работы с БД"""
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()

# Инициализация базы данных (создание таблиц)
def init_db():
    from src.infrastructure.database.models.base import Base
    Base.metadata.create_all(bind=engine)