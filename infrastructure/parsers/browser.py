import random
from typing import Optional
from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    Playwright,
)

from application.interfaces.browser import IBrowserManager
from .options import (
    USER_AGENTS,
    BROWSER_ARGS,
    CONTEXT_OPTIONS,
    DEFAULT_TIMEOUT,
    NAVIGATION_TIMEOUT,
)

from core.config.settings import settings
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
        headless: bool = settings.HEADLESS,
        proxy: Optional[dict] = None,
        user_agent: Optional[str] = None,
        delay: int = 2000,
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
        self.delay = delay

        # Внутренние объекты Playwright
        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        logger.info(f'[PROXY CHECK] {proxy}')

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
        logger.info(f'[PROXY BROWSER] {launch_options}')
        # Запускаем Chromium
        self._browser = await self._playwright.chromium.launch(
            **launch_options, proxy=self.proxy
        )

        # Создаем контекст с реалистичными настройками
        await self._create_context()

        logger.info(
            f'Браузер запущен, режим headless {"ВКЛЮЧЕН" if self.headless else "ОТКЛЮЧЕН"} ,User-Agent {self.user_agent[:50]}...',
        )

    async def _create_context(self) -> None:
        '''Создает контекст браузера с настройками антидетекта'''
        try:
            if not self._browser:
                logger.error(f'Браузер не запущен')
                raise RuntimeError('Браузер не запущен')

            # Копируем базовые настройки контекста
            context_opts = CONTEXT_OPTIONS.copy()

            # Добавляем User-Agent
            context_opts['user_agent'] = self.user_agent

            # Добавляем прокси если указан (с поддержкой аутентификации)
            if self.proxy:
                context_opts['proxy'] = self.proxy
                logger.info(
                    f'[BROWSER] Прокси добавлен в контекст: server={self.proxy.get("server")}'
                )
                logger.debug(f'[BROWSER] Полные настройки прокси: {self.proxy}')
            else:
                logger.info('[BROWSER] Прокси НЕ используется (proxy=None)')

            logger.debug(
                f'[BROWSER] Создание контекста с опциями: {list(context_opts.keys())}'
            )

            # Создаем контекст
            self._context = await self._browser.new_context(**context_opts)

            logger.info('[BROWSER] Контекст браузера успешно создан')

            # Устанавливаем таймауты
            self._context.set_default_timeout(DEFAULT_TIMEOUT)
            self._context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)

        except Exception as e:
            logger.error(f'[BROWSER] Ошибка создания контекста: {e}')
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

        try:
            # Переходим по URL
            await page.goto(url, wait_until='domcontentloaded')

            # Небольшая задержка для загрузки динамического контента
            await page.wait_for_timeout(self.delay)

            logger.info(f'Страница загружена URL - {url}')

            return page
        except Exception as e:
            # Закрываем страницу при ошибке навигации
            await page.close()
            logger.error(f'Ошибка загрузки страницы {url}: {e}')
            raise

    async def close(self) -> None:
        '''
        Корректно закрывает браузер и Playwright
        Освобождает все ресурсы
        '''
        if self._context:
            await self._context.close()
            self._context = None

        if self._browser:
            await self._browser.close()
            self._browser = None

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None

        logger.info(f'Браузер закрыт')

    @staticmethod
    def _get_random_user_agent() -> str:
        '''Возвращает случайный User-Agent из списка'''
        return random.choice(USER_AGENTS)

    async def __aenter__(self):
        '''Поддержка async context manager'''
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        '''Автоматическое закрытие при выходе из контекста'''
        await self.close()
