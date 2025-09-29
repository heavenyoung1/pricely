from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.presentation.bot.bot_instance import bot, logger, format_product_message, build_product_actions_keyboard
from src.presentation.bot.service_connector import service
from src.presentation.bot.keyboards.main_menu import main_menu
# ================= МЕНЮ =================

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

# ================= CALLBACKS =================

# 📦 Открыть карточку
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("product:"))
def handle_product_button(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        product = service.get_full_product(product_id)
        if not product:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="❌ Товар не найден."
            )
            return

        text = format_product_message(product)
        kb = build_product_actions_keyboard(product_id=product["id"], product_link=product["link"])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=kb,
            disable_web_page_preview=False
        )
    except Exception as e:
        logger.exception("Ошибка в handle_product_button")
        bot.answer_callback_query(call.id, f"Ошибка: {e}")

# 🔄 Обновить цену
@bot.callback_query_handler(func=lambda call: call.data.startswith("update_price:"))
def handle_update_price(call: CallbackQuery):
    product_id = call.data.split(":", 1)[1]

    try:
        updated_product = service.update_product_price(product_id)

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=format_product_message(updated_product),
            reply_markup=build_product_actions_keyboard(product_id, updated_product["link"])
        )
    except Exception as e:
        logger.exception("Ошибка при обновлении цены")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

# ================= УДАЛЕНИЕ ТОВАРА =================

# 1️⃣ Из главного меню показываем список товаров для удаления
@bot.message_handler(func=lambda m: m.text == "➖ Удалить товар")
def choose_product_to_delete(message: Message):
    try:
        products = service.get_all_products(str(message.from_user.id))
        if not products:
            bot.send_message(message.chat.id, "📭 У вас пока нет отслеживаемых товаров")
            return

        kb = InlineKeyboardMarkup(row_width=1)
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            kb.add(InlineKeyboardButton(text=f"🗑 {display}", callback_data=f"delete_product:{p['id']}"))

        bot.send_message(message.chat.id, "Выбери товар для удаления:", reply_markup=kb)
    except Exception as e:
        logger.exception("Ошибка при показе списка для удаления")
        bot.send_message(message.chat.id, f"❌ Ошибка: {e}")


# 2️⃣ Запрос подтверждения
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("delete_product:"))
def handle_delete_product_request(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        product = service.get_full_product(product_id)
        if not product:
            bot.answer_callback_query(call.id, "❌ Товар не найден")
            return

        kb = InlineKeyboardMarkup(row_width=2)
        kb.add(
            InlineKeyboardButton("✅ Да, удалить", callback_data=f"confirm_delete:{product_id}"),
            InlineKeyboardButton("❌ Отмена", callback_data=f"cancel_delete:{product_id}")
        )

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"⚠️ Удалить товар <b>{product['name']}</b>?",
            parse_mode="HTML",
            reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при запросе подтверждения удаления")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")


# 3️⃣ Подтверждение удаления
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("confirm_delete:"))
def handle_confirm_delete(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        service.delete_product(product_id)

        products = service.get_all_products(str(call.from_user.id))
        if not products:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="🗑️ Товар удалён.\n📭 У вас больше нет отслеживаемых товаров."
            )
            return

        kb = InlineKeyboardMarkup(row_width=1)
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            kb.add(InlineKeyboardButton(text=display, callback_data=f"product:{p['id']}"))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🗑️ Товар удалён.\n📋 Ваши товары:",
            reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при подтверждении удаления")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")


# 4️⃣ Отмена удаления
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("cancel_delete:"))
def handle_cancel_delete(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        product = service.get_full_product(product_id)
        if not product:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="❌ Товар не найден"
            )
            return

        text = format_product_message(product)
        kb = build_product_actions_keyboard(product_id=product["id"], product_link=product["link"])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=kb,
            disable_web_page_preview=False
        )
    except Exception as e:
        logger.exception("Ошибка при отмене удаления")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

# ==================================

# ⬅️ Назад
@bot.callback_query_handler(func=lambda call: call.data == "back_to_products")
def handle_back_to_products(call: CallbackQuery):
    bot.answer_callback_query(call.id)

    try:
        products = service.get_all_products(str(call.from_user.id))
        if not products:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📭 У вас пока нет отслеживаемых товаров"
            )
            return

        kb = InlineKeyboardMarkup(row_width=1)
        for p in products:
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            kb.add(InlineKeyboardButton(text=display, callback_data=f"product:{p['id']}"))

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="📋 Ваши товары:",
            reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при возврате к списку товаров")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")


@bot.callback_query_handler(func=lambda call: True)
def catch_all(call: CallbackQuery):
    print("CATCHED CALLBACK:", call.json)
    bot.answer_callback_query(call.id, "catch!")