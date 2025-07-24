import logging
#from selenium import webdriver
#from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config.settings import settings
from infrastructure.parsers.selenium_driver import driver

# Настройка логгера
logger = logging.getLogger(__name__)

class SessionEngine:
    '''Класс для управления сессией браузера с помощью Selenium WebDriver'''

    def __init__(self, 
                headless: bool = settings.SELENIUM_HEADLESS, 
                user_agent: str = settings.DEFAULT_USER_AGENT, 
                proxy: str = None, 
                wait_time: int = settings.SELENIUM_WAIT_TIME):
        '''Инициализация сессии с WebDriver'''
        self.driver = driver(headless=headless, user_agent=user_agent, proxy=proxy, wait_time=wait_time)
        self.wait_time = wait_time
        logger.info("SessionEngine инициализирован")

    def open_page(self, url: str) -> None:
        logger.info(f'Открытие страницы: {url}')
        self.driver.get(url)

    def find_element(self, by: str, value: str):
        '''Ищет элемент на странице'''
        return WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((by, value))
        )
    
    def close(self) -> None:
       '''Закрывает WebDriver''' 
       if self.driver:
           self.driver.quit()
           self.driver = None
           logger.info('WebDriver закрыт')
    
    def __enter__(self):
        """Поддержка контекстного менеджера."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрытие при выходе из контекстного менеджера."""
        self.close()


