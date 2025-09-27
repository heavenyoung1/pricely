from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.presentation.bot.bot_instance import bot, format_product_message, build_product_actions_keyboard
from src.presentation.bot.service_connector import service
import logging

logger = logging.getLogger(__name__)

# 🔄 Обновить цену
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("update_price:"))
def handle_update_price(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        updated_product = service.update_product_price(product_id)  # твой UseCase для парсинга
        text = format_product_message(updated_product)
        kb = build_product_actions_keyboard(product_id=updated_product["id"], product_link=updated_product["link"])

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"✅ Цена обновлена!\n\n{text}",
            parse_mode="HTML",
            reply_markup=kb,
            disable_web_page_preview=False
        )
    except Exception as e:
        logger.exception("Ошибка при обновлении цены")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

# 🗑 Удалить товар
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("delete_product:"))
def handle_delete_product(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        service.delete_product(product_id)

        # показываем список товаров заново
        products = service.get_all_products(str(call.from_user.id))
        if not products:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📭 У вас больше нет отслеживаемых товаров"
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
            text="📋 Ваши товары (после удаления):",
            reply_markup=kb
        )
    except Exception as e:
        logger.exception("Ошибка при удалении товара")
        bot.answer_callback_query(call.id, f"❌ Ошибка: {e}")

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
