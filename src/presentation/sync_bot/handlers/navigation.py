from telebot.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from src.presentation.sync_bot.bot_instance import bot, logger
from src.presentation.sync_bot.service_connector import service

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


# @bot.callback_query_handler(func=lambda call: True)
# def catch_all(call: CallbackQuery):
#     print("CATCHED CALLBACK:", call.json)
#     bot.answer_callback_query(call.id, "catch!")

def register_handlers(bot):
    bot.callback_query_handler(func=lambda call: call.data == "back_to_products")(handle_back_to_products)
    # bot.callback_query_handler(func=lambda call: True)(catch_all)