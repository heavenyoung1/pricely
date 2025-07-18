from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from utils.logger import logger
from typing import Dict, List, Optional
import time
from selenium.webdriver.remote.webelement import WebElement


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
            logger.info("WebDriver успешно инициализирован")
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

    def find_element(self, by: str, value: str) -> WebElement:
        """Поиск одного элемента на странице"""
        try:    
            element = self.driver.find_element(by=By.__getattribute__(by), value=value)
            return element
        except Exception as e:
            logger.error(f"Ошибка при поиске элементов: {e}")
            return 
        
    def find_elements(self, by: str, value: str) -> List[WebElement]:
            """Поиск нескольких элементов на странице"""
            try:
                return self.driver.find_elements(by=By.__getattribute__(by), value=value)
            except Exception as e:
                logger.error(f"Ошибка при поиске элементов: {e}")
                return []

    def get_cookies(self) -> List[Dict]:
        """Возвращает текущие куки браузера"""
        logger.info(self.driver.get_cookies())
        return self.driver.get_cookies()
    
    
    def get_headers(self) -> Dict[str, str]:
        return {
            "User-Agent": self.user_agent,
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Connection": "keep-alive",
        }
    
    def navigate(self, url: str, wait_after: int = 10) -> None:
        """Переходит по указанному URL и ожидает загрузки"""
        try:
            self.driver.get(url)
            time.sleep(wait_after) # Ожидание для загрузки контента
            logger.info(f'Вы успешно перешли на {url}')
        except Exception as e:
            logger.error(f'Ошибка перехода на {url}. Ошибка {e}')
            raise

    def refresh_session(self, url: str = None) -> None:
        """Обновляет сессию, очищая куки и переходя на URL (если указан)"""
        try:
            self.driver.delete_all_cookies()
            logger.info("Куки очищены")
            if url:
                self.navigate(url)
        except Exception as e:
            logger.error(f"Ошибка при обновлении сессии: {e}")
            raise     
    
    def close(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("WebDriver закрыт")

    def __enter__(self):
        """Поддержка контекстного менеджера"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие при выходе из контекстного менеджера"""
        self.close()
