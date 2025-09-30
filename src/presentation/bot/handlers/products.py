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
