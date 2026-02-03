import pytest
import pytest_asyncio
from infrastructure.parsers.browser import BrowserManager


@pytest_asyncio.fixture
async def browser_manager():
    '''Фикстура для создания менеджера браузера'''
    manager = BrowserManager(headless=True)
    yield manager
    await manager.close()
