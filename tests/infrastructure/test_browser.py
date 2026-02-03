import pytest

from core.logger import logger
from infrastructure.parsers.browser import BrowserManager


@pytest.mark.asyncio
async def test_browser_starts_successfully():
    browser_manager = BrowserManager(headless=False)
    await browser_manager.start()
    browser = await browser_manager.get_browser()

    assert browser is not None
    assert browser.is_connected()

    await browser_manager.close()


@pytest.mark.asyncio
async def test_context_created():
    browser_manager = BrowserManager()

    context = await browser_manager.get_context()

    assert context is not None
    assert context.pages == []
    logger.debug(f'Context: {context}')

    await browser_manager.close()


async def test_discovery_context():
    '''Исследуем внутренности BrowserContext'''
    async with BrowserManager(headless=True) as browser_manager:
        context = await browser_manager.get_context()
        cookies = await context.cookies()
        logger.info(f'[CONTEXT] Browser Type: {context.browser.browser_type.name}')
        logger.info(f'[CONTEXT] Cookie: {cookies}')


@pytest.mark.asyncio
async def test_browser_opens_page():
    '''Тест проверяет, что браузер может открывать страницы'''
    async with BrowserManager(headless=True) as browser_manager:
        # Открываем страницу
        page = await browser_manager.open_page('https://ya.ru')

        # Получаем заголовок страницы
        title = await page.title()
        logger.debug(f'Title: {title}')

        assert page is not None
        assert 'Яндекс' in title or 'яндекс' in title.lower()

        await page.close()
