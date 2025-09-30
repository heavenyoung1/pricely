from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
import asyncio
from src.presentation.bot.config import BOT_TOKEN
from src .infrastructure.services.logger import logger
dp = Dispatcher()

# Подключаем обработчики
from .handlers.start import command_start_handler
from .handlers.help import command_help_handler
from .handlers.products import (
    add_product_request, 
    add_product_process, 
    get_my_product_list, 
    handle_product_button,
    handle_update_price
    )

# Подключаем обработчики для сообщений и callback-запросов

dp.message.register(command_start_handler, CommandStart())
dp.message.register(command_help_handler, Command('help'))
dp.message.register(add_product_request, Command('add_product'))
dp.message.register(add_product_process)  # Если add_product_process должен быть следующим шагом

# Обработчики для callback-запросов (кнопки в сообщении)
dp.callback_query.register(handle_product_button, lambda call: call.data.startswith("product:"))
dp.callback_query.register(handle_update_price, lambda call: call.data.startswith("update_price:"))

async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logger.info('Бот запущен')
    asyncio.run(main())