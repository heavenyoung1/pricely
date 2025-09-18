from telebot.types import Message
from src.presentation.bot.bot_instance import bot
from src.presentation.bot.keyboards.main_menu import main_menu

@bot.message_handler(func=lambda m: m.text == "📊 Статистика")
def show_statistics(message: Message):
    text = (
        f"📊 Статистика\n\n"
        f"👤 Пользователь: {message.from_user.first_name}\n"
        f"📦 Товаров: 0\n"
        f"💰 Средняя цена: 0 ₽\n"
        f"📉 Скидок найдено: 0\n"
        f"🕒 Последнее обновление: никогда"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())
