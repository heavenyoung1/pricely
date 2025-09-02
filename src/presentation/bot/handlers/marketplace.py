from telebot.types import Message
from src.bot.keyboards.main_menu import marketplaces, main_menu

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📦 Выбрать маркетплейс")
    def choose_marketplace(message: Message):
        bot.send_message(message.chat.id, "Выбери маркетплейс:", reply_markup=marketplaces())

    @bot.message_handler(func=lambda m: m.text in ["🟦 Ozon", "🟪 Wildberries"])
    def marketplace_selected(message: Message):
        bot.send_message(message.chat.id, f"✅ Ты выбрал {message.text}", reply_markup=main_menu())

    @bot.message_handler(func=lambda m: m.text == "⬅️ Назад")
    def back_to_menu(message: Message):
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
