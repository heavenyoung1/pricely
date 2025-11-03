import logging
from aiogram.types import Message
from src.infrastructure.services import logger

logger = logging.getLogger(__name__)


async def command_help_handler(message: Message) -> None:
    logger.debug(f"Получена команда /help от {message.from_user.id}")
    text = (
        "📖 Справка:\n\n"
        "➕ Добавить товар\n"
        "📋 Мои товары\n"
        "➖ Удалить товар\n"
        "🗑 Очистить все\n"
        "📊 Статистика\n\n"
        "🔗 Мой проект на GitHub: [Pricely](https://github.com/heavenyoung1/pricely)\n"
        "🚀 Приглашаю к сотрудничеству! Буду рад работать вместе!"
    )
    try:
        # Отправляем сообщение в тот же чат, откуда пришло
        await message.answer(text)
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения: {e}")
