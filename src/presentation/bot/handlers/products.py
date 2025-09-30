from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.infrastructure.services import product_service
from src.infrastructure.services import logger
from src.presentation.bot.utils.formatters import format_product_message, format_categories
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard

async def get_my_product_list(message: Message):
    try:
        # Получаем список товаров пользователя
        products = product_service.get_all_products(str(message.from_user.id))

        # Если товаров нет
        if not products:
            await message.answer('📭 У вас пока нет отслеживаемых товаров')
            return
        
        kb = InlineKeyboardMarkup(row_width=1)
        # Добавляем кнопки для каждого товара (перебираем список словарей)
        for p in products: 
            name = p.get('name') or p.get('product_name') or p.get('id')
            display = name if len(name) <= 60 else name[:57] + '...'
            kb.add(InlineKeyboardButton(text=display, callback_data=f'product:{p['id']}'))
    except Exception as e:
        logger.exception('Ошибка при получении списка товаров')
        await message.answer(f'❌ Ошибка: {e}')
        
async def handle_product_button(call: CallbackQuery):
    await call.answer() # Отправляем ответ на callback, чтобы избежать 'залипания' кнопки
    
    # Извлекаем ID продукта из callback_data
    product_id = call.data.split(':', 1)[1]

    try:
        # Получаем полный продукт
        product = product_service.get_full_product(product_id)
        if not product:
            await call.message.edit_text('❌ Товар не найден.')
            return
        
        text = format_product_message(product)
         # Создаем клавиатуру для действия с продуктом
        kb = build_product_actions_keyboard(product_id=product['id'], product_link=product['link'])

        # Редактируем сообщение с информацией о товаре
        await call.message.edit_text(
            text=text,
            parse_mode='HTML',
            reply_markup=kb,
            disable_web_page_preview=False
        )

    except Exception as e:
        logger.exception('Ошибка в handle_product_button')
        await call.answer(f'Ошибка: {e}')

# 🔄 Обновить цену
async def handle_update_price(call: CallbackQuery):
    product_id = call.data.split(':', 1)[1]
    logger.info(f'Начинаем обновление цены для товара {product_id}')

    # Сразу отвечаем на callback, чтобы избежать timeout
    try:
        await call.answer('🔄 Обновляем цену...')
        logger.info('Ответили на callback query')
    except Exception as e:
        logger.warning(f'Не удалось ответить на callback query: {e}')

    try:
        # Обновляем цену
        logger.info('Вызываем service.update_product_price')
        updated_product = await product_service.update_product_price(product_id)
        logger.info(f'Получили обновленный товар: {type(updated_product)} - {updated_product}')

        # Формируем новое сообщение
        logger.info('Формируем новое сообщение')
        new_text = await format_product_message(updated_product)
        logger.info(f'Сформированный текст: {new_text}')

        new_markup = build_product_actions_keyboard(product_id, updated_product['link'])
        logger.info('Клавиатура сформирована')

        # Проверка на изменения, чтобы избежать отправки одинаковых данных
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        current_text = call.message.text
        current_markup = call.message.reply_markup

        if new_text != current_text or new_markup != current_markup:
            logger.info('Обновляем сообщение с новыми данными')
            await call.message.edit_text(
                text=new_text,
                parse_mode='HTML',
                reply_markup=new_markup,
                disable_web_page_preview=False
            )
            logger.info('✅ Сообщение успешно обновлено!')
        else:
            logger.info('Данные не изменились, обновление не требуется.')
        
    except Exception as e:
        logger.exception('❌ Ошибка при обновлении цены')
        
        # В случае ошибки показываем сообщение об ошибке
        try:
            await call.message.edit_text(
                f'❌ Ошибка при обновлении цены: {e}',
                reply_markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton('🔙 Назад', callback_data=f'product:{product_id}')
                )
            )
        except Exception as edit_error:
            logger.exception('Не удалось обновить сообщение с ошибкой')   

    