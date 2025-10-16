from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage

from src.presentation.bot.config import BOT_TOKEN
from src.presentation.bot.utils.fsm import ProductAddState
from .handlers.start import command_start_handler
from .handlers.help import command_help_handler
from .handlers.products import (
    add_product_request, 
    add_product_process, 
    get_my_product_list, 
    handle_product_button,
)
from src.presentation.bot.handlers.delete import (
    choose_product_to_delete,
    handle_delete_product_request,
    handle_confirm_delete,
    handle_cancel_delete,
)
from src.presentation.bot.handlers.navigation import handle_back_to_products
from src.presentation.bot.handlers.error import fallback
from src.infrastructure.services.logger import logger


def register_message_handlers(dp):
    '''Регистрация обработчиков для сообщений'''
    dp.message.register(command_start_handler, CommandStart())

    # Обработка текстовых кнопок
    dp.message.register(add_product_request, F.text == '➕ Добавить товар')
    dp.message.register(get_my_product_list, F.text == '📋 Мои товары')
    dp.message.register(choose_product_to_delete, F.text == '➖ Удалить товар')
    dp.message.register(command_help_handler, F.text == '📖 Справка')

    # Добавление продукта через FSM
    dp.message.register(add_product_request, Command('add_product'))
    dp.message.register(add_product_process, ProductAddState.waiting_for_url)

    # Список товаров
    dp.message.register(get_my_product_list, Command('my_products'))

    # Удаление товара
    dp.message.register(choose_product_to_delete, Command('delete'))


def register_callback_handlers(dp):
    '''Регистрация обработчиков для callback-запросов'''
    dp.callback_query.register(handle_delete_product_request, lambda call: call.data.startswith('delete_product:'))
    dp.callback_query.register(handle_confirm_delete, lambda call: call.data.startswith('confirm_delete:'))
    dp.callback_query.register(handle_cancel_delete, lambda call: call.data.startswith('cancel_delete:'))

    # Навигация
    dp.callback_query.register(handle_back_to_products, F.data == 'back_to_products')

    # Действия с товарами
    dp.callback_query.register(handle_product_button, lambda call: call.data.startswith('product:'))


def register_fallback_handler(dp):
    '''Регистрация фолбек обработчика'''
    dp.message.register(fallback)

    logger.info('Все хендлеры зарегистрированы.')

async def create_bot():# -> (Bot, Dispatcher):
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    return bot, dp
