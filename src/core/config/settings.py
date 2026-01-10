from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения (читается из .env файла)."""

    # === AIOSQLite параметры ===
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # SQLAlchemy параметры
    DRIVER: str = "sqlite+aiosqlite://"


settings = Settings()
