from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from functools import wraps


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

def get_db_engine():
    '''Создаёт и возвращает движок SQLAlchemy для подключения к базе данных'''
    db_settings = DataBaseSettings()
    engine = create_engine(db_settings.get_connection_db())
    return engine

def get_db_session():
    '''Создаёт и возвращает фабрику сессий SQLAlchemy'''
    engine = get_db_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal

def with_session(func):
    '''Декоратор для управления сессией SQLAlchemy'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        SessionLocal = get_db_session()
        with SessionLocal() as session:
            try:
                result = func(*args, session=session, **kwargs)
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
    return wrapper