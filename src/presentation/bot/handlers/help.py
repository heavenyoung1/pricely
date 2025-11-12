import logging
from aiogram.types import Message
from src.infrastructure.services import logger

logger = logging.getLogger(__name__)


async def command_help_handler(message: Message) -> None:
    logger.debug(f"Получена команда /help от {message.from_user.id}")
    text = (
        "🚀 Контакты для связи https://t.me/heavenyoung)\n"
        " === v.1.0.5 ===!"
    )
    try:
        # Отправляем сообщение в тот же чат, откуда пришло
        await message.answer(text)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
