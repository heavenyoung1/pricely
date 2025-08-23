from functools import wraps
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth
from typing import Dict, List, Optional, Callable
import time
import logging

logger = logging.getLogger(__name__)

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

        Args:
            headless (bool): Запуск браузера в headless-режиме (без GUI).
            user_agent (str, optional): Пользовательский user-agent.
            proxy (str, optional): Прокси-сервер в формате http://host:port.
            wait_time (int): Время ожидания для загрузки страниц (сек).
        """
        self.headless = headless
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/129.0.0.0 Safari/537.36"
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
                "--disable-logging",
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
        """Применяет stealth-настройки для маскировки браузера"""
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

    def navigate(self, url: str) -> None:
        """Переходит по указанному URL и ожидает загрузки страницы"""
        try:
            self.driver.get(url)
            time.sleep(self.wait_time)  # Даем странице время на загрузку
            logger.info(f"Успешно загружена страница: {url}")
        except Exception as e:
            logger.error(f"Ошибка при загрузке страницы {url}: {e}")
            raise

    def _extract_text(self, element) -> str:
        """Извлекает текст из элемента, если он существует"""
        return element.text.strip() if element else "N/A"

    def quit(self) -> None:
        """Закрывает WebDriver"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver успешно закрыт.")
            except Exception as e:
                logger.error(f"Ошибка при закрытии WebDriver: {e}")

def session_engine_decorator(headless: bool = False, user_agent: Optional[str] = None, proxy: Optional[str] = None, wait_time: int = 10):
    """
    Декоратор для управления сессией WebDriver с использованием SessionEngine.

    Создает и настраивает экземпляр SessionEngine, передает его в декорируемую функцию,
    а после выполнения (успешного или с ошибкой) закрывает WebDriver.

    Args:
        headless (bool): Запуск браузера в headless-режиме (без GUI).
        user_agent (str, optional): Пользовательский user-agent.
        proxy (str, optional): Прокси-сервер в формате http://host:port.
        wait_time (int): Время ожидания для загрузки страниц (сек).

    Returns:
        Callable: Обернутая функция, управляющая сессией WebDriver.

    Пример использования:
        @session_engine_decorator(headless=True)
        def parse_product(session, url):
            session.navigate(url)
            name = session.execute_name_of_product()
            return name

        result = parse_product("https://www.ozon.ru/product/123456789")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = None
            try:
                session = SessionEngine(
                    headless=headless,
                    user_agent=user_agent,
                    proxy=proxy,
                    wait_time=wait_time
                )
                result = func(session, *args, **kwargs)
                return result
            except Exception as e:
                logger.error(f"Ошибка в декорируемой функции: {e}")
                raise
            finally:
                if session:
                    session.quit()
        return wrapper
    return decorator

# Пример функции парсинга с использованием декоратора
@session_engine_decorator(headless=True)
def execute_name_of_product(session: SessionEngine, url: str) -> str:
    """
    Извлекает название товара с указанной страницы на Ozon.

    Args:
        session (SessionEngine): Экземпляр движка сессии с настроенным WebDriver.
        url (str): URL страницы товара.

    Returns:
        str: Название товара или "N/A" в случае ошибки.
    """
    try:
        session.navigate(url)
        name_element = WebDriverWait(session.driver, session.wait_time).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-widget='webProductHeading']//h1"))
        )
        name = session._extract_text(name_element)
        logger.info(f"Найдено название товара: {name}")
        return name
    except Exception as e:
        logger.error(f"Ошибка при извлечении названия товара: {e}")
        return "N/A"

# Пример вызова
if __name__ == "__main__":
    ozon_url = "https://www.ozon.ru/product/dzhinsy-befree-883110146/"  # Замените на реальный URL
    product_name = execute_name_of_product(ozon_url)
    print(f"Название товара: {product_name}")