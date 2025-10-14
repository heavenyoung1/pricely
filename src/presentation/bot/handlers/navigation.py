import logging
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.infrastructure.services import product_service

logger = logging.getLogger(__name__)

async def handle_back_to_products(call: CallbackQuery):
    await call.answer()  # Отправляем ответ на callback-запрос

    try:
        # Получаем все товары пользователя
        products = product_service.get_all_products(str(call.from_user.id))
        if not products:
            await call.message.edit_text(
                '📭 У вас пока нет отслеживаемых товаров'
            )
            return

        # Создаем клавиатуру с товарами
        buttons = []
        for p in products:
            name = p.get('name') or p.get('product_name') or p.get('id')
            display = name if len(name) <= 60 else name[:57] + '...'
            buttons.append([InlineKeyboardButton(text=display, callback_data=f'product:{p["id"]}')])

        kb = InlineKeyboardMarkup(inline_keyboard=buttons)

        # Обновляем сообщение с клавиатурой и списком товаров
        await call.message.edit_text(
            '📋 Ваши товары:',
            reply_markup=kb
        )
    except Exception as e:
        logger.exception('Ошибка при возврате к списку товаров')
        await call.answer(f'❌ Ошибка: {e}')  # Отправляем сообщение об ошибке
