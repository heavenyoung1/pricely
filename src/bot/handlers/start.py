from telebot.types import Message
from src.bot.keyboards.main_menu import main_menu

def register_handlers(bot):

    @bot.message_handler(commands=["start"])
    def cmd_start(message: Message):
        bot.send_message(
            message.chat.id,
            "👋 Привет! Я бот для отслеживания цен.\nВыбери действие:",
            reply_markup=main_menu()
        )
