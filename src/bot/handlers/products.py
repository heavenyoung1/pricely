from telebot.types import Message

def register_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "➕ Добавить товар")
    def add_product(message: Message):
        bot.send_message(message.chat.id, "Отправь ссылку на товар, который хочешь отслеживать.")

    @bot.message_handler(func=lambda m: m.text == "➖ Удалить товар")
    def remove_product(message: Message):
        bot.send_message(message.chat.id, "Выбери товар для удаления (пока заглушка).")

    @bot.message_handler(func=lambda m: m.text == "📋 Мои товары")
    def list_products(message: Message):
        bot.send_message(message.chat.id, "Твои отслеживаемые товары (пока заглушка).")
