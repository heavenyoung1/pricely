from aiogram.types import Message
from src.infrastructure.services import logger

async def command_help_handler(message: Message) -> None:
    logger.debug(f'Получена команда /help от {message.from_user.id}')
    text = (
        '📖 Справка:\n\n'
        '➕ Добавить товар\n'
        '📋 Мои товары\n'
        '➖ Удалить товар\n'
        '🗑 Очистить все\n'
        '📊 Статистика'
    )
    try:
        # Отправляем сообщение в тот же чат, откуда пришло
        await message.answer(text)
    except Exception as e:
        logger.error(f'Ошибка при отправке сообщения: {e}')
