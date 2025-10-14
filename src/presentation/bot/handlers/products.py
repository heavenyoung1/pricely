from aiogram.types import CallbackQuery, Message
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from datetime import datetime

from src.presentation.bot.utils.fsm import ProductAddState
from src.infrastructure.services import product_service
from src.infrastructure.services.logger import logger
from src.presentation.bot.utils.formatters import format_product_message
from src.presentation.bot.utils.keyboard import build_product_actions_keyboard


# ================= ДОБАВИТЬ ТОВАР ================= #

async def add_product_request(message: Message, state: FSMContext):
    '''Инициирует процесс добавления товара.'''
    await message.answer('📦 Отправь ссылку на товар с Ozon')
    await state.set_state(ProductAddState.waiting_for_url)
    await message.answer('⏳ Парсинг начался, ожидайте...')


async def add_product_process(message: Message, state: FSMContext):
    '''Обрабатывает URL товара и добавляет товар в систему.'''
    if not await state.get_state() == ProductAddState.waiting_for_url:
        return
    
    url = message.text.strip()
    try:
        # Сначала отправляем сообщение о начале парсинга
        await message.answer('⏳ Парсинг начался, ожидайте...')
        
        # Теперь выполняем логику добавления товара
        result = product_service.create_product(str(message.from_user.id), url)

        # Когда товар добавлен, отправляем сообщение с результатом
        await message.answer(
            f'✅ Товар добавлен!\n\n'
            f'Название: {result["product_name"]}\n'
            f'Цена с картой: {result["with_card"]} ₽\n'
            f'Цена без карты: {result["without_card"]} ₽',
            reply_markup=build_product_actions_keyboard(result['product_id'], result['link'])
        )
    except Exception as e:
        logger.exception('Ошибка при добавлении товара')
        await message.answer(f'❌ Ошибка: {e}')
    finally:
        await state.clear()


# ================= ПОЛУЧИТЬ СПИСОК ТОВАРОВ ================= #

async def get_my_product_list(message: Message):
    '''Отображает список товаров пользователя.'''
    try:
        products = product_service.get_all_products(str(message.from_user.id))
        
        if not products:
            await message.answer('📭 У вас пока нет отслеживаемых товаров')
            return
        
        inline_keyboard = [
            [InlineKeyboardButton(
                text=_truncate_name(p.get('name') or p.get('product_name') or p.get('id')),
                callback_data=f'product:{p["id"]}'
            )]
            for p in products
        ]
        
        kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await message.answer('📋 Ваши товары:', reply_markup=kb)

    except Exception as e:
        logger.exception('Ошибка при получении списка товаров')
        await message.answer(f'❌ Ошибка: {e}')


async def handle_product_button(call: CallbackQuery):
    '''Отображает детальную информацию о товаре.'''
    await call.answer()
    
    product_id = call.data.split(':', 1)[1]

    try:
        product = product_service.get_full_product(product_id)
        if not product:
            await call.message.edit_text('❌ Товар не найден.')
            return
        
        text = format_product_message(product)
        kb = build_product_actions_keyboard(product_id=product['id'], product_link=product['link'])

        await call.message.edit_text(
            text=text,
            parse_mode='HTML',
            reply_markup=kb,
            disable_web_page_preview=False
        )

    except Exception as e:
        logger.exception('Ошибка в handle_product_button')
        await call.answer(f'Ошибка: {e}', show_alert=True)

# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ================= #

def _truncate_name(name: str, max_length: int = 60) -> str:
    '''Обрезает имя товара до заданной длины.'''
    return name if len(name) <= max_length else name[:max_length - 3] + '...'