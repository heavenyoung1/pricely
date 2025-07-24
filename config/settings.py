from pydantic_settings import BaseSettings, SettingsConfigDict

from utils.logger import logger

class Settings(BaseSettings):
    # Telegram Bot Settings
    TELEGRAM_TOKEN: str = "your-telegram-bot-token"
    TELEGRAM_API_URL: str = "https://api.telegram.org"

    # Selenium Settings
    SELENIUM_HEADLESS: bool = True

    DEFAULT_USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) " 
    "Chrome/90.0.4430.212 Safari/537.36 "
)
    SELENIUM_PROXY: str | None = None
    SELENIUM_WAIT_TIME: int = 10

   # Scheduler Settings
    SCHEDULER_INTERVAL_MINUTES: int = 60  # Интервал парсинга (в минутах)

    # Storage Settings
    STORAGE_FILE_PATH: str = "data/storage.json"

    model_config = SettingsConfigDict(
        env_file = ".env"  # Загрузка из .env файла
        env_file_encoding = "utf-8"
    )

# Создание экземпляра настроек
settings = Settings()

