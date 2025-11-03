from aiogram.types import Message

from src.domain.entities import User
from src.infrastructure.services import product_service
from src.infrastructure.services import logger
from src.presentation.bot.keyboard.main_menu import main_menu


async def command_start_handler(message: Message, product_service) -> None:
    user = User(
        id=str(message.from_user.id),
        username=message.from_user.username,
        chat_id=str(message.chat.id),
    )
    try:
        product_service.create_user(user)
        logger.info(f"👤 Пользователь {user.id} создан или уже существует")

    except Exception as e:
        logger.warning(f"Ошибка создания пользователя {user.id}: {e}")

    keyboard = main_menu()
    await message.answer(
        f"""
👋 Добро пожаловать, {message.from_user.full_name}! Я — Pricely, твой личный помощник по отслеживанию цен на Ozon 🛒

📦 Просто пришли мне ссылку на товар, и я:
    • Добавлю его в список отслеживания  
    • Буду регулярно проверять цену  
    • Уведомлю тебя, когда она снизится 💸

✨ Начнём? Открой клавиатуру и отправь ссылку на любой товар с Ozon!
        """,
        reply_markup=keyboard,
    )
