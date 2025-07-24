import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
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
        
