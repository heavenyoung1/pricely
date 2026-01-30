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