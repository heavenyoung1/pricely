from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from src.presentation.bot.bot_instance import bot, logger
from src.presentation.bot.service_connector import service
from src.presentation.bot.keyboards.main_menu import main_menu

@bot.message_handler(func=lambda m: m.text == "➕ Добавить товар")
def add_product_request(message: Message):
    bot.send_message(message.chat.id, "📦 Отправь ссылку на товар с Ozon")
    bot.register_next_step_handler(message, add_product_process)

def add_product_process(message: Message):
    bot.send_message(message.chat.id, "⏳ Парсинг начался, ожидайте...")
    url = message.text.strip()
    try:
        result = service.create_product(str(message.from_user.id), url)

        bot.send_message(
            message.chat.id,
            f"✅ Товар добавлен!\n\n"
            f"Название: {result['product_name']}\n"
            f"Цена с картой: {result['with_card']} ₽\n"
            f"Цена без карты: {result['without_card']} ₽",
            reply_markup=main_menu()
        )

    except Exception as e:
        logger.exception("Ошибка при добавлении товара")
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda m: "📋 Мои товары" in m.text)
def list_products(message: Message):
    try:
        products = service.get_all_products(str(message.from_user.id))
        if not products:
            bot.send_message(message.chat.id, "📭 У вас пока нет отслеживаемых товаров")
            return

        kb = InlineKeyboardMarkup(row_width=1)
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            kb.add(InlineKeyboardButton(text=display, callback_data=f"product:{p['id']}"))

        bot.send_message(message.chat.id, "📋 Ваши товары:", reply_markup=kb)
    except Exception as e:
        logger.exception("Ошибка при получении списка товаров")
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

@bot.message_handler(func=lambda m: m.text == "🗑️ Очистить все")
def clear_products(message: Message):
    try:
        service.delete_all_products(str(message.from_user.id))
        bot.send_message(message.chat.id, "🗑️ Все товары удалены")
    except Exception as e:
        logger.exception("Ошибка при очистке товаров")
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")

def register_handlers(bot):
    bot.message_handler(func=lambda m: m.text == "➕ Добавить товар")(add_product_request)
    bot.message_handler(func=lambda m: "📋 Мои товары" in m.text)(list_products)
    bot.message_handler(func=lambda m: m.text == "🗑️ Очистить все")(clear_products)