from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class Settings(BaseSettings):
    '''Конфигурация приложения'''

    # Telegram Bot
    BOT_TOKEN: str
    APP_VERSION: str

    # Конфиг БД
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Redis
    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_QUEUE_NAME: str = 'pricely:notifications'

    # Checker
    CHECKER_CRON: str = '0 */4 * * *'  # каждые 4 часа

    # SQLAlchemy параметры (PostgreSQL)
    DRIVER: str = 'postgresql+asyncpg'
    SYNC_DRIVER: str = 'postgresql+psycopg2'

    # Browser
    HEADLESS: bool = True
    DELAY: int = 2000

    @property
    def redis_url(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    def url(self) -> URL:
        '''Собрать URL подключения безопасно'''
        return URL.create(
            drivername=self.DRIVER,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=self.DB_NAME,
        )

    def alembic_url(self) -> str:
        '''Строка для подключения к БД ТОЛЬКО для выполнения Alembic миграций.'''
        url = f'{self.SYNC_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        return url

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
    )


# Standalone на всё приложение
settings = Settings()
