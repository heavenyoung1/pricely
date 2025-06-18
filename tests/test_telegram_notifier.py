import pytest
from unittest.mock import AsyncMock, Mock, patch
from datetime import datetime

from core.telegram_notifier import TelegramNotifier
from models.product import Product


@pytest.fixture
def product():
    return Product(
        id='1234567889',
        url='https://ozon.ru/product/1234567889',
        name='Test Product',
        price=900,
        last_updated=datetime(2025, 6, 16)
    )

@pytest.fixture
def notifier():
    with patch('core.telegram_notifier.Bot') as MockBot:
        mock_bot_instance = Mock()
        mock_bot_instance.send_message = AsyncMock()

        MockBot.return_value = mock_bot_instance

        notifier = TelegramNotifier(bot_token='fake_token')
        return notifier

@pytest.mark.asyncio
async def test_notify(notifier, product):
    old_price = 1000
    await notifier.notify(chat_id=12345, product=product, old_price=old_price)

    notifier.bot.send_message.assert_called_once()
    message = notifier.bot.send_message.call_args.kwargs['text']

    assert 'Цена изменилась' in message
    assert 'Test Product' in message
    assert f'Старая цена: {old_price}' in message
    assert f'Новая цена: {product.price}' in message