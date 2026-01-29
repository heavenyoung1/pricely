"""
Пример настроек Playwright с undetected-плагинами для парсинга Ozon
"""

import asyncio
import random
from typing import Optional

from playwright.async_api import async_playwright, Browser, BrowserContext, Page


class PlaywrightBrowser:
    """Класс для работы с Playwright в stealth режиме"""

    def __init__(
        self,
        headless: bool = True,
        proxy: Optional[dict] = None,
        user_agent: Optional[str] = None,
    ):
        self.headless = headless
        self.proxy = proxy
        self.user_agent = user_agent or self._get_random_user_agent()
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None

    @staticmethod
    def _get_random_user_agent() -> str:
        """Возвращает случайный реалистичный user-agent"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        return random.choice(user_agents)

    async def start(self):
        """Запускает браузер с настройками stealth"""
        playwright = await async_playwright().start()

        # Настройки запуска браузера
        launch_options = {
            'headless': self.headless,
            'args': [
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
            ],
        }

        # Добавляем прокси, если указан
        if self.proxy:
            launch_options['proxy'] = self.proxy

        self.browser = await playwright.chromium.launch(**launch_options)

        # Настройки контекста браузера
        context_options = {
            'viewport': {'width': 1920, 'height': 1080},
            'user_agent': self.user_agent,
            'locale': 'ru-RU',
            'timezone_id': 'Europe/Moscow',
            'permissions': ['geolocation'],
            'geolocation': {'latitude': 55.7558, 'longitude': 37.6173},  # Москва
            'color_scheme': 'light',
            'extra_http_headers': {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            },
        }

        self.context = await self.browser.new_context(**context_options)

        # Добавляем скрипты для обхода детекции ботов
        await self.context.add_init_script(
            """
            // Удаляем webdriver флаг
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });

            // Переопределяем plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });

            // Переопределяем languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['ru-RU', 'ru', 'en-US', 'en']
            });

            // Переопределяем chrome
            window.chrome = {
                runtime: {}
            };

            // Переопределяем permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
        """
        )

        return self.context

    async def create_page(self) -> Page:
        """Создает новую страницу с дополнительными настройками"""
        if not self.context:
            await self.start()

        page = await self.context.new_page()

        # Дополнительные настройки страницы
        await page.set_extra_http_headers(
            {
                'Referer': 'https://www.ozon.ru/',
            }
        )

        return page

    async def close(self):
        """Закрывает браузер и контекст"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()

    async def __aenter__(self):
        """Async context manager entry"""
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()


# Пример использования
async def example_usage():
    """Пример использования PlaywrightBrowser для парсинга Ozon"""

    # Настройка прокси (опционально)
    proxy_config = {
        'server': 'http://proxy.example.com:8080',
        # 'username': 'user',
        # 'password': 'pass',
    }

    # Создаем экземпляр браузера
    browser = PlaywrightBrowser(
        headless=True,  # False для отладки
        proxy=proxy_config,  # None если не используем прокси
    )

    try:
        # Создаем страницу
        page = await browser.create_page()

        # Переходим на страницу товара Ozon
        url = 'https://www.ozon.ru/product/example-product/'
        await page.goto(url, wait_until='networkidle', timeout=30000)

        # Добавляем случайную задержку для имитации человеческого поведения
        await asyncio.sleep(random.uniform(2, 5))

        # Парсим данные
        # Пример: получение названия товара
        title = await page.locator('h1').first.inner_text()

        # Пример: получение цены
        price_element = await page.locator('[data-widget="webPrice"]').first
        price = await price_element.inner_text()

        print(f'Название: {title}')
        print(f'Цена: {price}')

        # Дополнительные действия для обхода детекции
        # Прокрутка страницы (имитация чтения)
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(random.uniform(1, 3))
        await page.evaluate('window.scrollTo(0, 0)')
        await asyncio.sleep(random.uniform(0.5, 1.5))

    finally:
        await browser.close()


if __name__ == '__main__':
    asyncio.run(example_usage())
