from aiogram.types import Message, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    """Инициирует процесс добавления товара."""
    await message.answer("📦 Отправь ссылку на товар с Ozon")
    await state.set_state(ProductAddState.waiting_for_url)
    await message.answer("⏳ Парсинг начался, ожидайте...")


async def add_product_process(message: Message, state: FSMContext):
    """Обрабатывает URL товара и добавляет товар в систему."""
    if not await state.get_state() == ProductAddState.waiting_for_url:
        return
    
    url = message.text.strip()
    try:
        # Сначала отправляем сообщение о начале парсинга
        await message.answer("⏳ Парсинг начался, ожидайте...")
        
        # Теперь выполняем логику добавления товара
        result = product_service.create_product(str(message.from_user.id), url)

        # Когда товар добавлен, отправляем сообщение с результатом
        await message.answer(
            f"✅ Товар добавлен!\n\n"
            f"Название: {result['product_name']}\n"
            f"Цена с картой: {result['with_card']} ₽\n"
            f"Цена без карты: {result['without_card']} ₽",
            reply_markup=build_product_actions_keyboard(result['product_id'], result['link'])
        )
    except Exception as e:
        logger.exception("Ошибка при добавлении товара")
        await message.answer(f"❌ Ошибка: {e}")
    finally:
        await state.clear()


# ================= ПОЛУЧИТЬ СПИСОК ТОВАРОВ ================= #

async def get_my_product_list(message: Message):
    """Отображает список товаров пользователя."""
    try:
        products = product_service.get_all_products(str(message.from_user.id))
        
        if not products:
            await message.answer('📭 У вас пока нет отслеживаемых товаров')
            return
        
        inline_keyboard = [
            [InlineKeyboardButton(
                text=_truncate_name(p.get('name') or p.get('product_name') or p.get('id')),
                callback_data=f"product:{p['id']}"
            )]
            for p in products
        ]
        
        kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        await message.answer("📋 Ваши товары:", reply_markup=kb)

    except Exception as e:
        logger.exception('Ошибка при получении списка товаров')
        await message.answer(f'❌ Ошибка: {e}')


async def handle_product_button(call: CallbackQuery):
    """Отображает детальную информацию о товаре."""
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


# ================= ОБНОВИТЬ ЦЕНУ ================= #

async def handle_update_price(call: CallbackQuery):
    """Обновляет цену товара и отображает результат."""
    product_id = call.data.split(':', 1)[1]
    logger.info(f'Начинаем обновление цены для товара {product_id}')

    try:
        await call.answer("⏳ Обновляем цену...")
        
        # update_product_price возвращает {"full_product": {...}, "is_changed": bool}
        result = product_service.update_product_price(product_id)
        
        # Извлекаем полные данные о товаре
        full_product_info = result['full_product']
        is_changed = result.get('is_changed', False)
        
        logger.info(f"Получены данные товара: {full_product_info}")

        new_text = _build_price_update_message(full_product_info, full_product_info)
        new_markup = build_product_actions_keyboard(product_id, full_product_info['link'])

        await _safe_edit_message(
            call.message, 
            new_text, 
            new_markup,
            is_changed,
        )

    except Exception as e:
        logger.exception('❌ Ошибка при обновлении цены')
        await _show_error_message(call, product_id)


# ================= ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ================= #

def _truncate_name(name: str, max_length: int = 60) -> str:
    """Обрезает имя товара до заданной длины."""
    return name if len(name) <= max_length else name[:max_length - 3] + '...'


def _get_price_change_emoji(current: float, previous: float) -> str:
    """Возвращает эмодзи в зависимости от изменения цены."""
    if current > previous:
        return "🔺"  # Увеличилась
    elif current < previous:
        return "🔻"  # Уменьшилась
    else:
        return "🔄"  # Не изменилась


def _build_price_update_message(updated_product: dict, full_info: dict) -> str:
    """Формирует сообщение об обновлении цены."""
    logger.info(f'FULL INFO DEBUG!!!! {full_info}')
    name = updated_product['name']
    price_with_card = full_info['latest_price']['with_card']
    price_without_card = full_info['latest_price']['without_card']
    prev_with_card = full_info['latest_price']['previous_price_with_card']
    prev_without_card = full_info['latest_price']['previous_price_without_card']
    
    emoji = _get_price_change_emoji(price_with_card, prev_with_card)
    updated_at = full_info['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    
    # Базовая информация
    message = (
        f"📦 {name}\n"
        f"💳 Цена с картой: {price_with_card} ₽ {emoji}\n"
        f"💵 Цена без карты: {price_without_card} ₽ {emoji}\n"
        f"🔗 Ссылка на товар: {updated_product['link']}\n\n"
        f"📊 Предыдущие цены:\n"
        f"  💳 С картой: {prev_with_card} ₽\n"
        f"  💵 Без карты: {prev_without_card} ₽\n\n"
        f"⏰ Обновлено: {updated_at}"
    )
    
    # Добавляем префикс если цена не изменилась
    if emoji == "🔄":
        message = f"✅ Цена не изменилась\n\n{message}"
    
    return message


async def _safe_edit_message(message, text: str, markup, is_changed: bool):
    """Безопасно редактирует сообщение с обработкой исключений."""
    try:
        await message.edit_text(
            text=text,
            parse_mode='HTML',
            reply_markup=markup,
            disable_web_page_preview=False
        )
        logger.info('✅ Цена обновлена!' if is_changed else '✅ Цена актуальна')
        
    except TelegramBadRequest as e:
        if "message is not modified" in str(e):
            logger.info('Сообщение не изменилось, пропускаем обновление')
        else:
            raise


async def _show_error_message(call: CallbackQuery, product_id: str):
    """Отображает сообщение об ошибке с кнопкой возврата."""
    try:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text='🔙 Назад', callback_data=f'product:{product_id}')
            ]]
        )
        await call.message.edit_text(
            '❌ Не удалось обновить цену. Попробуйте позже.',
            reply_markup=kb
        )
    except Exception:
        logger.exception('Не удалось обновить сообщение с ошибкой')
    