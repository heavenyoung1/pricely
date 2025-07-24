from dotenv import load_dotenv
import os

from utils.logger import logger

# Загружаем переменные из .env
load_dotenv()

# Telegram
bot_token = os.getenv("BOT_TOKEN")
chat_id = os.getenv("CHAT_ID")

if not bot_token or not chat_id:
    logger.error('Отсутствуют BOT_TOKEN или CHAT_ID в .env файле')
    raise ValueError("Отсутствуют BOT_TOKEN или CHAT_ID в .env файле")

#------------------------------------
from pydantic_settings import BaseSettings, SettingsConfigDict

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

   # Scheduler Settings
    SCHEDULER_INTERVAL_MINUTES: int = 60  # Интервал парсинга (в минутах)

    # Storage Settings
    STORAGE_FILE_PATH: str = "data/storage.json"

    model_config = SettingsConfigDict(
        env_file = ".env"  # Загрузка из .env файла
        env_file_encoding = "utf-8"
    )

