from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import logging
from typing import Optional
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

logger = logging.getLogger(__name__)

class SessionEngine:
    '''Класс для управления сессией браузера с поддержкой кук и заголовков'''

    def __init__(
            self,
            headless: bool = False,
            user_agent: Optional[str] = None,
            proxy: Optional[str] = None,
            wait_time: int = 10,
    ):
        '''
        Инициализация движка сессии.

        Args:
            headless (bool): Запуск браузера в headless-режиме (без GUI).
            user_agent (str, optional): Пользовательский user-agent.
            proxy (str, optional): Прокси-сервер в формате http://host:port.
            wait_time (int): Время ожидания для загрузки страниц (сек).
        '''
        self.headless = headless
        self.user_agent = user_agent or (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/129.0.0.0 Safari/537.36'
        )
        self.proxy = proxy
        self.wait_time = wait_time
        self.driver: Optional[webdriver.Chrome] = None
        self._initialize_driver()

    def _initialize_driver(self) -> None:
        '''Инициализирует WebDriver с заданными настройками'''
        try:
            options = Options()
            chrome_args = [
                '--no-sandbox',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled',
                '--start-maximized',
                '--disable-logging',
            ]

            if self.headless:
                chrome_args.append('--headless=new')
            if self.user_agent:
                chrome_args.append(f'--user-agent={self.user_agent}')
            if self.proxy:
                chrome_args.append(f'--proxy-server={self.proxy}')

            for arg in chrome_args:
                options.add_argument(arg)

            self.driver = webdriver.Chrome(options=options)
            self._apply_stealth_settings()
            logger.info('WebDriver успешно инициализирован.')
        except Exception as e:
            logger.error(f'Ошибка при инициализации WebDriver: {e}')
            raise

    def _apply_stealth_settings(self) -> None:
        '''Применяет stealth-настройки для маскировки браузера'''
        try:
            stealth(
                self.driver,
                languages=['en-US', 'en'],
                vendor='Google Inc.',
                platform='Win32',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=True,
                user_agent=self.user_agent,
            )
            logger.info('Stealth-настройки успешно применены.')
        except Exception as e:
            logger.error(f'Ошибка при применении stealth-настроек: {e}')
            raise

    def navigate(self, url: str) -> None:
        '''Переходит по указанному URL и ожидает загрузки страницы'''
        try:
            self.driver.get(url)
            # Используем WebDriverWait для более надежного ожидания элементов
            WebDriverWait(self.driver, self.wait_time).until(
                EC.presence_of_element_located((By.TAG_NAME, 'body'))
            )
            logger.info(f'Успешно загружена страница: {url}')
        except Exception as e:
            logger.error(f'Ошибка при загрузке страницы {url}: {e}')
            raise

    def _extract_text(self, element) -> str:
        '''Извлекает текст из элемента, если он существует'''
        return element.text.strip() if element else 'N/A'

    def quit(self) -> None:
        '''Закрывает WebDriver'''
        if self.driver:
            try:
                self.driver.quit()
                logger.info('WebDriver успешно закрыт.')
            except Exception as e:
                logger.error(f'Ошибка при закрытии WebDriver: {e}')
