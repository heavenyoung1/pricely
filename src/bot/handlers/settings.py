from telebot.types import Message

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "⚙️ Настройки")
    def settings_menu(message: Message):
        bot.send_message(message.chat.id, "Здесь будут настройки (пока заглушка).")
