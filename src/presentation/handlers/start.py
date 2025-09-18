from telebot.types import Message
from src.presentation.bot.bot_instance import bot
from src.presentation.bot.keyboards.main_menu import main_menu
from src.presentation.bot.services_connector import service
from src.domain.entities import User

@bot.message_handler(commands=["start"])
def start_handler(message: Message):
    user = User(
        id=str(message.from_user.id),
        username=message.from_user.username or "unknown",
        chat_id=str(message.chat.id),
    )
    try:
        service.create_user(user)
    except Exception:
        pass  # юзер уже есть

    bot.send_message(
        message.chat.id,
        "👋 Добро пожаловать! Я бот для отслеживания цен Ozon.",
        reply_markup=main_menu()
    )

@bot.message_handler(commands=["help"])
def help_handler(message: Message):
    text = (
        "📖 Справка:\n\n"
        "➕ Добавить товар\n"
        "📋 Мои товары\n"
        "➖ Удалить товар\n"
        "🗑 Очистить все\n"
        "📊 Статистика"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())
