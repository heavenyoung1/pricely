from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

from src.presentation.bot.config import BOT_TOKEN
from src .infrastructure.services.logger import logger

# FSM состояния
from src.presentation.bot.utils.fsm import ProductAddState

# Подключаем обработчики
from .handlers.start import command_start_handler
from .handlers.help import command_help_handler
from .handlers.products import (
    add_product_request, 
    add_product_process, 
    get_my_product_list, 
    handle_product_button,
    handle_update_price,
    )

from src.presentation.bot.handlers.delete import (
    choose_product_to_delete,
    handle_delete_product_request,
    handle_confirm_delete,
    handle_cancel_delete,
)
from src.presentation.bot.handlers.navigation import handle_back_to_products
from src.presentation.bot.handlers.error import fallback

# Dispatcher с хранилищем FSM


def register_handlers():
    """
    Все хендлеры собираем в одном месте
    """


    logger.info("Все хендлеры зарегистрированы.")

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    logger.info('Бот запущен')

    # Общие команды
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(command_help_handler, Command("help"))

    # Обработка ТЕКСТОВЫХ кнопок из меню
    dp.message.register(add_product_request, F.text == "➕ Добавить товар")
    dp.message.register(get_my_product_list, F.text == "📋 Мои товары")
    dp.message.register(choose_product_to_delete, F.text == "➖ Удалить товар")
    dp.message.register(command_help_handler, F.text == "📖 Справка")

    # Добавление продукта через FSM
    dp.message.register(add_product_request, Command("add_product"))
    dp.message.register(add_product_process, ProductAddState.waiting_for_url)

    # Список товаров (только из БД, без парсинга!)
    dp.message.register(get_my_product_list, Command("my_products"))

    # Удаление товара
    dp.message.register(choose_product_to_delete, Command("delete"))
    dp.callback_query.register(handle_delete_product_request, lambda call: call.data.startswith("delete_product:"))
    dp.callback_query.register(handle_confirm_delete, lambda call: call.data.startswith("confirm_delete:"))
    dp.callback_query.register(handle_cancel_delete, lambda call: call.data.startswith("cancel_delete:"))

    # Навигация
    dp.callback_query.register(handle_back_to_products, F.data == "back_to_products")

    # Действия с товарами
    dp.callback_query.register(handle_product_button, lambda call: call.data.startswith("product:"))
    dp.callback_query.register(handle_update_price, lambda call: call.data.startswith("update_price:"))

    # Фолбек — всегда в самом конце, чтобы перехватывал только незарегистрированные команды
    dp.message.register(fallback)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())