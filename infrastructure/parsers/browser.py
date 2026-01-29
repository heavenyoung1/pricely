import random
from typing import Optional
from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)

from domain.interfaces.browser import IBrowserManager
from .options import (
    USER_AGENTS,
    BROWSER_ARGS,
    CONTEXT_OPTIONS,
    DEFAULT_TIMEOUT,
    NAVIGATION_TIMEOUT,
)

from core.logger import logger


class BrowserManager(IBrowserManager):
    '''
    Менеджер браузера на Playwright

    Особенности:
    - Использует stealth режим для обхода антибот систем
    - Рандомизирует User-Agent для каждого запуска
    - Настраивает реалистичные заголовки HTTP
    - Поддерживает прокси (опционально)
    '''

    def __init__(
        self,
        headless: bool = True,
        proxy: Optional[dict] = None,
        user_agent: Optional[str] = None,
    ):
        '''
        Args:
            headless: Запускать браузер без GUI (True) или с GUI (False)
            proxy: Настройки прокси {'server': 'http://...', 'username': '...', 'password': '...'}
            user_agent: Кастомный User-Agent (если None - выбирается рандомный)
        '''
        self.headless = headless
        self.proxy = proxy
        self.user_agent = user_agent or self._get_random_user_agent()

        # Внутренние объекты Playwright
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None

    async def start(self) -> None:
        '''
        Запускает Playwright и браузер с антидетект настройками
        Вызывается автоматически при первом обращении к браузеру
        '''
        if self._browser:
            return  # Браузер уже запущен

        # Запускаем Playwright
        self._playwright = await async_playwright().start()

        # Конфигурация запуска браузера
        launch_options = {
            'headless': self.headless,
            'args': BROWSER_ARGS,
        }

        # Добавляем прокси если указан
        if self.proxy:
            launch_options['proxy'] = self.proxy

        # Запускаем Chromium
        self._browser = await self._playwright.chromium.launch(**launch_options)

        # Создаем контекст с реалистичными настройками
        await self._create_context()

        logger.info(
            f'Браузер запущен, режим headless включен -> {self.headless}',
            f'User-Agent {self.user_agent[:50]}...',
        )

    async def _create_create(self) -> None:
        '''Создает контекст браузера с настройками антидетекта'''
        try:
            if not self._browser:
                logger.error(f'Браузер не запущен')
                raise RuntimeError('Браузер не запущен')

            # Копируем базовые настройки контекста
            context_opts = CONTEXT_OPTIONS.copy()

            # Добавляем User-Agent
            context_opts['user_agent'] = self.user_agent

            # Создаем контекст
            self._context = await self._browser.new_context(**context_opts)

            # Устанавливаем таймауты
            self._context.set_default_timeout(DEFAULT_TIMEOUT)
            self._context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)

        except Exception as e:
            logger.error(f'Ошибка {e}')
            raise Exception(f'Ошибка {e}')

    async def get_browser(self) -> Browser:
        '''
        Возвращает объект браузера
        Автоматически запускает браузер если он не запущен
        '''
        if not self._browser:
            await self.start()
        return self._browser

    async def get_context(self) -> BrowserContext:
        '''
        Возвращает контекст браузера
        Автоматически запускает браузер если он не запущен
        '''
        if not self._context:
            await self.start()
        return self._context

    async def open_page(self, url: str) -> Page:
        '''
        Открывает новую страницу и переходит по URL

        Args:
            url: Адрес страницы

        Returns:
            Page: Объект страницы Playwright

        Example:
            page = await browser.open_page('https://www.ozon.ru/category/noutbuki-15692/')
        '''
        context = await self.get_context()

        # Создаем новую страницу
        page = await context.new_page()

        logger.debug(f'Открываем страницу URL - {url}')

        # Переходим по URL
        await page.goto(url, wait_until='domcontentloaded')

        # Небольшая задержка для загрузки динамического контента
        await page.wait_for_timeout(1000)

        logger.info(f'Страница загружена URL - {url}')

        return page
