from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Dict, Optional


class Settings(BaseSettings):
    '''
    :param headless: Запуск без графического интерфейса
    :param user_agent: Пользовательский user-agent
    :param proxy: Прокси-сервер (http://host:port)
    :param wait_time: Зарезервировано для будущих фич
    '''
    # Telegram Bot Settings
    TELEGRAM_TOKEN: str = "your-telegram-bot-token"
    TELEGRAM_API_URL: str = "https://api.telegram.org"

    # Selenium Settings
    SELENIUM_HEADLESS: bool = True
    SELENIUM_PROXY: Optional[str] = None
    SELENIUM_WAIT_TIME: int = 10

    DEFAULT_USER_AGENT: str = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) " 
    "Chrome/90.0.4430.212 Safari/537.36 "
)

    SELENIUM_CHROME_ARGS: List[str] = [
        "--no-sandbox",
        "--disable-gpu",
        "--disable-blink-features=AutomationControlled",
        "--start-maximized",
        "--log-level=3",
    ]

    SELENIUM_STEALTH_SETTINGS: Dict = {
        "languages": ["en-US", "en"],
        "vendor": "Google Inc.",
        "platform": "Win32",
        "webgl_vendor": "Intel Inc.",
        "renderer": "Intel Iris OpenGL Engine",
        "fix_hairline": True,
    }

   # Scheduler Settings
    SCHEDULER_INTERVAL_MINUTES: int = 60  # Интервал парсинга (в минутах)

    # Storage Settings
    STORAGE_FILE_PATH: str = "data/storage.json"

    model_config = SettingsConfigDict(
        env_file = ".env",  # Загрузка из .env файла
        env_file_encoding = "utf-8",
    )

# Создание экземпляра настроек
settings = Settings()

