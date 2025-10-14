from aiogram.types import Message

from src.domain.entities import User
from src.infrastructure.services import product_service
from src.infrastructure.services import logger
from src.presentation.bot.keyboard.main_menu import main_menu

async def command_start_handler(message: Message) -> None:
    user = User(
        id=str(message.from_user.id),
        username=message.from_user.username,
        chat_id=str(message.chat.id), 
    )
    try:
        product_service.create_user(user)
        logger.info(f'Пользователь {user.id} создан или уже существует')

    except Exception as e:
        logger.warning(f'Ошибка создания пользователя {user.id}: {e}')

    keyboard = main_menu()
    await message.answer(
        f'👋 Добро пожаловать, {message.from_user.full_name}! Я бот для отслеживания цен Ozon.',
        reply_markup=keyboard
    )
