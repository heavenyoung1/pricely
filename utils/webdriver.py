# from selenium import webdriver
# from selenium_stealth import stealth

# def init_driver(): 
#     options = webdriver.ChromeOptions()
#     options.add_argument("--start-maximized")
#     options.add_argument("--disable-blink-features=AutomationControlled")
#     options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     options.add_experimental_option("useAutomationExtension", False)
    
#     driver = webdriver.Chrome(options=options)
    
#     stealth(driver,
#             languages=["en-US", "en"],
#             vendor="Google Inc.",
#             platform="Win32",
#             webgl_vendor="Intel Inc.",
#             renderer="Intel Iris OpenGL Engine",
#             fix_hairline=True,
#             user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    
#     return driver

import logging
from typing import Optional
from contextlib import contextmanager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from selenium_stealth import stealth
from fake_useragent import UserAgent
from threading import Lock
from utils import logger

class DriverConfig:
    """ Конфигурация для WebDriver """
    HEADLESS: bool = True
    TIMEOUT: int = 10
    LANGUAGES: list = ['en-US', 'en']
    VENDOR: str = "Google Inc."
    PLATFORM: str = "Win32"
    WEBGL_VENDOR: str = "Intel Inc."
    RENDERER: str = "Intel Iris OpenGL Engine"
    FIX_HAIRLINE: bool = True

class DriverPool:
    """Пул WebDriver для повторного использования"""
    def __init__(self, max_drivers: int = 5):
        self.max_drivers = max_drivers
        self.drivers: list[WebDriver] = []
        self.lock = Lock()
        self._initialize_pool()
                
    def _initialize_pool(self):
        """Инициализирует пул драйверов"""
        for _ in range(self.max_drivers):
            try:
                    driver = self._create_driver()
                    self.drivers.append(driver)
                    logger.info("Инициализирован WebDriver")
            except Exception as e:
                    logger.error(f"Ошибка инициализации WebDriver: {str(e)}")
                        
    def _create_driver(self) -> WebDriver:
        """Создаёт новый экземпляр WebDriver."""
        options = Options()
        if DriverConfig.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # Случайный User-Agent
        ua = UserAgent()
        user_agent = ua.random
                
        driver = webdriver.Chrome(options=options)
                
        # Применяем stealth
        stealth(
        driver,
        languages=DriverConfig.LANGUAGES,
        vendor=DriverConfig.VENDOR,
        platform=DriverConfig.PLATFORM,
        webgl_vendor=DriverConfig.WEBGL_VENDOR,
        renderer=DriverConfig.RENDERER,
        fix_hairline=DriverConfig.FIX_HAIRLINE,
        user_agent=user_agent,
        )
            
        return driver
        
    @contextmanager
    def get_driver(self) -> WebDriver:
        """Получает драйвер из пула."""
        with self.lock:
            if not self.drivers:
                logger.warning("Все драйверы заняты, создаём новый")
                self.drivers.append(self._create_driver())
            driver = self.drivers.pop()
        
        try:
            yield driver
        finally:
            with self.lock:
                self.drivers.append(driver)
                logger.debug("Драйвер возвращён в пул")

    def close_all(self):
        """Закрывает все драйверы."""
        with self.lock:
            for driver in self.drivers:
                try:
                    driver.quit()
                    logger.info("Драйвер закрыт")
                except Exception as e:
                    logger.error(f"Ошибка при закрытии драйвера: {str(e)}")
            self.drivers.clear()

# Глобальный пул драйверов (singleton)
_driver_pool: Optional[DriverPool] = None

def init_driver_pool(max_drivers: int = 5) -> DriverPool:
    """Инициализирует глобальный пул драйверов."""
    global _driver_pool
    if _driver_pool is None:
        _driver_pool = DriverPool(max_drivers)
    return _driver_pool

def get_driver() -> WebDriver:
    """Получает драйвер из пула."""
    pool = init_driver_pool()
    with pool.get_driver() as driver:
        yield driver