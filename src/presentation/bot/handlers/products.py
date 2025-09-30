from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.infrastructure.services import product_service
from src.infrastructure.services import logger


async def my_products(message: Message):
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
            name = p.get("name") or p.get("product_name") or p.get("id")
            display = name if len(name) <= 60 else name[:57] + "..."
            kb.add(InlineKeyboardButton(text=display, callback_data=f"product:{p['id']}"))
    except Exception as e:
        logger.exception("Ошибка при получении списка товаров")
        await message.answer(f"❌ Ошибка: {e}")
        

