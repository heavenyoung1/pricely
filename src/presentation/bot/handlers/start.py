from telebot.types import Message
from src.presentation.bot.bot_instance import bot
from src.presentation.bot.keyboards.main_menu import main_menu
from src.presentation.bot.service_connector import service
from src.domain.entities import User

import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=["start"])
def start_handler(message: Message):
    user = User(
        id=str(message.from_user.id),
        username=message.from_user.username or "unknown",
        chat_id=str(message.chat.id),
    )
    try:
        service.create_user(user)
        logger.info(f"User {user.id} создан или уже существует")
    except Exception as e:
        logger.warning(f"Ошибка создания пользователя {user.id}: {e}")
                # Продолжаем, так как пользователь может уже существовать

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать! Я бот для отслеживания цен Ozon.",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=["help"])
def help_handler(message: Message):
    logger.debug(f"Received /help command from user {message.from_user.id}")
    text = (
        "📖 Справка:\n\n"
        "➕ Добавить товар\n"
        "📋 Мои товары\n"
        "➖ Удалить товар\n"
        "🗑 Очистить все\n"
        "📊 Статистика"
    )
    try:
        bot.send_message(message.chat.id, text, reply_markup=main_menu())
        logger.debug(f"Sent help message to chat {message.chat.id}")
    except Exception as e:
        logger.error(f"Failed to send help message to chat {message.chat.id}: {e}", exc_info=True)

@bot.message_handler(content_types=['text'])
def echo_handler(message: Message):
    logger.debug(f"Received text message from user {message.from_user.id}: {message.text}")
    try:
        bot.reply_to(message, f"You said: {message.text}")
        logger.debug(f"Replied to message in chat {message.chat.id}")
    except Exception as e:
        logger.error(f"Failed to reply to message in chat {message.chat.id}: {e}", exc_info=True)