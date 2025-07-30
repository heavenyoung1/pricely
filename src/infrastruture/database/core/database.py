from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine

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
        connection_str = f'{self.CONN}://{self.USER}:{self.PASS}@{self.HOST}:{self.PORT}/{self.NAME}'
        return connection_str

# Инициализация настроек БД   
db_settings = DataBaseSettings()

# Создание движка (engine)
engine = db_settings.get_connection_db()

# Фабрика сессий
SessionFactory = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
