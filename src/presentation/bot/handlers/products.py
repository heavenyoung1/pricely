from telebot.types import Message
from src.presentation.bot.bot_instance import bot
from src.presentation.bot.service_connector import service
from src.presentation.bot.keyboards.main_menu import main_menu

@bot.message_handler(func=lambda m: m.text == "➕ Добавить товар")
def add_product_request(message: Message):
    bot.send_message(message.chat.id, "📦 Отправь ссылку на товар с Ozon")
    bot.register_next_step_handler(message, add_product_process)

def add_product_process(message: Message):
    url = message.text.strip()
    try:
        result = service.create_product(str(message.from_user.id), url)
        bot.send_message(
            message.chat.id,
            f"✅ Товар добавлен!\n\n"
            f"Название: {result['name']}\n"
            f"Цена с картой: {result['with_card']} ₽\n"
            f"Цена без карты: {result['without_card']} ₽",
            reply_markup=main_menu()
        )
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda m: m.text == "📋 Мои товары" in m.text)
def list_products(message: Message):
    try:
        products = service.get_all_products(str(message.from_user.id))
        if not products:
            bot.send_message(message.chat.id, "📭 У вас пока нет отслеживаемых товаров")
            return
        text = "📋 Ваши товары:\n\n"
        for p in products:
            latest = p["latest_price"]
            text += f"{p['name']} — {latest['with_card']} ₽ (с картой)\n"
        bot.send_message(message.chat.id, text)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda m: m.text == "➖ Удалить товар")
def delete_product_request(message: Message):
    bot.send_message(message.chat.id, "❌ Введи артикул товара для удаления")
    bot.register_next_step_handler(message, delete_product_process)

def delete_product_process(message: Message):
    product_id = message.text.strip()
    try:
        service.delete_product(product_id)
        bot.send_message(message.chat.id, f"✅ Товар {product_id} удалён")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda m: m.text == "🗑️ Очистить все")
def clear_products(message: Message):
    try:
        service.delete_all_products(str(message.from_user.id))
        bot.send_message(message.chat.id, "🗑️ Все товары удалены")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda m: True)  # временно ловим все сообщения
def debug_all(message: Message):
    print(f"DEBUG: {repr(message.text)}")
