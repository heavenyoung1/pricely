from telebot.types import Message
from src.presentation.sync_bot.bot_instance import bot

@bot.message_handler(func=lambda m: True)
def fallback(message: Message):
    bot.send_message(message.chat.id, "❓ Неизвестная команда. Напишите /help")

def register_handlers(bot):
    bot.message_handler(func=lambda m: True)(fallback)