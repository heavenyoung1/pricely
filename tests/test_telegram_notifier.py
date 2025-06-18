from unittest.mock import AsyncMock, patch
import pytest
from datetime import datetime

from core.telegram_notifier import TelegramNotifier
from models.product import Product


@pytest.fixture
def telegram_notifier():
    with patch('pricetracker.core.telegram_notifier.Bot') as mock_bot:
        notifier = TelegramNotifier(bot_token='fake_token')
        notifier.bot = AsyncMock()
        notifier.bot.send_message = AsyncMock()
        return notifier

@pytest.fixture
def sample_product():
    return Product(
        id='123',
        url='https://ozon.ru/product/1234567889',
        name='Test Product',
        price=900,
        last_updated=datetime(2025, 6, 16)
    )

@pytest.mark.asyncio
async def test_notify(telegram_notifier, sample_product):
    await telegram_notifier.notify(chat_id=12345, product=sample_product, old_price=1000.0)
    telegram_notifier.bot.send_message.assert_called_once()
    args, kwargs = telegram_notifier.bot.send_message.call_args
    assert kwargs['chat_id'] == 12345
    assert 'Цена изменилась' in kwargs['text']
    assert 'Test Product' in kwargs['text']
    assert 'Старая цена: 1000' in kwargs['text']
    assert 'Новая цена: 900' in kwargs['text']