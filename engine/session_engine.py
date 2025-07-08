from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from utils.logger import logger
from typing import Dict, List, Optional
import time


class SessionEngine:
    """Класс для управления сессией браузера с поддержкой кук и заголовков"""

    def __init__(
            self,
            headless: bool = False,
            user_agent: Optional[str] = None,
            proxy: Optional[str] = None,
            wait_time: int = 10,
    ):
        """
        Инициализация движка сессии.

        :param headless: Запуск браузера в headless-режиме.
        :param user_agent: Пользовательский user-agent.
        :param proxy: Прокси-сервер (http://host:port).
        :param wait_time: Время ожидания для загрузки страниц.
        """
        self.headless = headless
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/90.0.4430.212 Safari/537.36"
        )
        self.proxy = proxy
        self.wait_time = wait_time
        self.driver: Optional[webdriver.Chrome] = None
        self._initialize_driver()

    def _initialize_driver(self) -> None:
        """Инициализирует WebDriver с заданными настройками"""
        try:
            options = Options()
            chrome_args = [
                "--no-sandbox",
                "--disable-gpu",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--disable-logging",  # Подавление логов GPU
            ]

            if self.headless:
                chrome_args.append("--headless=new")
            if self.user_agent:
                chrome_args.append(f"--user-agent={self.user_agent}")
            if self.proxy:
                chrome_args.append(f"--proxy-server={self.proxy}")

            for arg in chrome_args:
                options.add_argument(arg)

            self.driver = webdriver.Chrome(options=options)
            self._apply_stealth_settings()
            logger.info("WebDriver успешно инициализирован.")
        except Exception as e:
            logger.error(f"Ошибка при инициализации WebDriver: {e}")
            raise
    
    def _apply_stealth_settings(self) -> None:
        """Применяет stealth-настройки для маскировки"""
        stealth(
            self.driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            user_agent=self.user_agent,
        )