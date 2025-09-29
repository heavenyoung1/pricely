from telebot.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.presentation.bot.bot_instance import bot, logger
from src.presentation.bot.utils.formatters import format_product_message
from src.presentation.bot.utils.keyboards import build_product_actions_keyboard
from src.presentation.bot.service_connector import service
from src.presentation.bot.keyboards.main_menu import main_menu

# 📦 Открыть карточку
@bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("product:"))
def handle_product_button(call: CallbackQuery):
    bot.answer_callback_query(call.id)
    product_id = call.data.split(":", 1)[1]

    try:
        # Убедись, что get_full_product возвращает словарь
        product = service.get_full_product(product_id)
        if not product:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="❌ Товар не найден."
            )
            return

        text = format_product_message(product)  # Передаем словарь
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
    logger.info(f"Начинаем обновление цены для товара {product_id}")
    
    # Сразу отвечаем на callback, чтобы избежать timeout
    try:
        bot.answer_callback_query(call.id, "🔄 Обновляем цену...")
        logger.info("Ответили на callback query")
    except Exception as e:
        logger.warning(f"Не удалось ответить на callback query: {e}")
    
    # Показываем индикатор загрузки
    try:
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⏳ Обновление цены...",
            reply_markup=None
        )
        logger.info("Показали индикатор загрузки")
    except Exception as e:
        logger.warning(f"Не удалось обновить сообщение на индикатор загрузки: {e}")

    try:
        # Обновляем цену
        logger.info("Вызываем service.update_product_price")
        updated_product = service.update_product_price(product_id)
        logger.info(f"Получили обновленный товар: {type(updated_product)} - {updated_product}")
        
        # Формируем новое сообщение
        logger.info("Формируем новое сообщение")
        new_text = format_product_message(updated_product)
        logger.info(f"Сформированный текст: {new_text}")
        
        new_markup = build_product_actions_keyboard(product_id, updated_product['link'])
        logger.info("Клавиатура сформирована")
        
        # Проверка на изменения, чтобы избежать отправки одинаковых данных
        current_text = call.message.text
        current_markup = call.message.reply_markup

        if new_text != current_text or new_markup != current_markup:
            logger.info("Обновляем сообщение с новыми данными")
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=new_text,
                parse_mode="HTML",
                reply_markup=new_markup,
                disable_web_page_preview=False
            )
            logger.info("✅ Сообщение успешно обновлено!")
        else:
            logger.info("Данные не изменились, обновление не требуется.")
        
    except Exception as e:
        logger.exception("❌ Ошибка при обновлении цены")
        
        # В случае ошибки показываем сообщение об ошибке
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"❌ Ошибка при обновлении цены: {e}",
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🔙 Назад", callback_data=f"product:{product_id}")
                )
            )
        except Exception as edit_error:
            logger.exception("Не удалось обновить сообщение с ошибкой")

def register_handlers(bot):
    bot.callback_query_handler(func=lambda call: call.data and call.data.startswith("product:"))(handle_product_button)